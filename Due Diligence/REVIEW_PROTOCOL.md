# Cross-check protocol — GPT (Lyra / Aura), Antigravity, Grok (Architect, Compliance)

The point lead integrates; reviewers find. No reviewer edits a canonical file. Reviewer IDs: `F-GPT-*`, `F-LYRA-*`, `F-AG-*`, `F-Grok-*`, `F-Comp-*`.

## Before reading anything

1. Verify the mirror you are reading with the read-only verifier and the manifest hash pinned in the handoff — never by rebuilding:
   `python3 tools/verify_manifest.py --manifest <trusted manifest.json> --root <mirror> --expect-manifest-sha256 <pinned>`
   A mismatch is finding #1 — stop and report it.
2. Run the forbidden-label scan: `python3 tools/lint.py --root <mirror> --json report.json`. Exit 0 is the only pass; exit 2 (unscanned surface) is reported, not ignored. Note the `visual_review` list — images and image-only PDF pages need a human look.
3. Read the rendered PDFs as the audience will. Use `src/pages/*.html` only to cite the line of a proposed wording fix; the PDF and its HTML are both in the manifest, and a difference between them is a finding.

## What to check, in order

1. **Internal consistency** — the same number, name, date or claim is identical in every file: amount, runway, entity name and status, applicant of record, first research module, team roles, contact details.
2. **Claims discipline** — no sentence implies a device exists, works, or will work; every performance figure is attributed to its published author; every number carries its origin label (assumption · calculation · proposed target · company measurement · attributed published result); every forward-looking statement carries the disclaimer.
3. **Source fidelity** — each fact traces to a row in `SOURCE_LEDGER.md`, and the row's status supports the use (a REPORTED or secondary-summary row cannot support an outward-facing statement of fact). Unsourced is a finding.
4. **Audience fit** — the Investor package answers *why now, why this team, what does the money buy, what are the gates*. The DoW package answers *who is the applicant, what is the capability, how is it protected (CPI / AT), what are the eligibility facts, what exactly was submitted and when*.
5. **Freshness** — nothing superseded survives: the expired provisional described as live; "operating company" before formation; DoE assumptions in Army material; advisors in roles they have not confirmed; a reviewer's summary cited as counsel's words.
6. **Rendering fidelity** — nothing truncated at a page break; a continued table repeats its column headings; no section heading stranded from its first row; no page holding only a Sources block. On every page: the running header (document title · Confidential — Draft — For Discussion · version) and the footer (disclaimer · source pointer · page numbers). Once per document: the masthead and status line on page 1; status tags (Original · Verified · Open · Historical · Draft) wherever a file or fact is characterized; the "Sources:" block at the end, citing ledger rows for the whole document. The wordmark renders on the page's white background, as on the approved one-pager.

## Finding format — one line each

```
F-<reviewer>-<n> | <file> | <section or line> | <claim as written> | <evidence or ledger row> | <blocker | major | minor> | <proposed fix>
```

- **blocker** — would fail diligence or mislead: wrong entity, unsupported credential, device claim, forbidden label, a control that passes when it should fail.
- **major** — contradiction between files, missing source, stale fact, a summary presented as a primary record.
- **minor** — wording, formatting, naming convention.

## Returning

- One file per reviewer per round: `YYYY-MM-DD_dd-review_<reviewer>_vN.md` in `02_Project_Handoffs` on Drive, or pasted in chat. Source evidence goes in a sibling supplement, never into package folders.
- Close with one acknowledgment line: reviewer · package version · commit · `manifest.json` SHA-256 · count by severity.
- The lead answers every finding with **accepted / fixed (commit)** or a **source-backed disagreement**. Disagreements between reviewers are recorded, not averaged. Ian decides.
