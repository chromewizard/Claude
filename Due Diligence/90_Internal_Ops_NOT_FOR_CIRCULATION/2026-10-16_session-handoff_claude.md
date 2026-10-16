# Session handoff — Claude (point lead) to the next Claude instance — 16 October 2026

**Why this exists.** The founder asked for a handoff document before restarting his computer and the lead's session (16 Oct 2026, direct: “Let's restart another instance so if you can give me a handoff doc … Please update the Series A accordingly. Restarting.”). A new instance reads this file first, then `README.md`, `NEEDS_INPUT.md`, `DECISIONS.md`, `SOURCE_LEDGER.md` and `MANIFEST.md`, and continues without re-deriving the state. Nothing in this file is a new fact; every statement is traceable to a ledger row or a commit. Internal — not for circulation; excluded from every audience build; covered by the manifest and the forbidden-label scan like every other file in this folder.

## 1. Where the work is

| Item | Exact value |
|---|---|
| Canonical source | GitHub `chromewizard/Claude`, branch `claude/happy-knuth-yqtd41`, folder `Due Diligence/`. The only verified release location; mirrors verify against the pinned manifest. |
| Installed release | **r5.7** — commit `dad1419d1cb7cd6ff38778c5ff3cc35f1c5e8c07`, `manifest.json` SHA-256 `9c2dc08f48298ba3ac3b27240f9d783becd513acfcd1c8a28099e0083e3b3db8` (84 payload files, 21 rendered documents, 31 probes, lint OK). Installed by GPT/Lyra on 15–16 Oct (ledger S-54): canonical bytes under `/Users/ian/Documents/EnergyWave Final/Review Records/r5.7 Review Candidate/Due Diligence/`, matched on OneDrive and My Drive; 45 audience copies in the nine audience folders; outer collection manifest `13e3395c…`; 657 files / 137 directories. |
| Earlier pins | r5.6 `a6999f0ab43a6d37c4c3deaa8ad25e15ac189962` / `0960cf3f348a2755ae7203de00c02d7887eb57c76ccaada65835d3b8dc641e32`; r5.5 `5a9fcfdc…` / `8d07718a…`. |
| Working commits after r5.7 (not releases) | `c9edf2915f4ff8c344a9709ef0b1829d273470c0`, `183e69e0c53dc5bc3805c507532a80ce11ce0ddd`, `998681ea4db755a8ae1a7753d9e23e434bb6472b`, `e0d7ef0087edb60d9edabeb6bfc978ea642b0984`, then this session's 16 Oct commits (this handoff; the Alan/Jack confirmation, S-56; the Raise Model v1.2 derivative and the Series A update, S-57). `manifest.json` is rebuilt only at a pin. |
| Next pin | **r6** — version string `DD-2026-10-16-r6-draft` (r5.8 `DD-2026-10-15-r5.8-draft` was pinned at commit `b7230c47c7f092fc7214114250c2b825f541c445`, manifest `52945aed3f78aad36d63165f50cec8960a1d8cfd34290dc3c14e8a42bf742550`). The exact commit and `manifest.json` SHA-256 are reported to GPT/Lyra in the session at the moment of the pin (they cannot be written into the payload before it exists); afterwards they appear in `MANIFEST.md` (generated block) and `git log`. |
| Drive — Founder Decisions folder | `1A1C6kGZJa4Fh8YJP4QWd2Em86RkXXZO_` (GPT's handoff files, S-44/S-45; `ALAN_JACK_ROLE_CONFIRMATION.md` `1WdZyc5sk_M1I2JMGsxZgzWpx18zMyB3-`, S-46). |
| Drive — review records | Lyra r5.6 bundle `12PO6yCShu9N1gXFyzbtiK_oYszuAS5bH` (S-48); Antigravity r5.6 report `1Xpou503pcXEEfz1NstIKqJIMjMmWN9EP` (S-49) and GPT/Lyra's addendum `1Jo9eembfo-oDcgYusTZ10RbdLfkdYgAo` (S-50); Lyra r5.7 acceptance `1dlYAQcC_GA-KW_mF6JOMbv6D8hcXbTH4` (S-51); email review status `1p3nis3LApaYgc-andoMxwrdfKy8PBOcU` (S-52); Chip-draft Architect addendum `1o3MSIDWpCaPibeBf0rByFabgHEAPjJV3` (S-53/S-54). The Drive connector's `read_file_content` returns the text of these files. |
| Mac | Not reachable from the lead's session (Desktop Commander lists no device). Nothing on the Mac is read until it is placed in the Drive Founder Decisions folder or the My Mac / EnergyWave folder. |
| Build source in the repo | `src/pages/*.html` (21 pages) + `src/pages/_style.css` / `_slides.css` + `src/render.js`; **`src/build/`** (added 16 Oct) holds `gen_register.py` (generates the Open Items Register page and `NEEDS_INPUT.md` from the markers), `conv.py` (the single-pass orange-[TBD] converter) and `pp.py` (path helpers). Controls in `tools/` (five files only; the builder refuses anything else there). |

## 2. The people and the channels

- **Ian McLean** — founder (Ian Franklin McLean on legal records); the only authorization. Writes in the lead's session directly (his messages arrive with doubled letters when relayed through the council mechanism — a keyboard/relay artifact he finds “silly”; read through it, never quote the doubled form). His workspace handle contains the forbidden label and is never written anywhere.
- **GPT (Lyra / Aura)** — reconciliation, audience assembly and every mirror write; delta-checks each pin; relays the founder's decisions as dated Drive files or as quoted messages in the session. Owns the nine audience folders and the collection's `FILE_MANIFEST.json`.
- **Antigravity** — independent review of pinned releases; hashes; the Mac-side verifier when connected.
- **Grok (Architect, Compliance)** — per-email review of every held draft before any send; a verdict is never send authority.
- **Gemini / Argon** — cross-check reviewer when invoked.
- **Chip Story** — Co-Founder, “cofounder Physicist” by the founder's designation (S-47). **Jack Sarfatti** — team member, theoretical physicist. **Alan Crunkleton** — advisor. **Mike Wentz** — team member by the founder's direction of 16 Oct (S-55), title [TBD]. **Arath Acosta** — proposed Design Engineer from Seed, a planned role. **K&L Gates LLP** (Novak, Majewski) — patent counsel, handling the entity work.

## 3. Standing rules — the ones that bite

1. **The forbidden label** (defined in `tools/lint.py`) never appears in any file, name, path, metadata or spreadsheet cell; the scan fails closed and blocks the build. The founder's instruction of 14 Oct about it was emphatic; the documents refer to it only as “the label defined in tools/lint.py”.
2. **Originals are never edited.** A correction is a new dated file; the pinned workbook `EnergyWave_Raise_Model_v1.1-corrected_2026-10-15.xlsx` is never touched — changes go into a dated derivative (v1.2 is the first).
3. **No assistant sends, files, publishes or edits a portal.** No email from any assistant account; no outreach to anyone; drafts in this folder are held until Ian sends them himself from ian@energywave.ai. No outreach to Alan or Jack (their willingness and roles are confirmed by the founder's own outreach, S-56 — do not ask again, do not send a consent request).
4. **Silence never closes a substantive item.** Counsel is quoted only from the originals. Every number is labelled by origin. No device performance claim anywhere.
5. **No new questions to the founder** (“no more questions”, 15 Oct). An unresolved field is the exact bracketed **[TBD]** in orange ink followed by the field (`<span class="need"><b>[TBD]</b> — field</span>`; markdown `[TBD] — field`); an item owed by counsel or a named person is `[Pending: …]`. Every marker appears once in `NEEDS_INPUT.md`; a marker that is not there is a finding. Historical “TBD” wording (the xTech record's cover fields, the checklist) and the founder's quoted instruction stay verbatim.
6. **One canonical master; one writer at a time.** GPT/Lyra installs a pin only after its own delta check; reviewers do not authorize installation.
7. **Reviewer disagreements are recorded, not averaged** (see the Antigravity disposition in `MANIFEST.md`).
8. **Commits** are made as `Claude <noreply@anthropic.com>`; no model identifier is written into any repository artifact.

## 4. What this session did on 16 October (after r5.7)

1. Antigravity's r5.6 review dispositioned with GPT/Lyra's addendum (S-49, S-50); Lyra's r5.7 acceptance recorded (S-51).
2. The held counsel question set corrected per Grok Architect (S-52: items 5, 9, 11, 13; internal footer marked for removal) — not sent.
3. The held Chip consent request corrected per Grok Architect after Ian approved sharing it (S-53: eight points, then two further wording checks) — not sent.
4. r5.7 installation receipt recorded (S-54).
5. The founder's direct messages recorded (S-55): Mike Wentz on the team; a draft on his Mac not yet retrieved; his question why Chip's workbook row is $150,000 1099 rather than $500,000 W-2; his remark on the council review mechanism.
6. **This handoff written; the register generator moved into `src/build/`.**
7. **Alan and Jack (S-56):** the founder confirmed, through GPT/Lyra, that his own outreach has happened and both accepted their positions as stated — Alan advisor, Jack team member. Recorded on the Team page, deck, one-pager, DoW v2.1 §6, Safe Release §8, D4, the register and the two held drafts (now overtaken for role consent; preserved unsent). No signed instrument; no compensation, IP or employment terms.
8. **Series A updated (S-57):** `01_Investor/03_Series_A/EnergyWave_Raise_Model_v1.2_2026-10-16.xlsx` — a derivative of v1.1-corrected with Chip Story's row H02 at $500,000 W-2 (payroll load applied) as the founder directed, a Mike Wentz note row (not modeled — no figure invented), a change record on the README sheet, and every formula recalculated in LibreOffice headless; v1.1-corrected untouched. The Raise Model Note, the Series A Readiness Outline, the deck (slides 8–9), the one-pager, the folder README, the delivery map and the register carry the v1.2 figures beside the v1.1 historical ones, each labelled by origin. The interpretation applied — Chip's $500k modeled in addition to the two unnamed $500k physicist agreements (H08–H09), time commitment [TBD] — is stated on every page that shows a v1.2 figure.
9. **r5.8 pinned** (version bump on every page, all 21 documents re-rendered, probes, lint, manifest, fresh-mirror verification) and the pin handed to GPT/Lyra for the delta check.

## 5. What is open — read `NEEDS_INPUT.md`; the short version

- **T-1 (time-critical, the founder's action):** verify the xTech Search 10 portal attachment (artifact 262231) before **Monday 19 Oct 2026, 21:00 UTC**: download, hash (expected `90823d62…fea1`, 123,643 bytes), cover reads ≈ USD 10,000, no private-review banner, no blank cover fields; re-upload the approved replacement if not. Checklist: `2026-10-15_xtech-attachment-verification_checklist.md` in this folder. The founder asked “what do I need for the attachment” — the answer is that checklist; nothing else is needed from the package.
- **The founder's unretrieved draft** on his Mac (S-55): read only when placed in Drive.
- **Held drafts** (Chip; counsel): corrected, not re-reviewed since, not sent. Alan's and Jack's: overtaken for role consent (S-56); unsent.
- **[TBD] fields** by document (register §B) and **pending** items from counsel or named persons (§C) — none is asked of the founder.
- **Reviewers:** GPT/Lyra delta-checks r5.8; Antigravity's review of r5.7/r5.8; Grok re-reviews a draft only if and when the founder authorizes a send.

## 6. How to build and pin (author only)

```bash
cd "Due Diligence"
python3 src/build/gen_register.py                     # regenerate the register page + NEEDS_INPUT.md after any marker change
node src/render.js [name-fragment …]                 # re-render changed pages (no argument = all 21)
python3 tools/tests/run_probes.py                    # 31 probes
python3 tools/lint.py --root . --quiet               # must print LINT OK
python3 tools/build_manifest.py                      # bump PACKAGE_VERSION first; also bump dd-version on every page
M=$(mktemp -d) && tar --exclude=.git -cf - . | tar -xf - -C "$M"
python3 tools/verify_manifest.py --manifest manifest.json --root "$M" --expect-manifest-sha256 "$(sha256sum manifest.json | cut -c1-64)"
git add -A && git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -m "…" && git push -u origin claude/happy-knuth-yqtd41
```

Version string lives in `tools/build_manifest.py` (`PACKAGE_VERSION`), every page's `dd-version` meta, masthead and footers (the deck repeats it on each slide), `src/build/gen_register.py` (`VER`) and `README.md`. Rendering needs Node 18+, `playwright` and the Chromium path set in `src/render.js`; rendering is deterministic in content, not bytes — the manifest, not a re-render, is the reference. After the pin, report to GPT/Lyra: the version string, the commit hash, the `manifest.json` SHA-256, the payload file count and a short change list.

## 7. What not to do

- Do not edit a PDF; edit the page source and re-render. Do not edit the pinned workbook; derive. Do not rebuild `manifest.json` for a working commit.
- Do not send, file, publish, look up an address, or write to any mirror; do not ask the founder a question; do not quote the forbidden label; do not print a model identifier into the repository.
- Do not adopt a reviewer's categorical statement as a fact (e.g. “no other patents pending”, “no device exists”, “completely decoupled”); record it and state the evidence scope.
- Do not treat a Grok verdict, an Antigravity recommendation or a Lyra acceptance as send, filing or installation authority.

## 8. Added later on 16 October — the presentation build (r6; D13, S-58)

The founder's direction: the EnergyWave Final collection is the living presentation link for investors, DoW reviewers, collaborators and K&L Gates; the orange “needs input” language stays internal, and the outward materials say what is projected, planned or set with counsel (“this is the forecasted model that we have put together”). Mechanics:

- **One source, two outputs.** `node src/render.js` renders every page internally (as before) and, for pages with a `dd-final` meta, a presentation form into `EnergyWave_Final/<dd-final-folders>/`. In the page source: `data-int` = internal only; `data-ext` = presentation only (hidden internally by CSS); every `.need` marker needs `data-proj="…"` (or the body's `data-proj-template` / `data-proj-empty`); `.tag` and `.sources` are dropped unless `data-keep`; `.status` takes `data-status`; `.ver` takes the edition; slide footers take body `data-final-foot`. The transform is fail-closed: a marker without projected text, or any phrase in `src/build/final_banned.json`, refuses the render.
- **Build the collection:** `python3 src/build/build_final.py` (empties `EnergyWave_Final/`, renders, copies the originals and the forecast model byte for byte, runs `src/build/check_final.py` on the PDFs). Run it before every pin; the tree is payload and is in the manifest. Never edit a file in it.
- **Language rules outward:** a projected figure is the forecast model's (v1.2: Base $18,453,008 plan / $22,143,610 raise; gates $6,987,330 / $13,719,010 / $22,143,610; Lean $15,821,567 / $18,985,880; Full $22,303,608 / $26,764,330), labelled as a projection; a plan is labelled a plan; a term is “set with counsel”; the entity is “in formation with K&L Gates LLP”; no device figure, no unsupported credential, no consent, filing or agreement is asserted outward that the internal page leaves open; no reviewer names, ledger rows, decision numbers, file paths or version strings appear outward.
- **Installation:** GPT/Lyra copies the tree into the collection's nine folders by `DELIVERY_MAP.md`, moves the Review Records and the r4.1 snapshot out of the shared link (mirror instructions §7), verifies against `MANIFEST.md`. Sharing the link is Ian's action; the 506(b)/(c) point (C-1) was put to him once and is not re-raised unless asked.
- **Antigravity's “fill in the blank audit”** is expected (register R-5): each proposed fill is a reviewer suggestion, adopted only with a source or the founder's direction.

