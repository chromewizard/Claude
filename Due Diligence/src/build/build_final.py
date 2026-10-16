#!/usr/bin/env python3
"""Builds EnergyWave_Final/ — the presentation collection — from the one source, every time from empty.

  1. removes every file under EnergyWave_Final/ (a build output, never edited by hand);
  2. runs `node src/render.js --final`: every page with a dd-final meta is rendered in presentation form into
     its dd-final-folders (fail-closed: a marker without projected text or any internal language refuses the render);
  3. copies the approved originals and the forecast model listed in ORIGINALS into their folders, byte for byte,
     and verifies each copy's SHA-256 against its source;
  4. runs check_final.py over every rendered presentation PDF (the same banned-language rules, on the extracted text).

Usage (from anywhere):  python3 "Due Diligence/src/build/build_final.py"
Exit status is non-zero if any step fails. The nine folders are
  {1_Capital_Readiness, 2_Seed_Round, 3_Series_A} × {Investor_Package, Government_Package, Technical_Package}
and map onto the EnergyWave Final collection's folders on the Mac (DELIVERY_MAP.md gives the exact names).
"""
import hashlib
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
FINAL = os.path.join(ROOT, "EnergyWave_Final")
INV = ["1_Capital_Readiness/Investor_Package", "2_Seed_Round/Investor_Package", "3_Series_A/Investor_Package"]
GOV = ["1_Capital_Readiness/Government_Package", "2_Seed_Round/Government_Package", "3_Series_A/Government_Package"]
TEC = ["1_Capital_Readiness/Technical_Package", "2_Seed_Round/Technical_Package", "3_Series_A/Technical_Package"]

# (source path in the canonical package, published name in the Final folders, folders)
ORIGINALS = [
    ("01_Investor/01_Capital_Readiness/EnergyWave_Deck_2026-10-13.pdf", "EnergyWave_Deck_2026-10-13.pdf", ["1_Capital_Readiness/Investor_Package"]),
    ("01_Investor/01_Capital_Readiness/EnergyWave_OnePager_2026-10-13.pdf", "EnergyWave_OnePager_2026-10-13.pdf", ["1_Capital_Readiness/Investor_Package"]),
    ("02_DoW/EnergyWave_xTech_Search10_Paper_APPROVED_REPLACEMENT_2026-10-09.pdf", "McLean Capital Development LLC_xTech_Search10_White_Paper.pdf", GOV),
    ("02_DoW/EnergyWave_Compartmentalization_AT_Posture_v0.1_2026-09-12.pdf", "EnergyWave_Compartmentalization_AT_Posture_v0.1_2026-09-12.pdf", GOV),
    ("03_Technical_Documents/EnergyWave_Physical_Architecture_and_Baseline_Model_v1.3_2026-10-05.pdf", "EnergyWave_Physical_Architecture_and_Baseline_Model_v1.3_2026-10-05.pdf", TEC),
    ("01_Investor/03_Series_A/EnergyWave_Raise_Model_v1.2_2026-10-16.xlsx", "EnergyWave_Raise_Model_v1.2_2026-10-16.xlsx", ["3_Series_A/Investor_Package"]),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    # 1. empty the build output
    if os.path.isdir(FINAL):
        for dirpath, dirnames, filenames in os.walk(FINAL, topdown=False):
            for fn in filenames:
                os.remove(os.path.join(dirpath, fn))
            for d in dirnames:
                os.rmdir(os.path.join(dirpath, d))
    os.makedirs(FINAL, exist_ok=True)
    # 2. presentation renders
    r = subprocess.run(["node", os.path.join(ROOT, "src", "render.js"), "--final"], cwd=ROOT)
    if r.returncode != 0:
        print("BUILD REFUSED — a presentation render failed (see above)")
        return 1
    # 3. originals
    for src, name, folders in ORIGINALS:
        sp = os.path.join(ROOT, src)
        if not os.path.isfile(sp):
            print("BUILD REFUSED — original missing:", src)
            return 1
        h = sha256(sp)
        for folder in folders:
            d = os.path.join(FINAL, folder)
            os.makedirs(d, exist_ok=True)
            dp = os.path.join(d, name)
            shutil.copyfile(sp, dp)
            if sha256(dp) != h:
                print("BUILD REFUSED — copy differs from its source:", dp)
                return 1
        print("placed  ", name, "→", ", ".join(folders))
    # 4. language check on the rendered presentation PDFs
    r = subprocess.run([sys.executable, os.path.join(HERE, "check_final.py")], cwd=ROOT)
    if r.returncode != 0:
        print("BUILD REFUSED — check_final.py found internal language")
        return 1
    n = sum(len(f) for _, _, f in os.walk(FINAL))
    print(f"EnergyWave_Final built: {n} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
