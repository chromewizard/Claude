#!/usr/bin/env python3
"""Read-only verification of a mirror against a TRUSTED manifest.

Never writes. Exit 0 only when:
  - the manifest's own hash matches --expect-manifest-sha256 (when given);
  - every payload entry exists with the recorded size and SHA-256;
  - no payload file is missing and no unexpected payload file is present —
    "payload" is every file under the root except the recognized control
    files at exactly <root>/tools/ (nested directories named "tools" are
    payload; unlisted files inside <root>/tools/ are reported as EXTRA);
  - every control file pinned in the manifest is present and matches,
    unless --payload-only is given (then controls are not required, but any
    that are present must still match).

Usage:
  python3 tools/verify_manifest.py --manifest /trusted/manifest.json --root /path/to/mirror
         [--expect-manifest-sha256 HEX] [--payload-only] [--json OUT.json]

The control-file policy is identical to build_manifest.py and lint.py.
"""
import argparse
import hashlib
import json
import os
import sys

CONTROL_DIR = "tools"
CONTROL_FILES = ("lint.py", "lint.sh", "build_manifest.py", "verify_manifest.py",
                 os.path.join("tests", "run_probes.py"))
EXCLUDED_NAMES = {"manifest.json", "MANIFEST.md", ".DS_Store"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--expect-manifest-sha256")
    ap.add_argument("--payload-only", action="store_true",
                    help="do not require the pinned control files to be present")
    ap.add_argument("--json")
    args = ap.parse_args(argv)

    root = os.path.abspath(args.root)
    mpath = os.path.abspath(args.manifest)
    result = {"root": root, "manifest": mpath, "mode": "payload-only" if args.payload_only else "full",
              "ok": False, "manifest_sha256": None, "verified": [], "mismatched": [], "missing": [],
              "extra": [], "controls": []}

    if not os.path.isfile(mpath):
        print(f"VERIFY ERROR — manifest not found: {mpath}")
        return 2
    result["manifest_sha256"] = sha256(mpath)
    if args.expect_manifest_sha256 and args.expect_manifest_sha256.lower() != result["manifest_sha256"]:
        print(f"VERIFY FAIL — manifest hash {result['manifest_sha256']} != expected {args.expect_manifest_sha256}")
        return 1
    with open(mpath) as f:
        manifest = json.load(f)

    # payload entries
    expected = {e["path"]: e for e in manifest.get("files", [])}
    for rel, e in sorted(expected.items()):
        p = os.path.join(root, rel)
        if not os.path.isfile(p):
            result["missing"].append(rel)
            continue
        size, digest = os.path.getsize(p), sha256(p)
        if size != e["bytes"] or digest != e["sha256"]:
            result["mismatched"].append({"path": rel, "expected": e["sha256"], "actual": digest,
                                         "expected_bytes": e["bytes"], "actual_bytes": size})
        else:
            result["verified"].append(rel)

    # unexpected payload files: everything except the recognized control files at <root>/tools/
    control_abs = {os.path.join(root, CONTROL_DIR, c) for c in CONTROL_FILES}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        for fn in sorted(filenames):
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root)
            if fn in EXCLUDED_NAMES and dirpath == root:
                continue
            if p in control_abs:
                continue
            if rel not in expected:
                result["extra"].append(rel)

    # pinned control files
    pinned = manifest.get("controls", [])
    for c in pinned:
        p = os.path.join(root, c["path"])
        if os.path.isfile(p):
            actual = sha256(p)
            result["controls"].append({"path": c["path"], "state": "ok" if actual == c["sha256"] else "MISMATCH",
                                       "actual": actual})
        else:
            result["controls"].append({"path": c["path"], "state": "ABSENT", "actual": None})
    control_fail = any(c["state"] == "MISMATCH" for c in result["controls"]) or \
        (not args.payload_only and any(c["state"] == "ABSENT" for c in result["controls"]))

    result["ok"] = not (result["missing"] or result["mismatched"] or result["extra"] or control_fail)

    if args.json:
        with open(args.json, "w") as f:
            json.dump(result, f, indent=2)
            f.write("\n")

    print(f"root: {root}  mode: {result['mode']}")
    print(f"manifest: {mpath}  sha256 {result['manifest_sha256']}  version {manifest.get('version')}")
    print(f"verified {len(result['verified'])} / {len(expected)} payload files")
    for m in result["mismatched"]:
        print(f"  MISMATCH {m['path']}: expected {m['expected'][:16]}… ({m['expected_bytes']} B) got {m['actual'][:16]}… ({m['actual_bytes']} B)")
    for m in result["missing"]:
        print(f"  MISSING  {m}")
    for x in result["extra"]:
        print(f"  EXTRA    {x}")
    for c in result["controls"]:
        print(f"  control  {c['path']}: {c['state']}")
    print("VERIFY OK — mirror matches the trusted manifest" if result["ok"] else "VERIFY FAIL — mirror does not match the trusted manifest")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
