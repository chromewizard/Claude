"""Generates the Open Items Register (src/pages/18_Needs_Input_Register.html, rendered to
EnergyWave_Open_Items_Register_2026-10-15.pdf) and NEEDS_INPUT.md from the [TBD] / [Pending: ...] markers in the
pages and control files plus the fixed rows below. Run from anywhere:  python3 src/build/gen_register.py
Then re-render the register page:  node src/render.js 18_Needs"""
import os, re, glob, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pp import ROOT, write
from conv import wrap_html, conv_md

VER = "DD-2026-10-16-r6-draft"
SPAN = re.compile(r'<span class="need">(.*?)</span>', re.S)
MDM = re.compile(r"\[TBD\] — [^|·\n]+|\[TBD\]|\[Pending:[^\]]*\]")

def strip(t):
    return html.unescape(re.sub(r"<[^>]+>", "", t)).strip()

def markers_html(path):
    s = open(os.path.join(ROOT, path), encoding="utf-8").read()
    out = []
    for m in SPAN.finditer(s):
        t = strip(m.group(1))
        if (t.startswith("[TBD]") or t.startswith("[Pending")) and "…" not in t and t not in out:
            out.append(t)
    return out

def markers_md(path):
    s = open(os.path.join(ROOT, path), encoding="utf-8").read()
    out = []
    for m in MDM.finditer(s):
        t = m.group(0).strip()
        if "…" not in t and t not in out:
            out.append(t)
    return out

def title_of(page):
    s = open(os.path.join(ROOT, page), encoding="utf-8").read()
    return re.search(r'<meta name="dd-output" content="([^"]+)"', s).group(1)

def span(t):
    e = html.escape(t, quote=False)
    if e.startswith("[TBD]"):
        e = "<b>[TBD]</b>" + e[5:]
    return f'<span class="need">{e}</span>'

PAGES = [
    ("B-13", "src/pages/01_Capital_Readiness_Terms.html", "the founder, in his own time, with counsel"),
    ("B-1", "src/pages/10_SAFE_Term_Summary.html", "the founder with counsel; counsel for 506(b)/(c)"),
    ("B-2", "src/pages/12_Seed_Deck.html|src/pages/11_Seed_OnePager.html|src/pages/06_Seed_Round_Structure.html", "the founder with counsel; counsel for escrow and 506(b)/(c)"),
    ("B-3", "src/pages/13_Series_A_Readiness.html|src/pages/09_Raise_Model_Note.html", "the founder; a finance owner when named"),
    ("B-16", "src/pages/03_Research_Program_and_Gates.html", "Chip Story with the founder (inventor-defined)"),
    ("B-4", "src/pages/14_Thread_A_Characterization_Plan.html", "Chip Story with the founder (inventor-defined)"),
    ("B-5", "src/pages/15_Humanoid_Power_Budget.html", "the founder or Chip Story; the PI when hired"),
    ("B-6", "src/pages/16_Platform_Error_Budget.html", "the thread C lead and PI when hired"),
    ("B-12", "src/pages/20_Seed_Round_Technical_Docs.html", "filled from GPT/Codex's operating-requirements register; the founder in his own time"),
    ("B-14", "src/pages/04_Team_and_Counsel.html", "the founder (TBD fields); Chip; counsel"),
    ("B-7", "src/pages/17_DoW_White_Paper_v2.1.html", "the founder (TBD fields); Chip; counsel"),
    ("B-8", "src/pages/19_Safe_Release_Posture.html", "the founder (TBD fields); consents pending"),
    ("B-15", "src/pages/08_Applicant_and_Eligibility.html", "the founder, in his own time"),
]
# rows: (id, text_html, text_md, lands, who)
rows_B, rows_C = [], []
for bid, pages, who in PAGES:
    tbd, pend, outs = [], [], []
    for pg in pages.split("|"):
        outs.append(title_of(pg))
        for t in markers_html(pg):
            (tbd if t.startswith("[TBD]") else pend).append(t)
    lands = "; ".join(outs)
    if tbd:
        rows_B.append((bid, " · ".join(span(t) for t in tbd), " · ".join(tbd), lands, who))
    if pend:
        rows_C.append((bid.replace("B-", "P-"), " · ".join(span(t) for t in pend), " · ".join(pend), lands, who))

