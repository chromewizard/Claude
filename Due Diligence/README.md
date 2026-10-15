# EnergyWave — Due Diligence (canonical source)

**Status:** Fifth iteration — every remaining deliverable drafted and the open facts marked in place. r5 adds ten rendered documents: the SAFE term summary; the Seed deck (16 slides, 16:9, in the Oct-13 deck's own system) and Seed one-pager; the Series A readiness outline; the Thread A characterization plan, the humanoid power-budget specification and the measurement-platform error budget; the DoW white paper v2.1 pass; the Safe Release Posture paper that supersedes the August 2025 "QVED" paper on EnergyWave letterhead; and the consolidated register of everything still waiting on an answer. Every open fact or decision is tagged in the document itself with the literal text `[Needs Input from Ian or Chip: …]` and listed once in `NEEDS_INPUT.md`. The ledger gains §F, the legacy QVE-era sources read from the Drive copy of the Mac collection (nothing from them is placed), and `90_Internal_Ops_NOT_FOR_CIRCULATION/` holds the consent requests, the counsel question set, the xTech verification checklist and the mirror instructions — drafts only; nothing is sent. r4–r4.2 history is in `MANIFEST.md`. Nothing here is released; every substantive item stays open until Ian answers it — silence is not approval.
**Package version:** `DD-2026-10-15-r5-draft`
**Point lead:** Claude · **Cross-check:** GPT (Lyra / Aura), Antigravity, Grok (Architect, Compliance) · **Authorizations:** Ian McLean

## What this is

One canonical source for three audiences — investors, the Department of War, and technical reviewers — built so that each fact appears once, every file is hash-verified, and every release is reproducible.

The September data rooms diverged: same-named ZIPs with 22 vs 24 files; standalone decks differing from their data-room copies. That is the failure mode this structure removes. A package is *assembled* from canonical files, and the manifest proves which bytes went where.

## Layout

| Folder / file | Audience | Holds in r5 |
|---|---|---|
| `EnergyWave_DD_Reading_Guide_2026-10-15.pdf` | Everyone — read first | How the package is organized, what is verified, what is open, and how to read the status tags. |
| `EnergyWave_Needs_Input_from_Ian_or_Chip_2026-10-15.pdf` · `NEEDS_INPUT.md` | Ian, Chip, counsel, reviewers | The consolidated register: every open fact and decision, who answers it, where the answer lands. Generated from the `[Needs Input from Ian or Chip: …]` tags. |
| `EnergyWave_Claims_Discipline_2026-10-15.pdf` | Everyone | The rules every document obeys — two-question filter, evidence labels, no device figures, publish both ways — and the recorded difference between the September charter and the Oct-13 deck (D10). |
| `01_Investor/01_Capital_Readiness/` | Investors — now | The Oct-13 deck and one-pager, unedited; the Terms and Objectives page; the SAFE Term Summary (every unset term tagged). $60,000 SAFE, 3 months, **"not a seed round"** — preserved as written (D1). |
| `01_Investor/02_Seed_Round/` | Investors — next | Seed Round Structure; the Seed Deck (16 slides) and Seed One-Pager — amount, tranche sizes and terms tagged, the model's stored figures labelled as placeholder outputs; the September Investor Overview as the historical ancestor. Separate folder permitted by Ian (D1). |
| `01_Investor/03_Series_A/` | Investors — later | Raise Model v1.1-corrected (one cell changed; every other part byte-identical to v1), its reading note, and the Series A Readiness Outline. Cap table and Series A deck not located (tagged). |
| `02_DoW/` | Department of War / defense | xTech Search 10 submission record (D7 partially closed, still time-critical); the paper as submitted and the approved replacement; Applicant and Eligibility Facts; Compartmentalization & Anti-Tamper Posture v0.1; the August DoD white paper v2.0 (historical) and its v2.1 DoW pass (draft, inputs tagged); the Safe Release Posture paper on EnergyWave letterhead, superseding the August 2025 "QVED" paper (which stays in the archive unedited). |
| `03_Technical_Documents/` | Technical reviewers | Research Program and Gates (threads A / B / C under one protocol; no dependency asserted); the Thread A Characterization Plan, the Humanoid Power Budget Specification and the Measurement Platform Error Budget (drafts; inventor-defined inputs tagged); Physical Architecture & Baseline Model v1.3; Technical Prospectus v1; five Oct-5 review and source notes; Key Research Facts (Sept). |
| `04_Legal_and_IP/` | Shared | Entity, IP and Legal Status — recorded facts; counsel's dated statements quoted from the original messages; agreements bearing on ownership; open items. |
| `05_Team/` | Shared | Team and Counsel — bios exactly as on the Oct-13 deck, with the verification status of every credential and every consent. |
| `90_Internal_Ops_NOT_FOR_CIRCULATION/` | Internal — Ian, Grok | Consent-request drafts (Story, Sarfatti, Crunkleton), the consolidated counsel question set, the xTech attachment-verification checklist (D7), the mirror instructions. Drafts and checklists only: nothing is sent, filed or published by the package; excluded from every audience build. |
| `99_Source_Archive/` | Internal | Pointers (not copies) to untouched originals and their hashes. |
| `src/` | Internal — build source | `pages/*.html`, `pages/_style.css` (portrait) and `pages/_slides.css` (16:9 deck), `assets/wordmark_blue.png` and `assets/wordmark_white_wave.png`, `render.js`: the exact source of every rendered document. Payload, hash-recorded. |
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
10. **One visual system.** New pages use the Oct-13 one-pager's system — Liberation Sans, blue rules and table heads, letter-spaced section labels, the wordmark on white — so they sit beside the approved originals without a seam. Every page carries a running header (document title · Confidential — Draft — For Discussion · version) and a footer (disclaimer · source pointer · page numbers); each document carries the masthead and status line on page 1, status tags (Original · Verified · Open · Historical · Draft) wherever a file or fact is characterized, and a "Sources:" block at the end citing ledger rows. Slide decks use the Oct-13 deck's own system (`_slides.css`: 16:9, near-black ground, navy cards, blue letter-spaced labels) with a footer line on every slide in place of the running header.
11. **Open items are tagged in place.** A fact or decision the package cannot settle is written into the document as the literal text `[Needs Input from Ian or Chip: …]` (or `[Needs Input from counsel via Ian: …]`), never as a blank or a guess, and appears once in `NEEDS_INPUT.md`. A tag that is not in the register is a finding.

## Release locations (proposed — pending Ian's approval of D9)

| Mirror | Location | Created by |
|---|---|---|
| Canonical | `chromewizard/Claude` · branch `claude/happy-knuth-yqtd41` · `Due Diligence/` | Claude |
| Mac | `/Users/ian/Desktop/Due Diligence/` (D9); the source collection at `/Users/ian/Documents/Projects/EnergyWave/` is untouched | Claude via Desktop Commander once the Mac is connected; otherwise Antigravity from the release ZIP + manifest |
| Google Drive | `Ian + Aura — Shared AI Workspace / Due Diligence /` (same sub-tree) | Claude creates the text-only skeleton through the Drive connector; binaries by Mac sync (mirror instructions), verified against the manifest |
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

- `NEEDS_INPUT.md` — the register: 33 items by owner, with T-1 (the xTech attachment, closes 19 Oct 21:00 UTC) first.
- `DECISIONS.md` — D1 resolved; D2, D3, D4, D8, D9, D10, D11 open; **D7 partially closed and still time-critical** (corrections 1–4 and 7 observed in the live profile on 14 Oct; the attachment's bytes and cover value unverified; competition closes 19 Oct 21:00 UTC).
- `SOURCE_LEDGER.md` — every source, where it is, its hash and status; §C maps the Mac inventory; §E maps each package file to its source bytes; §F records the legacy QVE-era sources (read, never placed).
- `REVIEW_PROTOCOL.md` — how GPT, Antigravity and Grok return findings.
- `MANIFEST.md` — what is in this release, byte for byte, and the control code in force.
