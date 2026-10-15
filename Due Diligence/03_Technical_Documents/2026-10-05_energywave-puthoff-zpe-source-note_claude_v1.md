# Source note — Puthoff & Little, "Engineering the Zero-Point Field and Polarizable Vacuum for Interstellar Flight" (v1)

| Field | Value |
|---|---|
| Project | EnergyWave — physical architecture & baseline model |
| Author | Claude (Claude Desktop seat) |
| For | Antigravity IDE and GPT/Codex; Ian |
| Source | H. E. Puthoff and S. R. Little, Institute for Advanced Studies at Austin. Published in *J. Br. Interplanet. Soc.* 55:137–144 (2002). Public copy: https://arxiv.org/abs/1012.5264. Ian supplied the 2001 preprint PDF (Word source `pv-final.doc`, Jan 2001); read the arXiv copy for the same paper. |
| Date | 5 October 2026 |
| Status | Source assessment for the council. Calculations are order-of-magnitude and labelled as such. Nothing here is a measured result. |
| Sourcing layer | Layer A as a citation (society journal, named authors, public copy). Its energy-extraction statements rest on proposals and patents that are not demonstrations (§3). |
| Requested result | Antigravity: consider adding Hypothesis 4 (§5) in v1.4. Codex: check §3–4. |

## 1. What the paper is

A 12-page overview of propulsion concepts:

- a momentum-conservation check on field propulsion ("hidden momentum");
- zero-point energy (ZPE) as a possible basis for gravity, inertia and energy;
- the polarizable-vacuum (PV) rewrite of general relativity, or "metric engineering".

It reports no device, no measured energy extraction and no energy budget for any apparatus. It says nothing about permanent magnets, ferrites, conditioning or the VTA.

## 2. What we can cite it for

- **Vacuum fluctuations are real and can be altered by technology.** Examples: the Casimir force, now measured to high accuracy (Lamoreaux 1997; Mohideen & Roy 1998), and control of spontaneous emission in cavity QED. This matches our principles file.
- **"Vacuum engineering" is a legitimate research question in mainstream physics.** The term comes from T. D. Lee's field-theory textbook.
- **Conservation comes first.** Before examining any propulsion mechanism, Puthoff says to "apply this principle as an overall constraint to determine whether the principle is violated." He then shows that static-field propulsion fails on momentum conservation. Our first-law closure applies the same discipline to energy.
- **Its framing fits our claims discipline.** It calls the idea "not a priori ruled out, although certain constraints need to be acknowledged." It closes with Podolny, quoted by Puthoff: "It would be just as presumptuous to deny the feasibility of useful application as it would be irresponsible to guarantee such application."

## 3. What it does not support, in its own words

- **Casimir extraction:** "the amount of energy release for mechanical structures under laboratory conditions is minuscule," and "the conservative nature of the Casimir effect would appear to prevent recycling."
- **Plasma pinches and sonoluminescence:** "as yet without real promise for energy applications."
- **The authors' own ground-state experiment at a synchrotron:** "so far without success."
- **Overall:** "it remains to be determined whether such exploitation is even feasible."
- **The thermodynamics claim is narrower than it sounds.** The paper says "no energetic or thermodynamic constraints [prevent] such release under certain conditions," citing Cole & Puthoff, *Phys. Rev. E* 48, 1562 (1993). Read together with its own no-recycling point, that covers a one-time release when boundary conditions change. It does not support continuous output from a repeating cycle.
- **The energy-density figure is not a usable store.** The paper says the ZPE density is "on the order of nuclear energy densities or greater"; that is a theoretical sum over field modes, not a measured or available figure. If dark energy is vacuum energy, its measured density is about 5×10⁻¹⁰ J/m³. The gap between the two is the unsolved cosmological-constant problem.
- **A patent is not a demonstration.** The ZPE-converter patent the paper mentions (Mead & Nachamkin, US 5,590,031) is granted, but a grant does not establish that a device works.

## 4. The numbers behind "minuscule"

Order of magnitude, for ideal conductors; real metals give less.

| Quantity | Value |
|---|---|
| Casimir energy per area at 10 nm / 100 nm / 1 µm gap | 4×10⁻⁴ / 4×10⁻⁷ / 4×10⁻¹⁰ J/m² |
| Best-case single-use stack: 10 nm gold plates, 10 nm gaps, full collapse credited | ≈2×10⁴ J/m³, about 2 J/kg |
| Lithium-ion cell, for comparison | ≈250 Wh/kg = 9×10⁵ J/kg: about 400,000× more, and rechargeable |
| PV metric change from 1 C on a 5 cm sphere (no surface can hold that charge: it would need 3.6×10¹² V/m) | ~10⁻³² |

The one vacuum effect confirmed by experiment is, even idealized, a single-use store about 400,000 times less energy-dense than the battery a humanoid robot already carries.

The PV "engineered metric" (K < 1) applies only to propulsion and has no path at lab scale. The paper concedes this: "the required energy densities exceed by many orders of magnitude values achievable with existing engineering techniques."

## 5. How it enters the protocol

- **Add it as Hypothesis 4 (vacuum-fluctuation source), with no exemption from closure.** A vacuum-sourced surplus would have to show up the same way as any other source: heat out exceeding DC in, persisting past the stored-energy ceiling (review v1, §5–6). A Casimir-type term is a one-time release bounded by geometry (about 4×10⁻⁴ J per m² of 10 nm gap). It belongs in ΔU, not in P_in.
- **Two-question filter.**
  - Net source? The vacuum is the ground state; only a change in boundaries releases energy, and only once.
  - Colder sink? None: nothing sits below the ground state.
  - A continuously running vacuum device fails both questions unless the experiment shows otherwise.
- **No link to the VTA.** The paper gives no mechanism connecting ferrite magnets or conditioning to vacuum fluctuations, so it cannot be cited as support for the VTA lineage.
- **Public and investor use: §2 items only.** Never cite it for energy density, device feasibility or performance. This is consistent with the keep-off-public-sites list.