led = markers_md("SOURCE_LEDGER.md")
t9 = ("Legacy sources — the QVE Engine folder is inventoried if and when it reaches the Drive copy of the Mac collection or the Mac is connected; the Rossi relationship and the 2024 GPT-content text (D11) are TBD and counsel's lane; SHA-256 of each §F file from the Mac when Antigravity hashes them (R-2).")
rows_B.append(("B-9", (" · ".join(span(t) for t in led) + " — " if led else "") + html.escape(t9, quote=False), (" · ".join(led) + " — " if led else "") + t9, "SOURCE_LEDGER.md §D and §F", "TBD; Antigravity for the hashes"))
ops = []
for f in sorted(glob.glob("90_Internal_Ops_NOT_FOR_CIRCULATION/*.md", root_dir=ROOT)):
    ops += markers_md(f)
t10 = ("Internal-ops drafts — Chip's draft asks him for his printed wording, written consent and proposed co-founder terms (or “counsel to propose”); the counsel question set carries the formation and ALG placeholders counsel fills; Alan's and Jack's drafts are overtaken for role consent by the founder's own outreach of 16 Oct (H-1, H-2; S-56) and stay unsent. Every draft goes to Grok for its per-email review before any send; no send is authorized today.")
rows_B.append(("B-10", (" · ".join(span(t) for t in ops) + " — " if ops else "") + html.escape(t10, quote=False), (" · ".join(ops) + " — " if ops else "") + t10, "90_Internal_Ops_NOT_FOR_CIRCULATION/", "the founder (send authority only); Chip; counsel; Grok (review)"))
t11 = "Mirrors and project — GPT/Lyra places and verifies each reviewed release in the three copies and fills the nine audience folders from DELIVERY_MAP.md after review; Ian or Antigravity uploads manifest.json, MANIFEST.md and the twenty-one rendered documents to the EnergyWave Ops Claude Project (an action, not a question)."
rows_B.append(("B-11", html.escape(t11, quote=False), t11, "2026-10-15_mirror-instructions.md; README release table; DELIVERY_MAP.md", "GPT/Lyra; Ian or Antigravity"))

def P(rid, text, lands, who):
    return (rid, html.escape(text, quote=False), text, lands, who)

