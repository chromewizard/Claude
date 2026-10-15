# Creating the Desktop and Drive mirrors from the pinned commit — for Ian or Antigravity

The repository is the only verified release location. A mirror is valid only when `tools/verify_manifest.py` passes against the manifest hash pinned in the handoff. Binary files are not uploaded through the assistant's Drive connector (its payload limits make that impractical and it cannot verify the result); the Mac does it in three commands, and the verifier proves the copy.

## 1. Get the pinned commit

```
cd ~/Desktop
git clone https://github.com/chromewizard/Claude.git EnergyWave-DD-src
cd EnergyWave-DD-src
git checkout <COMMIT FROM THE HANDOFF>
```

## 2. Desktop mirror (decision D9 — path to confirm)

```
rsync -a --exclude .git "EnergyWave-DD-src/Due Diligence/" "$HOME/Desktop/Due Diligence/"
```

## 3. Drive mirror

With the Google Drive desktop app signed in to the workspace account, copy the same folder into `Ian + Aura — Shared AI Workspace / Due Diligence /`:

```
rsync -a --exclude .git "EnergyWave-DD-src/Due Diligence/" "<path to the Drive folder>/Due Diligence/"
```

## 4. Verify each mirror — never rebuild

```
cd "EnergyWave-DD-src/Due Diligence"
python3 tools/verify_manifest.py --manifest manifest.json --root "$HOME/Desktop/Due Diligence" --expect-manifest-sha256 <PIN FROM THE HANDOFF>
python3 tools/verify_manifest.py --manifest manifest.json --root "<Drive path>/Due Diligence" --expect-manifest-sha256 <PIN FROM THE HANDOFF>
python3 tools/lint.py --root "$HOME/Desktop/Due Diligence" --json ~/Desktop/dd-lint.json
```

`VERIFY OK` on both, and `LINT OK`, is the release record; paste the three result lines back to the lead. Finder's `.DS_Store` files are ignored by the verifier at any depth.

## 5. Claude Project

Upload `manifest.json`, `MANIFEST.md` and the twenty rendered documents to the *EnergyWave Ops* project knowledge, and link the repository. [Needs Input from Ian or Chip: do this, or give the assistant project-knowledge access]

The text-only skeleton of the Drive folder (READMEs, ledger, decisions, manifest, page sources, this file) is created by the assistant; the verifier will report every binary as MISSING until step 3 runs.
