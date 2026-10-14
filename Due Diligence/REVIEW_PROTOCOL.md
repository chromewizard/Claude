# Cross-check protocol — GPT (Lyra / Aura), Antigravity, Grok (Architect, Compliance)

The point lead integrates; reviewers find. No reviewer edits a canonical file.

## Before reading anything

1. Verify every file's SHA-256 against `manifest.json`. A mismatch is finding #1 — stop and report it.
2. Run (or re-run) the forbidden-label scan in `tools/lint.sh` against every file, path, metadata field and spreadsheet cell.

## What to check, in order

1. **Internal consistency** — the same number, name, date or claim is identical in every file: amount, runway, entity name and status, first research module, team roles, contact details.
2. **Claims discipline** — no sentence implies a device exists, works, or will work; every performance figure is attributed to its published author; every forward-looking statement carries the disclaimer.
3. **Source fidelity** — each fact traces to a row in `SOURCE_LEDGER.md`. Unsourced is a finding.
4. **Audience fit** — the Investor package answers *why now, why this team, what does the money buy, what are the gates*. The DoW package answers *who is the applicant, what is the capability, how is it protected (CPI / AT), what are the eligibility facts*.
5. **Freshness** — nothing superseded survives: the expired provisional 63/763,998 described as live; "operating company" before formation; DoE assumptions in Army material; advisors in roles they have not confirmed.

## Finding format — one line each

```
F-<reviewer>-<n> | <file> | <section or line> | <claim as written> | <evidence or ledger row> | <blocker | major | minor> | <proposed fix>
```

- **blocker** — would fail diligence or mislead: wrong entity, unsupported credential, device claim, forbidden label.
- **major** — contradiction between files, missing source, stale fact.
- **minor** — wording, formatting, naming convention.

## Returning

- One file per reviewer per round: `YYYY-MM-DD_dd-review_<reviewer>_vN.md` in `02_Project_Handoffs` on Drive, or pasted in chat.
- Close with one acknowledgment line: reviewer · package version reviewed · `manifest.json` SHA-256 · count by severity.
- Disagreements between reviewers are recorded, not averaged. Ian decides.
