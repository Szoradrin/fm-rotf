# Rime of the Frostmaiden — HANDOFF
_Rime of the Frostmaiden · game session 25 · checkpoint 2026-11-04 · Agent: Sage · Track: Rime of the Frostmaiden_
_Loaded: AI-Ops 1.8 at `3aaeb7c` · fm-rotf at `06ae030` (release 1.0.47)_

## Read first
1. `CAMPAIGN-PLAN.md` (this folder) — Reed's current plan, saved verbatim. It wins over older notes.
2. `ROTF-STORY-STATE.yaml` (this folder) — the WHAT. Story, leveling plan, dragon route and rules.
3. `MODULE-STATE.yaml` (repo root) — the HOW. What's built, release history, outstanding work.
4. `party/*.md` (this folder) — full level-6 character sheets for all five PCs.
5. `callinl/ai-ops/handoffs/2026-10-23-local-ai-ops-desktop.md` — how module work is done now.

Work now runs in local Claude Code on the desktop (`D:\AI-Ops\Dev\Szoradrin\fm-rotf`). Hosted chat sessions can't write to GitHub.

This folder (`campaign/` in `Szoradrin/fm-rotf`) holds all Rime game files. It moved here from `callinl/ai-ops` on 2026-11-10. The release zip leaves it out, so none of it installs into Foundry.

## Where the game is
- **Oct 28:** the party went through Sunblight.
  - Happened: X4 flight plan found.
  - Did not happen: Xardorok killed, Pleurota freed (X19), red dragon heart destroyed (X24). A living Xardorok can repair the dragon.
