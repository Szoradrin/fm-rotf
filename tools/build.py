#!/usr/bin/env python3
"""
fm-rotf build pipeline — Session 20.
One command: python3 tools/build.py
Gates (all must pass, fails loud, never proceeds past a failure):
  1. JSON validity          — every packs-src file parses
  2. Key conformance        — _id + canonical _key on docs and embedded children
  3. Uniqueness             — no duplicate _id per pack, no duplicate item/activity ids per doc
  4. Schema sanity          — critical field types (damage denominations numeric, etc.)
  5. Asset existence        — every referenced modules/rotf asset exists in repo
  6. Compile                — fvtt-cli, correct invocation, per-pack
  7. Count verification     — packed count == source count (catches SILENT SKIPS)
  8. Round-trip             — unpack compiled DB, semantic-diff against source
Exit 0 = all green. Exit 1 = gate failed, output says exactly where.
"""
import json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FVTT = os.path.expanduser("/home/claude/node_modules/.bin/fvtt")
PACKS = {
    "rotf-actors":  ("actors",  [("items", "actors.items")]),
    "rotf-journals":("journal", [("pages", "journal.pages")]),
    "rotf-scenes":  ("scenes",  [("levels", "scenes.levels")]),
    "rotf-tables":  ("tables",  [("results", "tables.results")]),
}
failures = []

def gate(name, ok, detail=""):
    mark = "✓" if ok else "✗"
    print(f"{mark} {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(f"{name}: {detail}")
    return ok

def load_all():
    docs = {}
    for pack in PACKS:
        pdir = os.path.join(ROOT, "packs-src", pack)
        docs[pack] = {}
        for fn in sorted(os.listdir(pdir)):
            if fn.endswith(".json"):
                docs[pack][fn] = os.path.join(pdir, fn)
    return docs

def main():
    docs = load_all()
    parsed = {}

    # Gate 1: JSON validity
    bad = []
    for pack, files in docs.items():
        parsed[pack] = {}
        for fn, path in files.items():
            try:
                with open(path) as f:
                    parsed[pack][fn] = json.load(f)
            except Exception as e:
                bad.append(f"{pack}/{fn}: {e}")
    gate("Gate 1: JSON validity", not bad, "; ".join(bad[:3]) or f"{sum(len(v) for v in parsed.values())} files")

    # Gate 2: key conformance
    bad = []
    for pack, (prefix, embedded) in PACKS.items():
        for fn, d in parsed[pack].items():
            if not d.get("_id"): bad.append(f"{pack}/{fn}: missing _id")
            elif d.get("_key") != f"!{prefix}!{d['_id']}": bad.append(f"{pack}/{fn}: bad _key")
            for coll, cprefix in embedded:
                for c in d.get(coll, []):
                    if not c.get("_id"): bad.append(f"{pack}/{fn}: {coll} child missing _id")
                    elif c.get("_key") != f"!{cprefix}!{d['_id']}.{c['_id']}":
                        bad.append(f"{pack}/{fn}: {coll}/{c.get('name','?')} bad _key")
    gate("Gate 2: _id/_key conformance", not bad, "; ".join(bad[:3]))

    # Gate 3: uniqueness
    bad = []
    for pack in PACKS:
        seen = {}
        for fn, d in parsed[pack].items():
            i = d.get("_id")
            if i in seen: bad.append(f"{pack}: dup _id {i} in {fn}+{seen[i]}")
            seen[i] = fn
        for fn, d in parsed[pack].items():
            iids = [c.get("_id") for c in d.get("items", [])]
            if len(iids) != len(set(iids)): bad.append(f"{pack}/{fn}: dup item ids")
            for c in d.get("items", []):
                aids = list(c.get("system", {}).get("activities", {}).keys())
                if len(aids) != len(set(aids)): bad.append(f"{pack}/{fn}/{c.get('name')}: dup activity ids")
    gate("Gate 3: ID uniqueness", not bad, "; ".join(bad[:3]))

    # Gate 4: schema sanity (grows as we learn)
    bad = []
    for fn, d in parsed["rotf-actors"].items():
        for it in d.get("items", []):
            for act in it.get("system", {}).get("activities", {}).values():
                for part in act.get("damage", {}).get("parts", []):
                    den = part.get("denomination")
                    if isinstance(den, str):
                        bad.append(f"{fn}/{it.get('name')}: damage denomination is string '{den}'")
    gate("Gate 4: schema sanity", not bad, "; ".join(bad[:3]) or "damage denominations numeric")

    # Gate 5: asset existence
    bad = []
    import re
    for pack in PACKS:
        for fn, d in parsed[pack].items():
            for m in re.finditer(r'modules/rotf/(assets/[^"\\\s<>]+)', json.dumps(d)):
                rel = m.group(1)
                if not os.path.exists(os.path.join(ROOT, rel)):
                    bad.append(f"{pack}/{fn}: missing {rel}")
    gate("Gate 5: asset existence", not bad, "; ".join(sorted(set(bad))[:3]))

    if failures:
        print(f"\nSTOP: {len(failures)} pre-compile failures. Not compiling."); sys.exit(1)

    # Gate 6+7: compile with count verification
    for pack in PACKS:
        target = os.path.join(ROOT, "packs", pack)
        subprocess.run(["rm", "-rf", target])
        r = subprocess.run([FVTT, "package", "pack", "-n", pack,
                            "--inputDirectory", f"packs-src/{pack}",
                            "--outputDirectory", "packs"],
                           cwd=ROOT, capture_output=True, text=True)
        out = r.stdout + r.stderr
        packed = out.count("\nPacked ") + (1 if out.startswith("Packed ") else 0)
        expected = len(parsed[pack])
        errs = ("Failed" in out) or ("LEVEL_INVALID" in out)
        ldb_ok = any(f.endswith(".ldb") and os.path.getsize(os.path.join(target, f)) > 0
                     for f in os.listdir(target)) if os.path.isdir(target) else False
        gate(f"Gate 6/7: compile+count {pack}", packed == expected and not errs and ldb_ok,
             f"{packed}/{expected} packed")

    if failures:
        print(f"\nSTOP: compile failures."); sys.exit(1)

    # Gate 8: round-trip semantic diff
    for pack in PACKS:
        with tempfile.TemporaryDirectory() as td:
            subprocess.run([FVTT, "package", "unpack", "-n", pack,
                            "--inputDirectory", "packs", "--outputDirectory", td],
                           cwd=ROOT, capture_output=True, text=True)
            unpacked = {}
            for fn in os.listdir(td):
                with open(os.path.join(td, fn)) as f:
                    d = json.load(f)
                unpacked[d["_id"]] = d
            bad = []
            for fn, src in parsed[pack].items():
                rt = unpacked.get(src["_id"])
                if rt is None: bad.append(f"{fn}: missing from round-trip"); continue
                if src.get("name") != rt.get("name"): bad.append(f"{fn}: name drift")
                for coll, _ in PACKS[pack][1]:
                    if len(src.get(coll, [])) != len(rt.get(coll, [])):
                        bad.append(f"{fn}: {coll} count drift {len(src.get(coll,[]))} -> {len(rt.get(coll,[]))}")
            gate(f"Gate 8: round-trip {pack}", not bad, "; ".join(bad[:3]) or f"{len(unpacked)} docs verified")

    print()
    if failures:
        print(f"BUILD FAILED — {len(failures)} gate failures"); sys.exit(1)
    print("BUILD GREEN — all gates passed. Safe to commit packs/ + packs-src/ and cut a release.")

if __name__ == "__main__":
    main()
