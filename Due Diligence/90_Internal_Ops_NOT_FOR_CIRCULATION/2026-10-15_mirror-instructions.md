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
REL=DD-2026-10-15-r5.1-draft
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

## 5. Audience folders

GPT/Lyra assembles the nine audience folders (`Capital Readiness` / `Seed Round` / `Series A` × `Government DoW:DoE:DARPA Package` / `Investor Due Dilligence Packet` / `Technical Package`) from `DELIVERY_MAP.md` after review — copies only, each checked against the hash in `MANIFEST.md` — and rebuilds the collection's `FILE_MANIFEST.json` afterwards. Nothing marked DRAFT or INTERNAL in the map goes in an audience folder.

## 6. Claude Project

Upload `manifest.json`, `MANIFEST.md` and the twenty rendered documents to the *EnergyWave Ops* project knowledge, and link the repository. [Needs Input from Ian or Chip: do this, or give the assistant project-knowledge access]
