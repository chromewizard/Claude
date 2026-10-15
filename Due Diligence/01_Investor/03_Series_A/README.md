# Series A

**What this is.** The later-stage package: the raise model Ian built, the cap table and the Series A deck.

**Status (r3).** The Raise Model is placed as a **corrected copy** and its reading note is drafted. Raise Model v2, cap table v1.1 and a Series-A-specific deck are referenced by the September manifest but **not located** in the 255-file inventory (M-08).

## Contents

| File | Status | What it is |
|---|---|---|
| `EnergyWave_Raise_Model_v1.1-corrected_2026-10-15.xlsx` | CORRECTED COPY — 148,646 B | Ancestry: `EnergyWave_Raise_Model_v1.xlsx`, 7 Sept 2026, 149,053 B, SHA-256 `a9126068…31ab` (M-02; untouched on the Mac). **The one change:** Roster!A4 — the parenthesized nickname after the founder's name removed; the cell now reads "Ian F. McLean". Made in `xl/sharedStrings.xml` only (exactly one match replaced); every other ZIP member is byte-identical to v1 and was verified so; no formula touched or recalculated. The original fails `tools/lint.py` (exit 1); this copy passes (exit 0). |
| `EnergyWave_Raise_Model_Note_2026-10-15.pdf` | DRAFT — 2 pages (r3) | What the workbook is (ten sheets, conventions, scenario lever), the headline outputs with their origin (Financial_Status_2026-09-18 — *model outputs on placeholder inputs*), the structure a diligence reader looks for, and what exists for Series A and what does not. Source: `../../src/pages/09_Raise_Model_Note.html`. |

## Not located

| Item | Note |
|---|---|
| Raise Model v2 (11 Sept 2026) | Headline figures known from the Financial Status note ($19.68M base / $23.40M with the full engineering band); the file is not in the inventory — ask Ian whether it exists as a file. |
| Cap table v1.1 DRAFT (11 Sept 2026) | Founder ≈ 29.5% fully diluted after Series A on placeholder inputs (Financial Status note); file not located. |
| Series A deck (13 slides, 11 Sept 2026) | Not located. |

## Naming rule (D8)

The corrected v1 is never called "v2" while a historical v2 remains unlocated. Ancestry is recorded in `SOURCE_LEDGER.md` §E.
