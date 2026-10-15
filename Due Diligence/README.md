# EnergyWave — Due Diligence (canonical source)

**Status:** Fourth iteration — the first audience draft, reconciled to GPT/Lyra's r3 audit (0 blockers; every finding dispositioned in `MANIFEST.md`); r4.1 adds a ledger addendum only, recording Antigravity's independent r3 review and the Mac-wide source scan (S-32, M-21) with no page content changed; r4.2 records the co-founder's name as he uses it, Chip Story, and sources his degrees and ZPEPG role to ZPEPG's public leaders page and his LinkedIn profile (S-33, S-34), on the Team page and in D4. Ten pages rendered in the approved Oct-13 visual system; eight originals placed byte-for-byte, including the xTech paper as submitted and its approved replacement; five Oct-5 technical notes placed from exact Drive bytes; the Raise Model placed as a corrected copy with its saved results intact and its ancestry recorded. Nothing here is released; every substantive item in `DECISIONS.md` stays open until Ian answers it — silence is not approval.
**Package version:** `DD-2026-10-15-r4.2-draft`
**Point lead:** Claude · **Cross-check:** GPT (Lyra / Aura), Antigravity, Grok (Architect, Compliance) · **Authorizations:** Ian McLean

## What this is

One canonical source for three audiences — investors, the Department of War, and technical reviewers — built so that each fact appears once, every file is hash-verified, and every release is reproducible.

The September data rooms diverged: same-named ZIPs with 22 vs 24 files; standalone decks differing from their data-room copies. That is the failure mode this structure removes. A package is *assembled* from canonical files, and the manifest proves which bytes went where.

## Layout

| Folder / file | Audience | Holds in r3 |
|---|---|---|
| `EnergyWave_DD_Reading_Guide_2026-10-15.pdf` | Everyone — read first | How the package is organized, what is verified, what is open, and how to read the status tags. |
| `EnergyWave_Claims_Discipline_2026-10-15.pdf` | Everyone | The rules every document obeys — two-question filter, evidence labels, no device figures, publish both ways — and the recorded difference between the September charter and the Oct-13 deck (D10). |
| `01_Investor/01_Capital_Readiness/` | Investors — now | The Oct-13 deck and one-pager, unedited; the Terms and Objectives page. $60,000 SAFE, 3 months, **"not a seed round"** — preserved as written (D1). |
| `01_Investor/02_Seed_Round/` | Investors — next | Seed Round Structure (DRAFT: gates and tranches; amount and terms open); the September Investor Overview as its historical ancestor. Separate folder permitted by Ian (D1). |
| `01_Investor/03_Series_A/` | Investors — later | Raise Model v1.1-corrected (one cell changed; every other part byte-identical to v1) and its reading note. Cap table and Series A deck not located. |
| `02_DoW/` | Department of War / defense | xTech Search 10 submission record (9 Oct record; 14 Oct read-only portal observation; D7 partially closed, still time-critical); the paper as submitted and the approved replacement; Applicant and Eligibility Facts; Compartmentalization & Anti-Tamper Posture v0.1; the August DoD white paper v2.0. |
| `03_Technical_Documents/` | Technical reviewers | Research Program and Gates (threads A / B / C under one protocol; no dependency asserted); Physical Architecture & Baseline Model v1.3; Technical Prospectus v1; five Oct-5 review and source notes; Key Research Facts (Sept). |
| `04_Legal_and_IP/` | Shared | Entity, IP and Legal Status — recorded facts; counsel's dated statements quoted from the original messages; agreements bearing on ownership; open items. |
| `05_Team/` | Shared | Team and Counsel — bios exactly as on the Oct-13 deck, with the verification status of every credential and every consent. |
| `99_Source_Archive/` | Internal | Pointers (not copies) to untouched originals and their hashes. |
| `src/` | Internal — build source | `pages/*.html`, `pages/_style.css`, `assets/wordmark_blue.png`, `render.js`: the exact source of every rendered page. Payload, hash-recorded. |
| `tools/` | Internal — controls | `lint.py` (forbidden-label scan, fail-closed) · `build_manifest.py` (author only) · `verify_manifest.py` (reviewers and mirrors) · `tests/run_probes.py` (31 probes) · `lint.sh`. The only five files excluded from the payload; anything else inside `tools/` is scanned, and the builder refuses it. All three tools also ignore the two manifest files at the root and Finder metadata (`.DS_Store`) at any depth. |

Shared material (team, legal, technical) lives once and is pulled into the Investor and DoW packages at build time. No hand-copied duplicates.

