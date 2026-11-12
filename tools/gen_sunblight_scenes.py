"""Generate the Sunblight fortress scenes (game session 26, 2026-11-11).

Builds one new V14 scene with three levels (Forge, Command, Ice Gate). The existing
single-level Sunblight scenes are not changed. Token positions follow
book chapter 3 (D&D Beyond, read 2026-11-11), placed by eye on Reed's level maps.

Map images: 1670x942 sources, aligned so the elevators match across levels, upscaled
x2.5 to 4175x2355. 10 ft = 100 px, so the 5 ft grid is 50 px.

Usage: python tools/gen_sunblight_scenes.py   (then python tools/build.py)
"""
import copy, json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACT = os.path.join(ROOT, "packs-src", "rotf-actors")
SCN = os.path.join(ROOT, "packs-src", "rotf-scenes")
S = 2.5            # source px -> scene px
GRID = 50          # px per 5 ft
W, H = 4175, 2355
PAD = 0.25
# Token x/y are canvas coordinates, which include the scene padding (Foundry: ceil(pad*size/grid)*grid)
PAD_X = math.ceil(PAD * W / GRID) * GRID   # 1050
PAD_Y = math.ceil(PAD * H / GRID) * GRID   # 600
IMG = "modules/rotf/assets/images/map-3.1-sunblight-{}-level.webp"
JOURNAL = "SunblightJrnl001"

LEVELS = {  # code: (name, image slug, elevation bottom, top)
    "F": ("Forge Level", "forge", 0, 100),
    "C": ("Command Level", "command", 100, 200),
    "I": ("Ice Gate Level", "ice-gate", 200, 300),
}

NAMES = ["Bruvo", "Duerreth", "Dwargyn", "Fisketta", "Gurn", "Harmok", "Jarjun", "Jonkin",
         "Kolbrak", "Lurgash", "Mrod", "Mursk", "Narla", "Qualkin", "Rovaalt", "Skarda",
         "Skorn", "Throd", "Ulkinn", "Vygardt", "Zorzula", "Zulkrod"]
_n = iter(range(10_000))
def dname(role):
    i = next(_n)
    base = NAMES[i % len(NAMES)]
    return f"{base}{'' if i < len(NAMES) else ' ' + str(i // len(NAMES) + 1)} ({role})"

HOSTILE, NEUTRAL, FRIENDLY = -1, 0, 1
P = []  # (level, x, y, actor, name|None, hidden, disposition|None)
def add(lv, x, y, actor, name=None, hidden=False, disp=None):
    P.append((lv, x, y, actor, name, hidden, disp))

# ---------------- Command level ----------------
add("C", 350, 790, "dreck", "Dreck (X6, invisible, Grandolpha loyalist)", True, NEUTRAL)
add("C", 200, 640, "duergar", dname("X3 guard at arrow slit"))
for x, y in [(110, 500), (110, 540), (110, 580), (110, 620), (110, 660), (152, 460), (192, 460), (152, 705)]:
    add("C", x, y, "duergar", dname("X3 guard, bunk room"))
add("C", 745, 505, "grandolpha-muzgardt", "Grandolpha Muzgardt (X8)", disp=NEUTRAL)
add("C", 715, 530, "chardalyn-dragonet", "Chardalyn Dragonet (X8)", disp=NEUTRAL)
for x, y in [(565, 485), (565, 525), (600, 525)]:
    add("C", x, y, "duergar", dname("X8 cook, Grandolpha's bodyguard"), disp=NEUTRAL)
add("C", 905, 500, "intelligent-mimic", "Stone Trunk (X10, intelligent mimic)")
add("C", 1040, 585, "duergar", "Nildar Sunblight (X11)")
for x, y in [(850, 712), (850, 785), (995, 712), (995, 785)]:
    add("C", x, y, "animated-armor", "Suit of Armor (X12)")

