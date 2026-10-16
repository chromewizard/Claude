#!/usr/bin/env python3
"""Checks every rendered presentation PDF under EnergyWave_Final/ for internal language.

The rules are src/build/final_banned.json — the same list src/render.js applies to the page text before it renders;
this check reads the text back out of the PDFs (pdftotext), so a reviewer or a mirror can repeat it without the
renderer. Only the pages rendered for the collection (names ending _2026-10-16.pdf) are checked; the approved
originals and the forecast model are placed byte for byte and are not rewritten.

Usage (from anywhere):  python3 "Due Diligence/src/build/check_final.py" [--root <EnergyWave_Final>]
Exit 0 = clean; 1 = a hit (each is printed with context); 2 = a PDF could not be read.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))


def main():
    root = os.path.join(ROOT, "EnergyWave_Final")
    if "--root" in sys.argv:
        root = sys.argv[sys.argv.index("--root") + 1]
    rules = []
    for src, flags in json.load(open(os.path.join(HERE, "final_banned.json"), encoding="utf-8")):
        rules.append(re.compile(src, re.I if "i" in (flags or "") else 0))
    hits, unread, checked = [], [], 0
    for dirpath, _, filenames in os.walk(root):
        for fn in sorted(filenames):
            if not fn.endswith("_2026-10-16.pdf"):
                continue
            p = os.path.join(dirpath, fn)
            r = subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True)
            if r.returncode != 0:
                unread.append(p)
                continue
            text = re.sub(r"\s+", " ", r.stdout)
            checked += 1
            for rule in rules:
                m = rule.search(text)
                if m:
                    i = m.start()
                    hits.append(f"{os.path.relpath(p, root)}: {m.group(0)!r} … {text[max(0, i - 60):i + 60]}")
    for h in hits:
        print("HIT ", h)
    for u in unread:
        print("UNREAD", u)
    if unread:
        return 2
    print(f"check_final: {checked} presentation PDFs checked, {len(hits)} hit(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
