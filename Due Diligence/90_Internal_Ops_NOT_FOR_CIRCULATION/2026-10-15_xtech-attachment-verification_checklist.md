# xTech Search 10 — attachment verification checklist (closes D7) — for Ian

**Deadline:** Monday 19 October 2026, 21:00 UTC (2:00 PM Pacific). The portal remains editable while the program manager has editing enabled.

**What is already observed (14 Oct, read-only, GPT reviewer):** Company Name = McLean Capital Development LLC; secondary contact Chip Story; Previous DoD business = No; exactly the six approved tags; capitalization 0; the materials link shows `McLeanCapitalDevelopmentLLC_xTech_Search10_White_Paper.pdf` at artifact 262231. **Not verified:** that the attachment's bytes are the approved replacement and that its cover reads approximately USD 10,000 under Capital Raised Total.

## Steps

1. Log in: https://usg.valideval.com/app/events/4d0427d3-32e7-4a00-80a5-84979d81a6de/teams/3b2a54ce-1bac-4a62-8331-ebfb6516b088/my_profile
2. Under *Materials Submitted for Evaluation*, download the attached PDF (artifact 262231) to your Mac. Do not click Save Profile or Submit.
3. In Terminal:
   ```
   shasum -a 256 ~/Downloads/McLeanCapitalDevelopmentLLC_xTech_Search10_White_Paper.pdf
   ```
   Expected: `90823d623fb4194eda74ca3560862004254c47a3af851f87987314aa8ca4fea1` (123,643 bytes).
4. Open the PDF. Page 1 must show no "PRIVATE REVIEW - NOT FOR SUBMISSION" banner, no "TBD" fields, and Capital Raised Total ≈ USD 10,000 including founder contributions. (That cover value is the 9 October record as approved and submitted; the founder's 15 Oct statement that no funding has been raised is recorded separately in the package and does not change the submitted record — do not alter it.)
5. If the hash matches and the cover is right: D7 is closed. Tell me the hash you saw and the time; the ledger records it as your observation.
6. If the hash differs or the cover is wrong: replace the attachment with the approved file from `/Users/ian/Documents/Codex/2026-10-08/task/xtechsearch10/McLean Capital Development LLC_xTech_Search10_White_Paper.pdf` (same hash as above), save, and repeat steps 2–4. Do not change any other field.
7. Either way, note who made the 9–14 October changes and when, if you know.

**Also record:** whether the evaluators' frozen version is known to you (the portal does not say).

The two local papers are in the package at `02_DoW/` for comparison; their hashes are in `MANIFEST.md`.