# ---------------- Ice Gate level ----------------
add("I", 395, 702, "duergar", dname("X13 north door"))
add("I", 585, 800, "duergar", dname("X13 lever"))
add("I", 312, 705, "duergar-hammerer", "Duergar Hammerer (X13 west chamber)")
add("I", 312, 745, "duergar-hammerer", "Duergar Hammerer (X13 west chamber)")
add("I", 370, 610, "duergar", dname("X14 mechanic, invisible"), True)
add("I", 415, 610, "duergar", dname("X14 mechanic, invisible"), True)
add("I", 840, 800, "duergar", dname("X15 lever"))

# ---------------- Forge level ----------------
add("F", 440, 245, "umber-hulk", "Umber Hulk (X16, sacked and roped)")
for x, y in [(400, 230), (480, 230), (400, 290), (480, 290)]:
    add("F", x, y, "duergar", dname("X16 handler"))
for x, y in [(235, 520), (265, 640), (225, 745)]:
    add("F", x, y, "rust-monster", "Rust Monster (X17)")
for x, y in [(412, 445), (412, 490), (548, 445), (548, 490)]:
    add("F", x, y, "duergar", dname("X18 crossbow guard"))
add("F", 560, 600, "thonot-krob", "Thonot Krob (X19)")
add("F", 612, 560, "pleurota", "Pleurota (X19, one arm torn off)", disp=NEUTRAL)
for x, y in [(575, 545), (590, 640), (540, 640), (525, 585)]:
    add("F", x, y, "quaggoth-spore-servant", "Quaggoth Spore Servant (X19)")
for x, y in [(565, 722), (605, 722), (565, 775), (605, 775)]:
    add("F", x, y, "quaggoth", "Quaggoth (X20)")
for x, y in [(352, 728), (352, 772)]:
    add("F", x, y, "duergar", dname("X21 Grandolpha loyalist"), disp=NEUTRAL)
# X24-X26 forge cavern: repairs under way (homebrew), dragon on the assembly platform
add("F", 720, 540, "chardalyn-dragon", "Chardalyn Dragon (X25, under repair)")
add("F", 760, 600, "xardorok-sunblight", "Xardorok Sunblight (X25)")
add("F", 700, 650, "thontara", "Thontara (X25 forewoman)")
for x, y in [(650, 620), (655, 680), (785, 640), (785, 690), (650, 720), (790, 590)]:
    add("F", x, y, "quaggoth", "Quaggoth (X25 clean-up crew)")
for tx, ty in [(615, 290), (855, 290), (1060, 345), (1060, 500)]:
    for dx in (-25, 0, 25):
        add("F", tx + dx, ty, "duergar", dname("forge tower guard"))
for x, y in [(650, 165), (755, 165), (860, 165)]:
    add("F", x, y, "duergar-hammerer", "Duergar Hammerer (X28)")
add("F", 700, 145, "pekoe-quint", "Pekoe Quint (X28 cell)", disp=NEUTRAL)
add("F", 820, 145, "kapanuk-talltree-thuunlakalaga", "Kapanuk (X28 cell)", disp=NEUTRAL)
add("F", 900, 690, "fyorl", "F'yorl (X29, chained)", disp=NEUTRAL)
add("F", 858, 760, "duergar-hammerer", "Duergar Hammerer (X30)")
add("F", 985, 760, "klondorn", "Klondorn (X31, disguised)", disp=NEUTRAL)
for x, y in [(1190, 268), (1230, 268), (1270, 268), (1190, 300), (1230, 300), (1270, 300)]:
    add("F", x, y, "duergar", dname("X33 barracks"))
for x, y in [(1135, 215), (1175, 215), (1215, 215), (1255, 215), (1295, 215),
             (1120, 258), (1120, 298), (1370, 258), (1370, 298)]:
    add("F", x, y, "duergar", dname("X33 bunk room"))
add("F", 1165, 690, "nefrun", "Nefrun (X34, shackled, 7 HP)", disp=NEUTRAL)
add("F", 1138, 690, "duergar-mind-master", "Hooded Torturer (X34)")
add("F", 1192, 690, "duergar-mind-master", "Hooded Torturer (X34)")
add("F", 1390, 398, "duergar-hammerer", "Duergar Hammerer (X36 north alcove)")
add("F", 1440, 420, "duergar-hammerer", "Duergar Hammerer (X36 portcullis)")