- **Game session 25 (Nov 4):** the party fought the chardalyn dragon at Easthaven's gate and pulled it out of town. They got it under 100 HP and it fled back toward Sunblight.
- **Next:** the Easthaven aftermath, then the pursuit to Sunblight. Not recorded yet: the dragon's exact HP when it fled, and the damage to Easthaven.
- **Next game:** tomorrow, 2026-11-11 (Reed, 2026-11-10).
- **Not recorded:** what happened at Black Swords / Caer-Dineval (Crannoc, Hethyl, the Knights' alliance, how the party got the map). Reed to supply.

## The arc (Reed's plan, 2026-11-04; full text in `CAMPAIGN-PLAN.md`)
Battle at Easthaven -> dragon retreats to Sunblight -> party pursues and destroys it there -> heroes' welcome at Bryn Shander (the dragon never reaches it) -> Vellynne introduces Ythryn -> Arveiaturace appears as the cliffhanger, not automatically a fight -> on to Solstice, the Reghed Glacier and Ythryn.

Dragon route, timing and rules are in `ROTF-STORY-STATE.yaml` under `dragon_scourge`.

## Open DM decisions
- **Dragon's HP:** tuned to AC 18, HP 236 and it fled at under 100. The exact number is needed for the repair countdown.
- **Three towns:** the plan says three are devastated; the book's route has only Dougan's Hole and Good Mead before Easthaven.
- **Vellynne:** Reed's earlier note had the party on her dogsleds; the plan introduces her after the dragon is destroyed.
- **Vistel:** the plan's name for the Enclave character. These files have Rhystal; assumed the same character until confirmed.
- **Enclave contact:** Session 7 notes say Bal; the sheet and later docs say Talen Stonebrook, a name Sage invented.
- **Level-up:** the book's Sunblight level-up (any 2 of X4 plan / free Pleurota / destroy the heart) versus level 7 when the dragon is destroyed. The party has 1 of the 3. The new plan doesn't state a level.
- **Xardorok:** recorded as alive after Oct 28; the plan lists his status to determine for next session.
- Carried over: Sahnar's actor design.

## Table assets (made by Reed, not in the module)
- **Cinematics** (ChatGPT stills plus Gemini 10-second videos): the dragon launching from Sunblight's summit doors; the dragon attacking Dougan's Hole.
- **Gemini lesson:** start a fresh chat with a first-frame image plus a separate character-reference image, ONE continuous shot, explicit scale, and say what the beam hits.
- **Sahnar** (the Elven Tomb mummy) is now the barkeep at the Ramshackle (player request). Portrait and animation done; actor/design still to finalize.
- **Rhystal** (player): photoreal portrait done. Dragonborn, remorhaz-chitin breastplate, slim kite shield, bullwhip.
- **Sunblight maps:** split into 3 labeled level images, set by Reed in the scenes by hand (details in `MODULE-STATE.yaml`).

## Tracks (planned after the game; do NOT restructure tonight)
- Rename to "Launch Foundry Module" (the HOW) and "Launch Foundry Game <name>" (the WHAT).
- Shared `tracks/ref_foundry-game-base.yaml`, plus `ref_foundry-game-rime.yaml` (continues the Rime session count) and a stub `ref_foundry-game-shadow-king.yaml` for Reed's homebrew "Legacy of the Shadow King" (source still being written: Gemini research, dictation to ChatGPT, ChatGPT images, Claude writes the canon).
- Old launch names stay as aliases. Reed will give the full restructure prompt separately. Manifest changes need "climax".
- Rule conflict for that work: both Foundry track manifests still say never keep a local repo copy; Bootstrap 1.8 allows copies under `D:\AI-Ops\Dev`.

## Open items
- **Module compatibility:** bump `compatibility.verified` to 14.369 in the next release (Reed chose after the game).
- **Token art:** audited 2026-11-05 (full list in `MODULE-STATE.yaml`). Of the 19 Sunblight actors, only Xardorok and Grandolpha have their own token; Kapanuk has a generic one, Klondorn has book art, and 15 are placeholders. The 16 prompts aren't saved in `D:\AI-Ops`, and no images have been uploaded. Nine actors have a token file in the module that isn't wired in yet (Vellynne, Nass, Dzaan's simulacrum, Icewind kobold, Arveiaturace, Bjornhild, three Auril forms).
- Reed DM decisions carried over: Yajath charm/sneak; Hethyl's 4th prophecy; Dinev's Rest. These may already be settled by play; see "Not recorded" above.
- STANDARDS-SCENES update pending.
- Campaign files now live in this public repo by Reed's choice (2026-11-10: players don't read the repo), so the old campaign block in git history doesn't need scrubbing.
- Confirm Rurik's actual level at the table.
- Jira ROTF: 25 open tickets, all Backlog, none updated since Aug 12; several are out of date (for example ROTF-28). Reconcile when Reed wants it.

## Prep done for game session 25
- Module release 1.0.48: four gridless Easthaven battle scenes (Reed sets grid and lighting by hand) and the `duergar.json` HP fix (`4d8+8`).
- Chapter 4 read on D&D Beyond 2026-11-04; route, timing and rules match Reed's notes.
- Not done: Dragon Scourge journal, town scene shells, dragon actor rebuild. Reed tuned the dragon in the compendium.

## Standing rules
- **Game sessions are not Claude Code sessions.** Session numbers count game sessions, and one game session can span several Claude Code sessions. Older `S` numbers in these files (S23, S24, S25) were counted per work session, so don't read them as game sessions.
- Foundry v14 only, D&D 5.5e (2024) by default; exceptions only when Reed names them.
- RAW content from D&D Beyond, never memory. Read the book before explaining plot or building stat blocks.
- Actors built on TRAZZM exemplar chassis (`Szoradrin/fm-template/exemplars/trazzm`) or the compact generator pattern used for 1.0.47.
- Compile via `tools/build.py` only (GitHub Actions "Build packs" on push to main touching `packs-src/**`). Release tags plain semver, no `v` prefix. One release per batch.
- Scrub every stale ID after copying an exemplar (nested effect `_key`s, prototypeToken, folder, `flags.core.originText`).
- Scenes are empty shells; Reed places maps manually.
- Campaign files (spoilers, party state, table plans) live in `campaign/` in this repo. Keep `./campaign/*` in `.github/zip-exclude.lst` so they never ship in the module.
- **Stay in this project.** Rime work changes only this repo. Never touch `callinl/ai-ops` or any other project unless Reed explicitly says to. Rime work is logged here (`GAME-SESSIONS.md`, this handoff, the `MODULE-STATE.yaml` changelog), not in the PC's AI-Ops logs.

## Load record (Claude Code session of 2026-11-04)
| Source | Kind | Status |
|---|---|---|
| `BOOTSTRAP.md`, `ref_RELEASE.yaml`, `ref_change-management.md`, `ref_principles.md`, `ref_connections.md`, `ref_knowledge-architecture.md`, `ref_session-management.md` at `3aaeb7c` | principle | loaded |
| `profiles/ref_sage.md`, `profiles/ref_reed.md` | profile | loaded; Sage assumed from track history |
| `tracks/ref_rime-of-the-frostmaiden.yaml` | track | loaded |
| `personas/creative-game-master.md`, `personas/engineering-foundry-vtt-developer.md` | persona | loaded |
| `skills/creative/INDEX.md`, `narrative-and-worldbuilding.md`, `skills/engineering/INDEX.md`, `system-design.md` | skill | loaded |
| Story state, campaign state, party sheets, S23 run sheet | project | loaded |
| `Szoradrin/fm-rotf/MODULE-STATE.yaml` at `06ae030` | project | loaded |
| `Szoradrin/fm-template` standards and TRAZZM exemplars | project | not yet; load before building |
| D&D Beyond Chapter 4 | source | not yet; read before writing plot |
| `docs/how/ref_operating-model.md` | principle | not loaded; not needed so far |
