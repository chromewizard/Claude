#!/usr/bin/env python3
"""Build manifest.json and the generated table in MANIFEST.md for the Due Diligence package.

Usage (from anywhere):  python3 "Due Diligence/tools/build_manifest.py"
Exit status is non-zero if the forbidden-label lint fails, so a release cannot be
built with a forbidden label in it.
"""
import datetime
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGE_VERSION = "DD-2026-10-14-r1-draft"
SKIP_DIRS = {"tools", ".git"}
SKIP_FILES = {"manifest.json", "MANIFEST.md"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    entries = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for fn in sorted(filenames):
            if fn in SKIP_FILES or fn.startswith("."):
                continue
            p = os.path.join(dirpath, fn)
            entries.append({
                "path": os.path.relpath(p, ROOT),
                "bytes": os.path.getsize(p),
                "sha256": sha256(p),
            })

    lint = subprocess.run(["bash", os.path.join(ROOT, "tools", "lint.sh")],
                          capture_output=True, text=True)
    lint_ok = lint.returncode == 0
    generated = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    manifest = {
        "package": "EnergyWave Due Diligence",
        "version": PACKAGE_VERSION,
        "generated_utc": generated,
        "lint": "OK" if lint_ok else "FAIL",
        "file_count": len(entries),
        "files": entries,
    }
    manifest_path = os.path.join(ROOT, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    mhash = sha256(manifest_path)

    table = ["| # | Path | Bytes | SHA-256 |", "|---|---|---:|---|"]
    for i, e in enumerate(entries, 1):
        table.append(f"| {i} | `{e['path']}` | {e['bytes']:,} | `{e['sha256']}` |")
    block = "\n".join([
        f"**Package version:** {PACKAGE_VERSION}  ",
        f"**Generated (UTC):** {generated}  ",
        f"**Files:** {len(entries)}  ",
        f"**Lint:** {'OK' if lint_ok else 'FAIL'}  ",
        f"**manifest.json SHA-256:** `{mhash}`",
        "",
        *table,
    ])

    md_path = os.path.join(ROOT, "MANIFEST.md")
    with open(md_path) as f:
        md = f.read()
    start, end = "<!-- BEGIN GENERATED -->", "<!-- END GENERATED -->"
    a, b = md.index(start) + len(start), md.index(end)
    with open(md_path, "w") as f:
        f.write(md[:a] + "\n" + block + "\n" + md[b:])

    print(f"manifest: {len(entries)} files · lint {'OK' if lint_ok else 'FAIL'} · manifest.json sha256 {mhash}")
    if not lint_ok:
        sys.stdout.write(lint.stdout + lint.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