rows_F = [
    P("F01", "Audiences: Capital Readiness for close friends, family and angel investment groups, may combine with the Seed Round; Conviction the Seed example; Sequoia the Series A example; IQT, DOE, DoW, DARPA the government and national-security targets — targets, not relationships. The three round folders stand; the Capital Readiness deck is not relabelled. Still TBD: the combined-round structure, the exact opportunity, recipient and format.", "D1; Capital Readiness Terms; Series A outline §1; Reading Guide; DELIVERY_MAP.md", "closed (founder)"),
    P("F02", "No SAFE executed (“correct no safe has been done”); no funding raised. The prior-SAFE question is closed. Still TBD: the accounting basis reconciling the 9 Oct ≈ $10,000 record; the workbook's E10 / P4 entries stay as dated conflicts.", "D3; SAFE Term Summary; Capital Readiness Terms; Seed deck slide 5 and one-pager; Legal page; Applicant page; xTech record §5; Raise Model Note status box", "closed (founder)"),
    P("F03", "Amounts, instrument and budgets: no numeric target supplied (“sky is the limit” sets no number); a future SAFE possible, not selected. TBD: amount, tranche sizes, instrument, cap / valuation / discount / MFN, budget owner, allocation; the Oct-13 $60,000 and the model's outputs stay dated proposals and scenarios.", "every investor page (B-1, B-2, B-3, B-13)", "closed (founder); fields TBD"),
    P("F04", "Entity work: K&L Gates is handling the entity (founder) — a responsibility, not formation evidence. Certificate, file number, officer and share details are pending from counsel (C-2).", "D3; Legal page §1 and §5; Capital Readiness Terms; SAFE page; deck slides 5 and 14; one-pager; DoW v2.1 §5; Safe Release §8; Applicant page; counsel draft §A", "closed (founder); counsel pending"),
    P("F05", "First research path: Sweet solid-state leads. Replication (B) and metrology (C) stay distinct; xTech's proposal is not rewritten. TBD: specimen, conditioning, website-device identity, bench order, laboratory, named measurement lead (B-4, B-16).", "D2; Research Program; deck slide 6; one-pager; structure page; Thread A plan; Technical Docs hub; DoW v2.1 §3.2", "closed (founder); fields TBD"),
    P("F06", "Planned office: the UCI area near the National Fuel Cell Research Center, where the founder says ACT Hydrogen works — a plan. [TBD]: address, lease, space, price, laboratory access, any agreement (B-12). No lease, facility access, sponsored research, partnership, endorsement or institutional agreement with UCI, the NFCRC or ACT Hydrogen is established in the reviewed evidence; the plan implies none.", "D12; deck slide 9; one-pager; structure page; Technical Docs hub; Applicant page; Raise Model Note status box", "closed (founder); fields TBD"),
    P("F07", "Current core team: Ian McLean and Chip Story; Chip “cofounder Physicist” by the founder's designation (S-47), not credential proof. TBD: compensation, equity, vesting and agreements — counsel's lane.", "D4; Team page roster; deck slide 11; one-pager; DoW v2.1 §6; Safe Release §8", "closed (founder)"),
    P("F08", "Team additions: Mike Wentz — on the team by the founder's direct direction of 16 Oct 2026 (S-55), superseding the 15 Oct after-Capital-Readiness plan; title [TBD]; credentials unverified; consent pending, no outreach authorized. Arath Acosta — proposed Design Engineer from Seed onward (planned). [TBD]: other roles, terms, start, credentials; no age, praise, invented qualification, employment or signed hire.", "D4; Team page roster; deck slide 11; one-pager; DoW v2.1 §6; Safe Release §8; Raise Model Note status box", "closed (founder); fields TBD"),
    P("F09", "Roles confirmed (S-46): Alan Crunkleton — advisor; Jack Sarfatti — team member, not advisor (“Jack has consented as team member not advisor”); consent confirmed by the founder for both (founder-reported; no signed instrument claimed); supersedes the handoff's “both advisors” wording; historical records unchanged; not asked again. 16 Oct 2026 (S-56): the founder's own outreach has happened — “they are good with the positions as they are … Jack has stated he is willing and also Alan as said yes to being my advisor”; willingness and role consent confirmed; the initial willingness / role-consent outreach item is closed; not a signed agreement; no compensation, IP or employment terms; role wording unchanged. TBD: Crunkleton's three bio items.", "D4; Team page; deck slide 11; one-pager; DoW v2.1 §6; Safe Release §8; the two held drafts", "closed (founder)"),
    P("F10", "Contact: ian@energywave.ai fully configured in Outlook (founder report); the forwarding / Send-As question is retired; the prepared signature reported saved and verified in Outlook by GPT. No send or delivery test. TBD: the letterhead address (B-8).", "D5; DoW v2.1 header; Safe Release letterhead; drafts' From lines; internal-ops README", "closed (founder)"),
    P("F11", "No assistant outreach to Alan Crunkleton or Jack Sarfatti: the 15 Oct HOLD barred it, and on 16 Oct the founder confirmed that his own outreach has happened (S-56) — the founder is not asked again, no consent-request email is sent, no new outreach; their drafts preserved unsent as records; earlier Grok reviews are dated records of exact drafts, not send authority; no address lookup.", "H-1, H-2; internal-ops README; Team page; Seed deck and one-pager", "standing instruction"),
    P("F13", "Series A updated as directed (16 Oct 2026, S-55, S-57: “Please update the Series A accordingly”, read with “Doesn't it make sense to have him at five hundred k W2?”): the dated derivative EnergyWave_Raise_Model_v1.2_2026-10-16.xlsx carries Chip Story's row at $500,000 W-2 (payroll load applied; status From Ian, interpretation flagged), a Mike Wentz note (not modeled), a README change record; recalculated in full; v1.1-corrected untouched. Base effect: plan $18,453,008; raise $22,143,610; gates $6,987,330 / $13,719,010 / $22,143,610 — model outputs on placeholder inputs. [TBD]: whether Chip's agreement is one of the two $500k physicist agreements or additional; his time commitment and cash / equity split; Mike Wentz's title, type, base and start in the model.", "Series A folder (v1.2 workbook, README); Raise Model Note; Series A outline §2a; deck slides 8–9; one-pager; D8; ledger §E", "closed (founder); fields TBD"),
    P("F14", "EnergyWave Final is the living presentation link (16 Oct 2026, S-58; D13): the collection is rebuilt from the sources on every pin (src/build/build_final.py) in projected language — what is projected (the forecast model v1.2), planned or set with counsel — with no marker, tag, source block, reviewer name or internal reference; the orange [TBD] / [Pending] regime governs the internal package only; the Delaware C corporation is stated as in formation with K&L Gates (founder's statement). A projection never resolves a fact the internal page leaves open. GPT/Lyra installs the tree into the nine collection folders and moves the Review Records and the r4.1 snapshot out of the shared link. Sending the link is the founder's action; counsel's 506(b)/(c) answer (C-1) governs whether it may reach anyone the company has not spoken with — put to the founder once, not re-raised.", "EnergyWave_Final/; DELIVERY_MAP.md; mirror instructions §7; README Rule 12; REVIEW_PROTOCOL item 8; D13", "closed (founder); installation GPT/Lyra"),
    P("F12", "Keep the format and other content as they are; no more questions; mark unresolved fields with the exact bracketed [TBD] in orange ink (“make the TBD in brackets [TBD] and in orange ink”, superseding the earlier marker wording). [TBD] is not resolved, signed or verified; originals, dated quotes, historical figures, scientific thresholds and hashes are preserved.", "every page; this register; README Rule 11; REVIEW_PROTOCOL item 7; D8, D10, D11 marked TBD", "closed (founder)"),
]
rows_T = [P("T-1", "Verify the current xTech attachment (artifact 262231) before the close: download it, hash it (expected 90823d62…fea1, 123,643 bytes), confirm the cover reads ≈ USD 10,000 under Capital Raised Total — the 9 Oct record as submitted, which the 15 Oct no-funding statement does not change — with no private-review banner and none of the six blank cover fields; re-upload the approved replacement if not. Record the hash and time seen; who applied the 9–14 Oct changes, whether Beacon/Muse made the submission and whether the evaluators' frozen version is known stay [TBD] unless noted. Nothing on the portal is changed by this package.", "90_Internal_Ops_NOT_FOR_CIRCULATION/2026-10-15_xtech-attachment-verification_checklist.md; D7; xTech Submission Record §3 and §5", "Ian (an action, not a question)")]
rows_C += [
    P("C-1", "Securities: Rule 506(b) or 506(c) for the capital-readiness financing (instrument [TBD]; the Oct-13 materials proposed a $60,000 SAFE; none executed) and for the seed round — no deck reaches an investor who has not heard from the company first until answered; escrow structure for Tranches B and C; any CFIUS / FIRRMA consideration.", "counsel question set §C; SAFE Term Summary; Seed deck slide 14; structure page", "counsel"),
    P("C-2", "Formation: the four confirmations; the 1988 Delaware “EnergyWave Inc.” #2149394; the filing itself (K&L Gates handling — founder, 15 Oct), then the certificate and file number.", "counsel question set §A; Legal page §1", "counsel"),
    P("C-3", "Patent: the current Patent Center docket for 63/763,998 and any later filing; the coversheet provisional in the inventors' names and what “some app and claim prep” covers; the ALG IP Assignment (Exhibit A, blank signature line), the July 2025 NDA and the Integrated Protective Rider reviewed against the EnergyWave work; assignment of energywave.ai and existing work product on formation; a freedom-to-operate note on the Haisch–Moddel / Jovion patents (ledger L-04) and thread B.", "counsel question set §B; Legal page §§2–4", "counsel"),
    P("C-4", "People and naming: consent to name K&L Gates, Novak and Majewski with their exact titles; advisor and team-member agreements; a 409A before any option grant; co-founder terms and the ZPEPG IP boundary.", "counsel question set §E; Team and Counsel", "counsel"),
    P("C-5", "Security posture: the AT-posture memo's §8 questions (trade-secret program; patent versus trade secret by compartment; Invention Secrecy Act exposure; export classification and deemed exports; CPI / AT obligations under federal funding; NDAs and departure procedures).", "counsel question set §F; Compartmentalization & AT Posture v0.1 §8", "counsel"),
]
rows_H = [
    P("H-1", "Alan Crunkleton — advisor; role consent confirmed by the founder (S-46) and, on 16 Oct 2026, willingness confirmed by the founder's own outreach (S-56: “Alan as said yes to being my advisor”) — the willingness / role-consent item is closed; no signed instrument; no compensation, IP or employment terms. No assistant outreach: the draft (bio-item confirmation) is overtaken for role consent and preserved unsent, not to be sent as a consent request; the three bio items stay [TBD] on the Team page, the founder's to raise in his own time; the r5.3 Grok verdict is a dated record, not send authority; no address lookup.", "90_Internal_Ops/2026-10-15_consent-request_alan-crunkleton_DRAFT.md; Team page", "no one — closed for consent; the founder, for the [TBD] items"),
    P("H-2", "Jack Sarfatti — team member, in his existing role; role consent confirmed by the founder (S-46) and, on 16 Oct 2026, willingness confirmed by the founder's own outreach (S-56: “Jack has stated he is willing”) — the willingness / role-consent item is closed; no signed instrument; no compensation, IP or employment terms. No assistant outreach: his draft is overtaken for role consent and preserved unsent, not to be sent as a consent request; the printed-wording question stays open on the Team page, the founder's to raise in his own time.", "90_Internal_Ops/2026-10-15_consent-request_jack-sarfatti_DRAFT.md; Team page", "no one — closed for consent; the founder, for the wording"),
]
rows_R = [
    P("R-1", "Delta-check this release from the commit and pin in the handoff, per REVIEW_PROTOCOL.md — r5.8 pins the working changes made after r5.7: the Antigravity r5.6 disposition and Claims Discipline §3 wording, the held counsel and Chip drafts corrected per Grok (unsent), the r5.7 installation receipt, Mike Wentz on the team (S-55), the Alan/Jack confirmation (S-56), the Raise Model v1.2 derivative and the Series A update (S-57), the session handoff and the register generator in src/build/; the slide deck is 16:9 with its own footer line on each slide.", "REVIEW_PROTOCOL.md", "Lyra; Antigravity"),
    P("R-2", "Hash the §F legacy files on the Mac and send the list.", "SOURCE_LEDGER.md §F; mirror instructions", "Antigravity"),
    P("R-3", "Re-review the Chip and counsel drafts if and when the founder authorizes a send — a prior verdict is not clearance of a revised draft; the Alan and Jack drafts are overtaken for role consent (S-56) and stay unsent; verdicts recorded in the folder; none sent.", "90_Internal_Ops README", "Grok (Architect, Compliance)"),
    P("R-4", "Install EnergyWave_Final/ from the pinned commit into the collection's nine folders by DELIVERY_MAP.md (the Guide at the collection root), hash-checked against MANIFEST.md; move the Review Records and the r4.1 snapshot out of the shared link, unchanged, and verify them where they land; rebuild the collection's FILE_MANIFEST.json; one writer at a time.", "DELIVERY_MAP.md; mirror instructions §7", "GPT/Lyra"),
    P("R-5", "Antigravity's “fill in the blank audit” from a scientific structure (founder, 16 Oct 2026, S-58): when received, read in full and recorded in the ledger; each proposed fill is a reviewer suggestion, adopted into a page only with a source or the founder's direction — never written into a marker on its own authority.", "SOURCE_LEDGER.md §B; the affected pages", "Antigravity (audit); Claude (disposition)"),
]
rows_E = [
    P("E-1", "When a [TBD] field is filled, a consent arrives or counsel answers: fill the marker, re-render the affected pages, bump the version, rebuild the manifest, commit, push, and hand the new pin to the reviewers.", "—", "Claude"),
    P("E-2", "Fold GPT/Codex's operating-requirements register into the Technical Docs hub when received (B-12); draft the supersession note if the 2025 paper's distribution is confirmed (D11); draft the Series A files when the cap table and deck are located or rebuilt (B-3); place the QVE Engine inventory in the ledger when reachable (B-9).", "—", "Claude"),
    P("E-3", "Update DELIVERY_MAP.md whenever a file enters or leaves the collection, in the same commit as the pin.", "—", "Claude"),
    P("E-4", "Before every pin: python3 src/build/build_final.py (fail-closed), then render, probes, lint, manifest, verify; a new marker in a page source needs its data-proj text in the same edit, or the presentation render refuses.", "—", "Claude"),
]
SECTIONS = [
    ("0 · Time-critical — before Monday 19 October 2026, 21:00 UTC (2:00 PM Pacific)", "The xTech Search 10 portal is editable until the close. This is an action on the checklist, not a question.", rows_T),
    ("A · The founder's decisions of 15 October 2026 — applied and closed (ledger S-44, S-46, S-47)", "Founder statements and authoring directions relayed by GPT; not independent bank, registry, contractual, institutional or recipient verification. Each row names where it was applied and what stays [TBD].", rows_F),
    ("B · [TBD] fields, by document — the literal markers, where each one sits", "[TBD] — the exact bracketed marker in orange ink, as the founder asked on 15 Oct 2026 — stands for a current amount, term, role or detail not yet determined. It identifies an unresolved field; it establishes no term, result, agreement or submission clearance; and no further question is asked of the founder about it. He fills these in his own time.", rows_B),
    ("C · Pending from counsel or a named person", "Evidence, consent or an action owed by someone other than the founder. Drafted question sets are not sent; nothing here authorizes outreach.", rows_C),
    ("D · Holds", "An express instruction not to act — and, for Alan and Jack, the record that the founder's own outreach has closed the willingness / role-consent item (16 Oct 2026, S-56).", rows_H),
    ("E · For the reviewers (GPT / Lyra, Antigravity, Grok, Gemini / Argon)", "GPT/Lyra audited r5 (S-39), delta-checked r5.2 (S-40), closed r5.3 (S-41), delivered the founder decisions (S-44, S-46, S-56), audited r5.6 (S-48) and accepted and installed r5.7 (S-51, S-54); Antigravity reviewed r5.6 (S-49, read with S-50); each later release gets its own delta check against its pin.", rows_R),
    ("F · What the lead closes without further input, once the inputs arrive", "Held by the lead; listed so the sequence is visible.", rows_E),
]
n_open = sum(len(rows) for label, _, rows in SECTIONS if not label.startswith("A ·"))
n_dec = len(rows_F)
TH = '<thead><tr><th style="width:6%">#</th><th>Item</th><th style="width:27%">Where it lands</th><th style="width:13%">Who</th></tr></thead>'
H = [f'''<!doctype html><html><head><meta charset="utf-8">
<meta name="dd-output" content="EnergyWave_Open_Items_Register_2026-10-15.pdf">
<meta name="dd-title" content="Open Items Register">
<meta name="dd-version" content="{VER}">
<link rel="stylesheet" href="_style.css">
<style>table {{ table-layout: fixed; }} td {{ overflow-wrap: anywhere; word-break: break-word; }} td.muted {{ font-size: 7.8pt; }} .label, p.muted, thead {{ break-after: avoid; page-break-after: avoid; }}</style></head><body class="compact">
<div class="masthead"><img src="../assets/wordmark_blue.png" alt="Energy Wave">
<div class="meta"><b>energywave.ai</b> • Open Items Register — the founder’s decisions as applied, every [TBD] field, every pending item<br>15 October 2026 · {VER}</div></div>
<div class="status">Confidential — Draft — For Discussion · <span class="flag">{n_open} open items · {n_dec} founder decisions applied · no question is asked of the founder</span></div>

<h1>What was decided, what is <span class="need">[TBD]</span>, what is pending. <span class="sub">Who holds each item, and where it lands.</span></h1>
<p class="lead">On 15 October 2026 the founder gave his decisions (ledger S-44, S-46, S-47), asked that unresolved fields be marked with the exact bracketed <span class="need"><b>[TBD]</b></span> in orange ink, and asked that no further questionnaire follow. This register therefore asks the founder nothing. It records, in order: the one time-critical action; the founder’s decisions as applied (closed); every <span class="need"><b>[TBD]</b></span> marker by document, exactly as it appears; every <span class="need">[Pending: …]</span> item owed by counsel or a named person; the holds; and the reviewer and lead operations. [TBD] identifies an unresolved field and establishes no term, result, agreement or submission clearance. A marker that is not listed here is a finding. The same list is kept as <b>NEEDS_INPUT.md</b> at the root of the package (file name kept for continuity).</p>
<div class="box warn"><b>One item is time-critical:</b> T-1, the xTech Search 10 attachment, before Monday 19 October 2026, 21:00 UTC. Everything else is gated by circulation, not by a clock.</div>
''']
M = [f"# Open Items Register — the founder’s decisions as applied, every [TBD] field, every pending item\n\n**Package version:** `{VER}` · **Open items:** {n_open} · **Founder decisions applied:** {n_dec} · No question is asked of the founder.\n\nOn 15 October 2026 the founder gave his decisions (ledger S-44, S-46, S-47), asked that unresolved fields be marked with the exact bracketed **[TBD]** in orange ink, and asked that no further questionnaire follow. This register therefore asks the founder nothing. It records, in order: the one time-critical action; the founder’s decisions as applied (closed); every `[TBD]` marker by document, exactly as it appears (with the field it stands for after a dash); every `[Pending: …]` item owed by counsel or a named person; the holds; and the reviewer and lead operations. [TBD] identifies an unresolved field and establishes no term, result, agreement or submission clearance. A marker that is not listed here is a finding. The rendered twin of this file is `EnergyWave_Open_Items_Register_2026-10-15.pdf`, where every marker is printed in orange ink (this file keeps its name for continuity).\n\n**Time-critical:** T-1 before **Monday 19 October 2026, 21:00 UTC**. Everything else is gated by circulation, not by a clock.\n"]
for label, intro, rows in SECTIONS:
    H.append(f'<div class="label">{html.escape(label, quote=False)}</div>\n<p class="muted">{html.escape(intro, quote=False)}</p>\n<table>\n{TH}\n<tbody>\n')
    M.append(f"\n## {label}\n\n{intro}\n\n| # | Item | Where it lands | Who |\n|---|---|---|---|\n")
    for rid, th_, tm, lands, who in rows:
        H.append(f'<tr><td><b>{rid}</b></td><td>{th_}</td><td class="muted">{html.escape(lands, quote=False)}</td><td>{html.escape(who, quote=False)}</td></tr>\n')
        M.append(f"| **{rid}** | {tm} | {lands} | {who} |\n")
    H.append("</tbody></table>\n")
H.append('\n<div class="sources">Sources: the marked pages in src/pages/; DECISIONS.md D1–D12; SOURCE_LEDGER.md §D, §F, S-36–S-58; 90_Internal_Ops_NOT_FOR_CIRCULATION/; DELIVERY_MAP.md; REVIEW_PROTOCOL.md; the founder decisions of 15 Oct 2026 (S-44, S-46, S-47). This register is generated from the markers; a marker that is not here is a finding.</div>\n</body></html>\n')
write("src/pages/18_Needs_Input_Register.html", wrap_html("".join(H)))
M.append("\nGenerated from the `[TBD]` and `[Pending: …]` markers in `src/pages/`, `DECISIONS.md`, `SOURCE_LEDGER.md` §D/§F, `90_Internal_Ops_NOT_FOR_CIRCULATION/` and `DELIVERY_MAP.md`, and from the founder decisions of 15 Oct 2026 (S-44, S-46, S-47). A marker that is not here is a finding.\n")
write("NEEDS_INPUT.md", conv_md("".join(M)))
print(f"register: {n_open} open items, {n_dec} decisions; B rows {len(rows_B)}, C rows {len(rows_C)}")