## Rules

1. **One canonical file.** If two packages need it, they reference the same file; the build copies it and records the hash.
2. **Every release has a manifest.** `manifest.json` and `MANIFEST.md`, regenerated only by the author with `tools/build_manifest.py`. A file not in the manifest is not in the release. The manifest also records the digests of the control code in force.
3. **Claims discipline is the asset.** No document says a device exists, works, or will work. The two-question filter — *what is the net energy source, and where is the colder sink?* — applies to every sentence. Every number is labelled by origin: assumption · calculation · proposed target · company measurement · attributed published result. Adjacent science stays separate from claims of continuous net extraction.
4. **Forbidden label.** No file may contain the label defined in `tools/lint.py` — in any form: name, handle, path, email, metadata, spreadsheet cell, archive member name. The scan fails closed: a match blocks the build, and so does any surface it could not read. The founder is **Ian McLean** (Ian Franklin McLean on legal records). The Mac source collection was scanned read-only on 14 Oct (ledger M-21): the label occurs there only in four third-party pronunciation dictionaries and one archived chat log, none of which feeds a package file; 13,332 image surfaces outside the substantive folders remain unreviewed, so that scan supports "no text or metadata match in the substantive folders", not "clean".
5. **Names and contacts.** Department of War → **DoW** in new documents; "DoD" only in historical titles, in a portal's own field names when quoted, and in regulatory citations. New documents use the contact Ian designates for them; historical and submitted records are quoted exactly as they stand and are never normalized.
6. **Sources before conclusions.** A reviewer's summary of counsel, a portal, or a registry is cited as a summary. Only the original communication or record supports a statement of what counsel said, what was filed, or what was submitted.
7. **Dates and versions.** `EnergyWave_<Name>_YYYY-MM-DD.ext` for deliverables; `YYYY-MM-DD_<topic>_<author>_vN.md` for working notes (Council convention). Corrected copies carry their ancestry in `SOURCE_LEDGER.md` and never take a version number that a missing historical file already holds.
8. **Originals are never edited.** A correction produces a new dated file; the original stays, hash-recorded, in its source location.
9. **Rendered pages are never edited as PDFs.** Every `EnergyWave_<Name>_2026-10-15.pdf` is generated from `src/pages/<nn>_<Name>.html` by `src/render.js`. A wording fix is made in the HTML and the page re-rendered; the PDF and its source are both in the manifest.
10. **One visual system.** New pages use the Oct-13 one-pager's system — Liberation Sans, blue rules and table heads, letter-spaced section labels, the wordmark on white — so they sit beside the approved originals without a seam. Every page carries a running header (document title · Confidential — Draft — For Discussion · version) and a footer (disclaimer · source pointer · page numbers); each document carries the masthead and status line on page 1, status tags (Original · Verified · Open · Historical · Draft) wherever a file or fact is characterized, and a "Sources:" block at the end citing ledger rows.

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
python3 tools/tests/run_probes.py                   # 31 regression probes: scanner, verifier, builder, shared control policy
python3 tools/lint.py --root .                      # exit 0 OK · 1 match · 2 unscanned surface
node src/render.js                                  # AUTHOR ONLY — re-renders src/pages/*.html to the paths in their dd-output meta
python3 tools/build_manifest.py                     # AUTHOR ONLY — regenerates manifest.json / MANIFEST.md

# Reviewer or mirror: never rebuild; verify against the pinned manifest
python3 tools/verify_manifest.py --manifest /trusted/manifest.json --root /path/to/mirror \
        --expect-manifest-sha256 <hash from the handoff>
python3 tools/lint.py --root /path/to/any/collection --json report.json   # e.g. the Mac collection
```

`render.js` needs Node 18+, the `playwright` package and a Chromium build (path set in the file). Rendering is deterministic in content, not in bytes: a re-render on another Chromium build can hash differently, which is why the manifest — not a re-render — is the reference.

## Read next

- `DECISIONS.md` — D1 resolved; D2, D3, D4, D8, D9, D10 open; **D7 partially closed and still time-critical** (corrections 1–4 and 7 observed in the live profile on 14 Oct; the attachment's bytes and cover value unverified; competition closes 19 Oct 21:00 UTC).
- `SOURCE_LEDGER.md` — every source, where it is, its hash and status; §C maps the Mac inventory; §E maps each package file to its source bytes.
- `REVIEW_PROTOCOL.md` — how GPT, Antigravity and Grok return findings.
- `MANIFEST.md` — what is in this release, byte for byte, and the control code in force.
