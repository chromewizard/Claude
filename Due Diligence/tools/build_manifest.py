#!/usr/bin/env python3
"""Build manifest.json and the generated table in MANIFEST.md for the canonical package.

AUTHOR-ONLY. This regenerates the reference; it is not a verification step.
Reviewers and mirrors use tools/verify_manifest.py with the pinned manifest.

Usage (from anywhere):  python3 "Due Diligence/tools/build_manifest.py"
Exit status is non-zero unless the forbidden-label scan returns OK (a match or
an unscanned surface both block the build).
"""
import datetime
import hashlib
import json
import os
import subprocess
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
PACKAGE_VERSION = "DD-2026-10-14-r2-draft"
SKIP_FILES = {"manifest.json", "MANIFEST.md", ".DS_Store"}
CONTROL_FILES = ["tools/lint.py", "tools/lint.sh", "tools/build_manifest.py", "tools/verify_manifest.py",
                 "tools/tests/run_probes.py"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    entries = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d != ".git" and os.path.join(dirpath, d) != TOOLS)
        for fn in sorted(filenames):
            if fn in SKIP_FILES or fn.startswith("."):
                continue
            p = os.path.join(dirpath, fn)
            entries.append({"path": os.path.relpath(p, ROOT), "bytes": os.path.getsize(p), "sha256": sha256(p)})

    lint = subprocess.run([sys.executable, os.path.join(TOOLS, "lint.py"), "--root", ROOT, "--quiet"],
                          capture_output=True, text=True)
    lint_status = {0: "OK", 1: "FAIL", 2: "UNSCANNED"}.get(lint.returncode, f"ERROR({lint.returncode})")
    generated = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    controls = []
    for rel in CONTROL_FILES:
        p = os.path.join(ROOT, rel)
        if os.path.isfile(p):
            controls.append({"path": rel, "bytes": os.path.getsize(p), "sha256": sha256(p)})

    manifest = {
        "package": "EnergyWave Due Diligence",
        "version": PACKAGE_VERSION,
        "generated_utc": generated,
        "lint": lint_status,
        "file_count": len(entries),
        "files": entries,
        "controls": controls,
        "verify": "python3 tools/verify_manifest.py --manifest <trusted manifest.json> --root <mirror> --expect-manifest-sha256 <pinned hash>",
    }
    manifest_path = os.path.join(ROOT, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    mhash = sha256(manifest_path)

    table = ["| # | Path | Bytes | SHA-256 |", "|---|---|---:|---|"]
    for i, e in enumerate(entries, 1):
        table.append(f"| {i} | `{e['path']}` | {e['bytes']:,} | `{e['sha256']}` |")
    ctable = ["| Control | Bytes | SHA-256 |", "|---|---:|---|"]
    for c in controls:
        ctable.append(f"| `{c['path']}` | {c['bytes']:,} | `{c['sha256']}` |")
    block = "\n".join([
        f"**Package version:** {PACKAGE_VERSION}  ",
        f"**Generated (UTC):** {generated}  ",
        f"**Payload files:** {len(entries)}  ",
        f"**Lint:** {lint_status}  ",
        f"**manifest.json SHA-256:** `{mhash}`",
        "",
        *table,
        "",
        "Control code in force for this release (verify with `tools/verify_manifest.py`):",
        "",
        *ctable,
    ])

    md_path = os.path.join(ROOT, "MANIFEST.md")
    with open(md_path) as f:
        md = f.read()
    start, end = "<!-- BEGIN GENERATED -->", "<!-- END GENERATED -->"
    a, b = md.index(start) + len(start), md.index(end)
    with open(md_path, "w") as f:
        f.write(md[:a] + "\n" + block + "\n" + md[b:])

    print(f"manifest: {len(entries)} payload files · lint {lint_status} · manifest.json sha256 {mhash}")
    if lint.returncode != 0:
        sys.stdout.write(lint.stdout + lint.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
