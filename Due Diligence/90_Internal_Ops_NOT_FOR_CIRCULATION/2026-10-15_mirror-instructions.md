# Placing a release in the EnergyWave Final collection — for Ian or Antigravity (GPT/Lyra verifies and assembles)

The repository is the only verified release location. A copy is valid only when `tools/verify_manifest.py` passes against the manifest hash pinned in the handoff. The release location is resolved (D9): `/Users/ian/Documents/EnergyWave Final/`, with matching copies on OneDrive and in My Drive. Each release goes in its own folder beside the preserved r4.1 snapshot; nothing is overwritten and no duplicate master is created. One writer at a time.

## 1. Get the pinned commit

```
cd ~/Desktop
git clone https://github.com/chromewizard/Claude.git EnergyWave-DD-src
cd EnergyWave-DD-src
git checkout <COMMIT FROM THE HANDOFF>
```

## 2. Place the release in the collection (Mac copy)

```
REL=DD-2026-10-15-r5.7-draft
rsync -a --exclude .git "EnergyWave-DD-src/Due Diligence/" "$HOME/Documents/EnergyWave Final/Due Diligence/$REL/"
```

## 3. Matching copies

```
rsync -a "$HOME/Documents/EnergyWave Final/Due Diligence/$REL/" "$HOME/Library/CloudStorage/OneDrive-mcleancompanies.com/EnergyWave Final/Due Diligence/$REL/"
rsync -a "$HOME/Documents/EnergyWave Final/Due Diligence/$REL/" "$HOME/My Drive/EnergyWave Final/Due Diligence/$REL/"
```

## 4. Verify each copy — never rebuild

```
cd "EnergyWave-DD-src/Due Diligence"
for ROOT in "$HOME/Documents/EnergyWave Final" "$HOME/Library/CloudStorage/OneDrive-mcleancompanies.com/EnergyWave Final" "$HOME/My Drive/EnergyWave Final"; do
  python3 tools/verify_manifest.py --manifest manifest.json --root "$ROOT/Due Diligence/$REL" --expect-manifest-sha256 <PIN FROM THE HANDOFF>
done
python3 tools/lint.py --root "$HOME/Documents/EnergyWave Final/Due Diligence/$REL" --json ~/Desktop/dd-lint.json
```

`VERIFY OK` three times, and `LINT OK`, is the release record; paste the four result lines back to the lead. Finder's `.DS_Store` files are ignored by the verifier at any depth.

## 4a. As actually installed

GPT/Lyra's guarded installation of r5.7 (15 Oct 2026, S-54) placed the canonical bytes under `Review Records/r5.7 Review Candidate/Due Diligence/` in each root rather than under `Due Diligence/$REL/`; the r4.1 snapshot stays under `Due Diligence/`. Either layout is acceptable so long as the verifier passes against the pin and nothing is overwritten.

## 5. Audience folders

GPT/Lyra assembles the nine audience folders (`Capital Readiness` / `Seed Round` / `Series A` × `Government DoW:DoE:DARPA Package` / `Investor Due Dilligence Packet` / `Technical Package`) from `DELIVERY_MAP.md` after review — copies only, each checked against the hash in `MANIFEST.md` — and rebuilds the collection's `FILE_MANIFEST.json` afterwards. Nothing marked DRAFT or INTERNAL in the map goes in an audience folder.

## 6. Claude Project

Ian or Antigravity: upload `manifest.json`, `MANIFEST.md` and the twenty-one rendered documents to the *EnergyWave Ops* project knowledge, and link the repository — an action item, not a question.

## 7. The collection as the living presentation link (founder, 16 Oct 2026, S-58; D13)

From r6 the collection is what investors, Department of War reviewers, collaborators and counsel see at any time, so it holds the presentation build and nothing else outward-facing:

1. **Audience folders.** Copy the contents of `EnergyWave_Final/<round>/<audience>/` from the pinned commit into the nine collection folders by the mapping in `DELIVERY_MAP.md` (repository names → the Mac's names, including “Dilligence”), and `EnergyWave_Final/EnergyWave_Guide_to_these_Materials_2026-10-16.pdf` to the collection root `Due Diligence/`. Replace earlier audience copies; the collection carries one edition at a time. Verify every copied file's SHA-256 against `MANIFEST.md` (the `EnergyWave_Final/…` rows).
2. **Working records leave the shared link.** `Review Records/` (the r5.7 canonical bytes) and the preserved `Due Diligence/DD-2026-10-15-r4.1-draft/` snapshot are working records, not presentation materials. Move them, unchanged, out of `EnergyWave Final` to a non-shared working location (for example `~/Documents/EnergyWave Working/`) in each of the three roots, and verify each moved tree against its own pinned manifest after the move. Nothing is deleted.
3. **Rebuild** the collection's `FILE_MANIFEST.json`; paste the verification lines back to the lead.
4. **Sharing** the link is the founder's action. Before the link goes to anyone the company has not spoken with, counsel's answer on the securities exemption (Rule 506(b) or 506(c)) governs (counsel question set §C; D13); K&L Gates is the first intended recipient.
5. **Never edit a file in the collection.** A correction is made in the page source, the tree is rebuilt with `python3 src/build/build_final.py`, the release re-pinned, and the changed files copied again.

