# Technical Documents

**What this is.** The physics and the protocol — what a technical reviewer reads to decide whether the program is disciplined.

**Scope statement.** No measured EnergyWave hardware performance evidence has been reviewed for this package. Numbers in the EnergyWave-authored documents are assumptions, calculations or proposed targets and are labelled by origin; figures cited from published research (e.g., Moddel et al.'s 1.4 pW) are attributed to their authors and are not EnergyWave results.

**Status (r5).** The Research Program page, the Thread A Characterization Plan, the Humanoid Power Budget Specification and the Measurement Platform Error Budget are drafted; the Oct-5 briefing, the September prospectus, five Oct-5 notes and the Key Research Facts page are placed. Which thread leads is the founder's decision (D2); the inventor-defined inputs for thread A and the platform inputs for the power budget are tagged `[Needs Input from Ian or Chip: …]` (register B-4 to B-6). No dependency between threads is asserted. The legacy QVE-era documents (2023–2025) are recorded in `SOURCE_LEDGER.md` §F and are not placed.

## Contents

| File | Status | What it is |
|---|---|---|
| `EnergyWave_Research_Program_and_Gates_2026-10-15.pdf` | DRAFT — 3 pages (r4) | The research question; the three-gate protocol with pass / kill criteria; the energy-accounting standard; threads A (founder's solid-state module), B (independent replication of Moddel et al. 2021), C (measurement platform) kept separate under one protocol; the eight commitments; why physicists expect "no"; the documents in this folder. Source: `../src/pages/03_Research_Program_and_Gates.html`. |
| `EnergyWave_Thread_A_Characterization_Plan_DRAFT_2026-10-15.pdf` | DRAFT (r5) | The first testable question for the founder's module; hypotheses H-A1 (stored-energy depletion), H-A2 (environmental transduction), H-A3 (metrology phase skew); specimen table with off-the-shelf baseline proposals and inventor-input tags; the four-step unconditioned characterization; energy accounting and the deskew benchmark; artifact catalogue; pre-registered pass / kill / ambiguous rule; deliverables. Source: `../src/pages/14_Thread_A_Characterization_Plan.html`. |
| `EnergyWave_Humanoid_Power_Budget_Specification_DRAFT_2026-10-15.pdf` | DRAFT (r5) | Capital-readiness objective #2: method; attributed platform benchmarks; the subsystem worksheet (sight and sound, smell and taste, touch, motion, compute, thermal) with platform inputs tagged; the worked structure on a published anchor; the specification outputs (P̄, P-peak, ramp, mass, volume, heat rejection); what the document is not. Source: `../src/pages/15_Humanoid_Power_Budget.html`. |
| `EnergyWave_Measurement_Platform_Error_Budget_DRAFT_2026-10-15.pdf` | DRAFT (r5) | Thread C for external review: the floor criterion for thread B (≤ 0.14 pW), the error-budget table with every term "[to be measured]" until commissioning, the commissioning sequence on known-null samples, calorimetry, sign-off (leads tagged). Source: `../src/pages/16_Platform_Error_Budget.html`. |
| `EnergyWave_Physical_Architecture_and_Baseline_Model_v1.3_2026-10-05.pdf` | VERIFIED original — 6 pages | AI-reviewed working briefing (Antigravity & GPT/Codex; reviewed by Claude): reservoir inventory, energy accounting, metrology, the conditioning hypotheses, baseline characterization. PB-2 — the build in the main collection's `02 Technical`; the Drive copy (S-11) was downloaded as exact bytes in r4 and is byte-identical (M-14 / S-11; SHA-256 `b65ddf5a…5aef`). Its §6 legal/corporate table is historical and superseded by `04_Legal_and_IP`; its "63/763,986" reference is unsupported by the ALG document text. Canonical build to be confirmed by Ian (D8). |
| `EnergyWave_Technical_Prospectus_DRAFT_v1_2026-09-07.docx` | HISTORICAL original | The September program in full — §4 physics with labels; §6 Gate 1 design and artifact catalogue; §6.5 workstream 1C (the founder's own structures under the same protocol; conditional Forward-1984 note); §6.6 decision rule. From `EnergyWave_DataRoom_v1_DRAFT.zip` (M-05; SHA-256 `126325d2…bb16`). |
| `2026-10-05_energywave-physics-review_claude_v2.md` | VERIFIED — exact Drive bytes (S-13) | Claude's engineering review of the briefing, v2 (supersedes v1; v1's Python appendix still applies). |
| `2026-10-05_energywave-puthoff-zpe-source-note_claude_v1.md` | VERIFIED — exact Drive bytes (S-15) | Puthoff & Little assessed; best-case single-use Casimir stack ≈ 2 J/kg against ~9×10⁵ J/kg for lithium-ion. |
| `2026-10-05_energywave-sources-regauging-pais-exodus_claude_v1.md` | VERIFIED — exact Drive bytes (S-16) | Regauging essay, Pais Navy patents, Exodus Propulsion checked; identifies the description file uploaded for 63/763,998. |
| `2026-10-05_zpe-gr-physics-evaluation_antigravity_v1.md` | VERIFIED — exact Drive bytes (S-17) | GR-coupling evaluation. |
| `2026-10-05_zpe-gr-physics-evaluation-review_claude_v1.md` | VERIFIED — exact Drive bytes (S-18) | Review of the above. |
| `Key_Research_Facts_verified_2026-09-07.md` | HISTORICAL — September packet member (M-03b) | One-page corrections to common belief; the energy figures used in the narrative. |

## Drafted; waiting on inputs

| Item | Waiting on |
|---|---|
| Thread A characterization plan — specimen, magnetization, winding axis, conditioning; the founder's notes and prior measurements | Ian or Chip (register B-4); D2 |
| Humanoid power-budget specification — target platform, mass and bay volume, duty profile, heat rejection, the six subsystem rows | Ian or Chip (register B-5) |
| Measurement-platform error budget — the thread A effect size to resolve, the calorimetric resolution to fund, the thread C and measurement leads | Ian or Chip; thread C lead (register B-6) |

## Register

Legitimate adjacent science (Casimir effect, Lamb shift, metamaterials, ion-wind / field propulsion) is kept explicitly separate from the contested leap (continuous net extraction from the vacuum), exactly as the deck does on slide 6. Every number carries its origin label.
