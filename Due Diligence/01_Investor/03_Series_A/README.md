# Series A

**What this is.** The later-stage package: the raise model Ian built, the cap table and the Series A deck.

**Status (r5).** The Raise Model is placed as a **corrected copy**, its reading note is drafted, and the Series A Readiness Outline lists what a Series A reader expects, what exists, and what closes each gap. Raise Model v2, cap table v1.1 and a Series-A-specific deck are referenced by the September manifest but **not located** (M-08); the outline marks them `[TBD] — …` (orange ink) (register B-3). Founder's Series A example audience: groups such as Sequoia Capital — a target, not a relationship (15 Oct 2026).

## Contents

| File | Status | What it is |
|---|---|---|
| `EnergyWave_Raise_Model_v1.1-corrected_2026-10-15.xlsx` | CORRECTED COPY — 148,646 B | Ancestry: `EnergyWave_Raise_Model_v1.xlsx`, 7 Sept 2026, 149,053 B, SHA-256 `a9126068…31ab` (M-02; untouched on the Mac). **The one change:** Roster!A4 — the parenthesized nickname after the founder's name removed; the cell now reads "Ian F. McLean". Made in `xl/sharedStrings.xml` only (exactly one match replaced); every other ZIP member is byte-identical to v1 and was verified so; no formula touched or recalculated. The workbook retains v1's saved calculation results (saved scenario: Base; UseOfFunds!C4 = 17,073,008.33, C6 = 20,487,610; checks C38:C40 = 0 as stored) — stored historical results, not validated outputs. The original fails `tools/lint.py` (exit 1); this copy passes (exit 0). |
| `EnergyWave_Series_A_Readiness_Outline_DRAFT_2026-10-15.pdf` | DRAFT — 2 pages (r5) | Where Series A sits (a Gate-3 event); the model's stored Base figures with their origin; the readiness checklist (gate reports, validation, cap table, deck, validated model, financials, IP, governance, data-room index) with what closes each; what the folder will hold when the inputs arrive. Source: `../../src/pages/13_Series_A_Readiness.html`. |
| `EnergyWave_Raise_Model_Note_2026-10-15.pdf` | DRAFT — 2 pages (r4) | What the workbook is (ten sheets, conventions, scenario lever), the headline outputs with their origin (Financial_Status_2026-09-18 — *model outputs on placeholder inputs*), the structure a diligence reader looks for, and what exists for Series A and what does not. Source: `../../src/pages/09_Raise_Model_Note.html`. |

## Not located

| Item | Note |
|---|---|
| Raise Model v2 (11 Sept 2026) | Headline figures known from the Financial Status note ($19.68M base / $23.40M with the full engineering band); the file is not in the inventory — [TBD]; not asked again. |
| Cap table v1.1 DRAFT (11 Sept 2026) | Founder ≈ 29.5% fully diluted after Series A on placeholder inputs (Financial Status note); file not located. |
| Series A deck (13 slides, 11 Sept 2026) | Not located. |

## Naming rule (D8)

The corrected v1 is never called "v2" while a historical v2 remains unlocated. Ancestry is recorded in `SOURCE_LEDGER.md` §E.
