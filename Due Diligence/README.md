# EnergyWave — Due Diligence (canonical source)

**Status:** Second iteration — controls corrected after GPT/Lyra's r1 audit; ledger reconciled to the 255-file Mac inventory; decisions updated. Nothing here is released.
**Package version:** `DD-2026-10-14-r2-draft`
**Point lead:** Claude · **Cross-check:** GPT (Lyra / Aura), Antigravity, Grok (Architect, Compliance) · **Authorizations:** Ian McLean

## What this is

One canonical source for three audiences — investors, the Department of War, and technical reviewers — built so that each fact appears once, every file is hash-verified, and every release is reproducible.

The September data rooms diverged: same-named ZIPs with 22 vs 24 files; standalone decks differing from their data-room copies. That is the failure mode this structure removes. A package is *assembled* from canonical files, and the manifest proves which bytes went where.

## Layout

| Folder | Audience | Holds |
|---|---|---|
| `01_Investor/01_Capital_Readiness/` | Investors — now | The $60,000 / 3-month SAFE bridge: deck, one-pager (full and redacted), SAFE summary, use of funds, objectives. The materials say **"Not a seed round"** and stay that way (D1). |
| `01_Investor/02_Seed_Round/` | Investors — next | The round the bridge is designed to reach. Separate folder permitted by Ian; amounts and terms unsettled. |
| `01_Investor/03_Series_A/` | Investors — later | Raise Model (corrected copy, ancestry recorded), cap table, Series A deck. |
| `02_DoW/` | Department of War / defense | xTech Search 10 — the submission as it stands, with its hash; Compartmentalization & Anti-Tamper posture; the DoD white paper; applicant and eligibility facts; GovThink / 501(c)(3). |
| `03_Technical_Documents/` | Technical reviewers | Physical architecture & baseline model, reviews, source notes, the energy-conservation gate protocol, humanoid power budget. |
| `04_Legal_and_IP/` | Shared | Recorded filing facts, counsel communications (originals, not summaries), formation evidence, IP agreements bearing on ownership. |
| `05_Team/` | Shared | Bios exactly as on the Oct-13 deck, with the verification status of every credential and every named-role consent. |
| `99_Source_Archive/` | Internal | Pointers (not copies) to untouched originals and their hashes. |
| `tools/` | Internal | `lint.py` (forbidden-label scan, fail-closed), `build_manifest.py` (author only), `verify_manifest.py` (reviewers and mirrors), `tests/run_probes.py`. |

Shared material (team, legal, technical) lives once and is pulled into the Investor and DoW packages at build time. No hand-copied duplicates.

## Rules

1. **One canonical file.** If two packages need it, they reference the same file; the build copies it and records the hash.
2. **Every release has a manifest.** `manifest.json` and `MANIFEST.md`, regenerated only by the author with `tools/build_manifest.py`. A file not in the manifest is not in the release. The manifest also records the digests of the control code in force.
3. **Claims discipline is the asset.** No document says a device exists, works, or will work. The two-question filter — *what is the net energy source, and where is the colder sink?* — applies to every sentence. Every number is labelled by origin: assumption · calculation · proposed target · company measurement · attributed published result. Adjacent science stays separate from claims of continuous net extraction.
4. **Forbidden label.** No file may contain the label defined in `tools/lint.py` — in any form: name, handle, path, email, metadata, spreadsheet cell, archive member name. The scan fails closed: a match blocks the build, and so does any surface it could not read. The founder is **Ian McLean** (Ian Franklin McLean on legal records).
5. **Names and contacts.** Department of War → **DoW** in new documents; "DoD" only in historical titles and regulatory citations. New documents use the contact Ian designates for them; historical and submitted records are quoted exactly as they stand and are never normalized.
6. **Sources before conclusions.** A reviewer's summary of counsel, a portal, or a registry is cited as a summary. Only the original communication or record supports a statement of what counsel said, what was filed, or what was submitted.
7. **Dates and versions.** `EnergyWave_<Name>_YYYY-MM-DD.ext` for deliverables; `YYYY-MM-DD_<topic>_<author>_vN.md` for working notes (Council convention). Corrected copies carry their ancestry in `SOURCE_LEDGER.md` and never take a version number that a missing historical file already holds.
8. **Originals are never edited.** A correction produces a new dated file; the original stays, hash-recorded, in its source location.

## Release locations (proposed — pending Ian's approval of D9)

| Mirror | Location | Created by |
|---|---|---|
| Canonical | `chromewizard/Claude` · branch `claude/happy-knuth-yqtd41` · `Due Diligence/` | Claude |
| Mac | `/Users/ian/Desktop/Due Diligence/` (D9); the source collection at `/Users/ian/Documents/Projects/EnergyWave/` is untouched | Claude via Desktop Commander once the Mac is connected; otherwise Antigravity from the release ZIP + manifest |
| Google Drive | `Ian + Aura — Shared AI Workspace / Due Diligence /` (same sub-tree) | Claude via the Drive connector |
| Claude Project | *EnergyWave Ops* — release ZIP + manifest uploaded; this repo linked | Ian (project-knowledge upload) |

The repository is the only verified release location today. A mirror becomes verified only when `tools/verify_manifest.py` passes against the pinned manifest hash from the handoff.

## Build (author) and verify (everyone else)

```bash
cd "Due Diligence"
python3 tools/tests/run_probes.py                   # regression probes for the scanner (19 cases)
python3 tools/lint.py --root .                      # exit 0 OK · 1 match · 2 unscanned surface
python3 tools/build_manifest.py                     # AUTHOR ONLY — regenerates manifest.json / MANIFEST.md

# Reviewer or mirror: never rebuild; verify against the pinned manifest
python3 tools/verify_manifest.py --manifest /trusted/manifest.json --root /path/to/mirror \
        --expect-manifest-sha256 <hash from the handoff>
python3 tools/lint.py --root /path/to/any/collection --json report.json   # e.g. the Mac collection
```

## Read next

- `DECISIONS.md` — D1 resolved; D2–D4, D7 (time-critical), D9 open.
- `SOURCE_LEDGER.md` — every source, where it is, its hash and status; §C maps the Mac inventory.
- `REVIEW_PROTOCOL.md` — how GPT, Antigravity and Grok return findings.
- `MANIFEST.md` — what is in this release, byte for byte, and the control code in force.