PROTO_ONLY = ("randomImg", "appendNumber", "prependAdjective")
_actors = {}
def actor(slug):
    if slug not in _actors:
        with open(os.path.join(ACT, slug + ".json"), encoding="utf-8") as f:
            _actors[slug] = json.load(f)
    return _actors[slug]

def tokens_for(scene_id, code, level_ids, only=None):
    out, n = [], 0
    for lv, x, y, slug, name, hidden, disp in P:
        if only and lv != only:
            continue
        n += 1
        a = actor(slug)
        t = copy.deepcopy(a["prototypeToken"])
        for k in PROTO_ONLY:
            t.pop(k, None)
        w = t.get("width", 1)
        tid = f"Sb{code}{lv}Tok{n:09d}"
        t.update({
            "_id": tid, "_key": f"!scenes.tokens!{scene_id}.{tid}",
            "name": name or a["name"], "actorId": a["_id"], "actorLink": False,
            "x": PAD_X + round(x * S - w * GRID / 2), "y": PAD_Y + round(y * S - t.get("height", 1) * GRID / 2),
            "elevation": LEVELS[lv][2], "level": level_ids[lv], "hidden": hidden,
            "locked": False, "sort": n,
        })
        if disp is not None:
            t["disposition"] = disp
        out.append(t)
    return out

def level(lid, scene_id, code):
    name, slug, bottom, top = LEVELS[code]
    return {
        "_id": lid, "_key": f"!scenes.levels!{scene_id}.{lid}", "name": name,
        "background": {"color": "#000000", "src": IMG.format(slug), "tint": "#ffffff", "alphaThreshold": 0.75},
        "elevation": {"bottom": bottom, "top": top},
        "foreground": {"src": None, "tint": "#ffffff", "alphaThreshold": 0.75},
        "fog": {"src": None},
        "textures": {"anchorX": 0.5, "anchorY": 0.5, "offsetX": 0, "offsetY": 0, "fit": "fill",
                     "scaleX": 1, "scaleY": 1, "rotation": 0},
        "visibility": {"levels": []}, "sort": {"F": 0, "C": 1, "I": 2}[code], "flags": {},
    }

def dungeon(d):
    d.update({"width": W, "height": H, "padding": PAD, "tokenVision": True})
    d["grid"].update({"size": GRID, "distance": 5, "units": "ft"})
    d["fog"]["mode"] = 1
    d["environment"]["darknessLevel"] = 0.2      # braziers everywhere; globalLight stays on
    d["environment"]["globalLight"]["enabled"] = True
    return d

def write(fn, d):
    with open(os.path.join(SCN, fn), "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")

# The existing single-level Sunblight scenes are left untouched (Reed, 2026-11-11);
# one of them is read only as a format template.
with open(os.path.join(SCN, "scene-sunblight-command.json"), encoding="utf-8") as f:
    template = json.load(f)

# New scene: one scene, three levels
SID = "SunblightFortrs1"
LIDS = {"F": "SunblightLvForge", "C": "SunblightLvCmmnd", "I": "SunblightLvIceGt"}
d = copy.deepcopy(template)
d.update({"_id": SID, "_key": f"!scenes!{SID}", "name": "Sunblight Fortress (3 levels)",
          "navName": "Sunblight", "journal": JOURNAL, "journalEntryPage": None, "sort": 1,
          "initialLevel": LIDS["C"]})
d["levels"] = [level(LIDS[c], SID, c) for c in ("F", "C", "I")]
# 1.0.50: Reed places the NPCs by hand; the book positions stay in P for reference.
d["tokens"] = []
write("scene-sunblight-fortress.json", dungeon(d))

print(f"{len(P)} tokens:", {c: sum(1 for p in P if p[0] == c) for c in LEVELS})
