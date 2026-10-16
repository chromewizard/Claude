# Delivery map — the EnergyWave Final collection, built from the canonical package

**What the collection is (founder, 16 Oct 2026, ledger S-58).** `EnergyWave Final` is the living presentation link: the materials prospective investors, Department of War reviewers, collaborators and counsel may see at any time. It holds no drafts and no working apparatus. Where the canonical package marks an undetermined item with the orange `[TBD] — …` or `[Pending: …]`, the collection says what is projected, planned or set with counsel. Nothing in the collection states a fact the canonical package does not support; the projected figures are the forecast model's (v1.2, 16 October 2026) and are labelled as projections.

**How it is built.** `python3 src/build/build_final.py` regenerates `EnergyWave_Final/` from empty on every pin: `src/render.js --final` renders each page's presentation form (its `dd-final` name, into its `dd-final-folders`; fail-closed on any marker without projected text or any internal language — `src/build/final_banned.json`), the approved originals and the forecast model are copied byte for byte and hash-checked, and `src/build/check_final.py` re-reads every rendered PDF. Every file in `EnergyWave_Final/` is in `manifest.json`. **No file in the collection is ever edited by hand**; a change is made in the page source and the tree rebuilt.

**Layout (Ian, 14 Oct 2026).** `/Users/ian/Documents/EnergyWave Final/Due Diligence/` holds three round folders — `Capital Readiness`, `Seed Round`, `Series A` — and each holds three audience folders: `Government DoW:DoE:DARPA Package`, `Investor Due Dilligence Packet`, `Technical Package` (names exactly as they exist on disk). The repository tree uses the equivalent names below; GPT/Lyra copies by this mapping and verifies each copy against `MANIFEST.md`.

| Repository folder (`EnergyWave_Final/…`) | Collection folder on the Mac (`EnergyWave Final/Due Diligence/…`) |
|---|---|
| `EnergyWave_Guide_to_these_Materials_2026-10-16.pdf` (root) | `Due Diligence/` (root) |
| `1_Capital_Readiness/Investor_Package/` | `Capital Readiness/Investor Due Dilligence Packet/` |
| `1_Capital_Readiness/Government_Package/` | `Capital Readiness/Government DoW:DoE:DARPA Package/` |
| `1_Capital_Readiness/Technical_Package/` | `Capital Readiness/Technical Package/` |
| `2_Seed_Round/Investor_Package/` | `Seed Round/Investor Due Dilligence Packet/` |
| `2_Seed_Round/Government_Package/` | `Seed Round/Government DoW:DoE:DARPA Package/` |
| `2_Seed_Round/Technical_Package/` | `Seed Round/Technical Package/` |
| `3_Series_A/Investor_Package/` | `Series A/Investor Due Dilligence Packet/` |
| `3_Series_A/Government_Package/` | `Series A/Government DoW:DoE:DARPA Package/` |
| `3_Series_A/Technical_Package/` | `Series A/Technical Package/` |

## Shared sets — identical copies in more than one folder

### Set I — investor core (every `Investor_Package`)
| File in the collection | Rendered from | What it is |
|---|---|---|
| `EnergyWave_Guide_to_these_Materials_2026-10-16.pdf` | `src/pages/00_Reading_Guide.html` | How to read the materials; how statements are labelled; rounds and audiences; reading orders; where things stand. Also at the collection root. |
| `EnergyWave_Claims_Discipline_2026-10-16.pdf` | `src/pages/02_Claims_Discipline.html` | The rules every document obeys. (Also in every Government and Technical package.) |
| `EnergyWave_Team_and_Counsel_2026-10-16.pdf` | `src/pages/04_Team_and_Counsel.html` | The roster with the lines the company prints for each person, and how the lines are supported. |
| `EnergyWave_Corporate_IP_and_Legal_Status_2026-10-16.pdf` | `src/pages/05_Entity_IP_Legal_Status.html` | The entities, the IP position, counsel's advice summarized, the workplan with counsel. |

### Set G — government core (every `Government_Package`)
| File in the collection | Source | What it is |
|---|---|---|
| `EnergyWave_Claims_Discipline_2026-10-16.pdf` | `src/pages/02_Claims_Discipline.html` | As above. |
| `EnergyWave_xTech_Search10_Submission_Summary_2026-10-16.pdf` | `src/pages/07_xTech_Submission_Record.html` | The competition entry: who applied, what was submitted and when, what the paper proposes. |
| `McLean Capital Development LLC_xTech_Search10_White_Paper.pdf` | original `02_DoW/EnergyWave_xTech_Search10_Paper_APPROVED_REPLACEMENT_2026-10-09.pdf` (`90823d62…`), byte for byte, under the portal's filename | The three-page competition paper as approved by the founder. |
| `EnergyWave_Applicant_and_Eligibility_Facts_2026-10-16.pdf` | `src/pages/08_Applicant_and_Eligibility.html` | Applicant of record, ownership, eligibility facts with their evidence or plan. |
| `EnergyWave_Compartmentalization_AT_Posture_v0.1_2026-09-12.pdf` | original, byte for byte | How know-how and any future hardware would be protected (CPI / AT), pre-device. |
| `EnergyWave_DoW_White_Paper_v2.1_2026-10-16.pdf` | `src/pages/17_DoW_White_Paper_v2.1.html` | Energy at the Point of Use, v2.1 — supersedes v2.0 for government use. |
| `EnergyWave_Safe_Release_Posture_2026-10-16.pdf` | `src/pages/19_Safe_Release_Posture.html` | If a high-density power source ever exists, how it ships. |

