# fm-rotf

Foundry VTT module for Reed's Icewind Dale: Rime of the Frostmaiden game (module ID `rotf`, Foundry v14, dnd5e).
Install in Foundry with the manifest URL: `https://github.com/Szoradrin/fm-rotf/releases/latest/download/module.json`

## What's where

**Ships to Foundry** (inside the release zip):

| Path | What it is |
|---|---|
| `module.json` | Module manifest. The release workflow fills in the version and download links. |
| `packs/` | Compiled compendium packs: actors, journals, scenes, tables, items. Built from `packs-src/`; don't edit by hand. |
| `assets/images/` | Art (`art-`), tokens (`token-`), maps (`map-`) and handouts (`handout-`). |

**Builds the module** (not in the zip):

| Path | What it is |
|---|---|
| `packs-src/` | Source JSON, one file per document. Edit here. |
| `tools/build.py` | Compiles `packs-src/` into `packs/` behind 8 checks. Runs in GitHub Actions on every push to `main` that touches `packs-src/`. |
| `.github/` | Workflows ("Build packs" on push, "Release Module" on a published release) and `zip-exclude.lst`, the list of paths kept out of the zip. |
| `package.json`, `package-lock.json` | The Foundry CLI the build uses. `node_modules/` is installed by npm and not stored in git. |
| `MODULE-STATE.yaml` | What's built, release history, outstanding work. |
| `docs/` | Build plans and notes (Cult of Auril journal plan, an old image manifest). |
| `reference/` | Reference images for planning only, never used in the module. |
| `archive/` | Retired source files kept for reference. |

**The game table** (not in the zip):

| Path | What it is |
|---|---|
| `campaign/` | Reed's campaign: what happened each session, party sheets, story state, plans and run sheets. Start with `campaign/HANDOFF.md`. |

## Rules
- Anything new that must not install into Foundry needs a line in `.github/zip-exclude.lst`.
- Release tags are plain semver (`1.0.48`), never `v1.0.48`.