### Set T — technical core (every `Technical_Package`)
| File in the collection | Source | What it is |
|---|---|---|
| `EnergyWave_Claims_Discipline_2026-10-16.pdf` | `src/pages/02_Claims_Discipline.html` | As above. |
| `EnergyWave_Research_Program_and_Gates_2026-10-16.pdf` | `src/pages/03_Research_Program_and_Gates.html` | The protocol, the threads, the commitments. |
| `EnergyWave_Thread_A_Characterization_Plan_2026-10-16.pdf` | `src/pages/14_Thread_A_Characterization_Plan.html` | The plan for the lead research path; inventor-defined inputs specified at kickoff. |
| `EnergyWave_Humanoid_Power_Budget_Specification_2026-10-16.pdf` | `src/pages/15_Humanoid_Power_Budget.html` | The load a power supply must meet; platform inputs set at the design review. |
| `EnergyWave_Measurement_Platform_Error_Budget_2026-10-16.pdf` | `src/pages/16_Platform_Error_Budget.html` | Thread C for external review; bounds measured at commissioning. |
| `EnergyWave_Physical_Architecture_and_Baseline_Model_v1.3_2026-10-05.pdf` | original, byte for byte | The working briefing: reservoir inventory, energy accounting, metrology, the conditioning hypotheses. |

## Round-specific files

| Folder | File in the collection | Source |
|---|---|---|
| `1_Capital_Readiness/Investor_Package` | `EnergyWave_Deck_2026-10-13.pdf` · `EnergyWave_OnePager_2026-10-13.pdf` | approved originals (`3446357c…`, `dda97ba0…`), byte for byte |
| `1_Capital_Readiness/Investor_Package` | `EnergyWave_Capital_Readiness_Terms_and_Objectives_2026-10-16.pdf` | `src/pages/01_Capital_Readiness_Terms.html` |
| `1_Capital_Readiness/Investor_Package` | `EnergyWave_Capital_Readiness_Indicative_SAFE_Terms_2026-10-16.pdf` | `src/pages/10_SAFE_Term_Summary.html` |
| `2_Seed_Round/Investor_Package` | `EnergyWave_Seed_Deck_2026-10-16.pdf` (16 slides) · `EnergyWave_Seed_OnePager_2026-10-16.pdf` · `EnergyWave_Seed_Round_Structure_2026-10-16.pdf` | `src/pages/12_…`, `11_…`, `06_…` |
| `2_Seed_Round/Technical_Package` | `EnergyWave_Seed_Round_Technical_Docs_2026-10-16.pdf` | `src/pages/20_Seed_Round_Technical_Docs.html` |
| `3_Series_A/Investor_Package` | `EnergyWave_Series_A_Readiness_Outline_2026-10-16.pdf` · `EnergyWave_Forecast_Model_Reading_Note_2026-10-16.pdf` · `EnergyWave_Raise_Model_v1.2_2026-10-16.xlsx` (the forecast model, byte for byte) | `src/pages/13_…`, `09_…`; the workbook |

## Not in the collection, and why

| File | Why it stays in the canonical package only |
|---|---|
| `EnergyWave_Open_Items_Register_2026-10-15.pdf`, `NEEDS_INPUT.md` | The working register of markers — internal by definition. |
| Every internal document (`…_2026-10-15.pdf`) | The marked, sourced working versions; the collection carries their presentation form. |
| `02_DoW/EnergyWave_xTech_Search10_Paper_AS_SUBMITTED_2026-10-09.pdf` | The private-review record of the 9 Oct upload (banner and blank cover fields); evidence of the submission, superseded by the approved paper. |
| `02_DoW/EnergyWave_DoD_White_Paper_v2.0_2026-08.pdf` | Superseded by v2.1 for government use; retained for provenance. |
| `01_Investor/02_Seed_Round/EnergyWave_Investor_Overview_DRAFT_2026-09-07.pptx`, `03_Technical_Documents/EnergyWave_Technical_Prospectus_DRAFT_v1_2026-09-07.docx` | September ancestors with bracketed placeholders; history only. |
| The five technical notes of 5 Oct 2026 and `Key_Research_Facts_verified_2026-09-07.md` | Working notes in Markdown; their content is carried by the Research Program and Technical Docs pages. |
| `EnergyWave_Raise_Model_v1.1-corrected_2026-10-15.xlsx` | The September model's corrected copy; the collection carries its v1.2 successor. |
| `README.md`, `MANIFEST.md`, `manifest.json`, `SOURCE_LEDGER.md`, `DECISIONS.md`, `REVIEW_PROTOCOL.md`, this map, every folder `README.md`, `90_Internal_Ops_NOT_FOR_CIRCULATION/`, `99_Source_Archive/`, `src/`, `tools/` | Governance, controls and build source. |

## Readiness, stated plainly

The collection is built to be sent as “the forecasted model we have put together” (founder, 16 Oct 2026). It is professional in form and projected in language; it is not a legal clearance. Before the link goes to anyone the company has not spoken with, counsel's answer on the securities exemption (Rule 506(b) or 506(c)) governs — the internal counsel question set carries that item, and K&L Gates is the first intended recipient of the link. The people are named per the founder's confirmations of 15–16 October 2026; written team and advisor agreements follow formation. Every projected figure is the forecast model's and is labelled as a projection.

## How a change reaches the collection

A fact arrives, a decision is taken or a reviewer finds a defect → the lead edits the page source (internal text, projected text, or both), re-renders, rebuilds `EnergyWave_Final/` with `src/build/build_final.py`, re-pins the release and updates this map in the same commit → GPT/Lyra delta-checks the pin → GPT/Lyra copies the changed files into the collection's folders by the mapping above, verifies each against `MANIFEST.md`, and rebuilds the collection's `FILE_MANIFEST.json`. One writer at a time; nothing is edited in the collection.
