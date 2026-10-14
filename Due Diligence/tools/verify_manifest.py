#!/usr/bin/env python3
"""Read-only verification of a mirror against a TRUSTED manifest.

Never writes. Exit 0 only when every manifest entry exists with the recorded
size and SHA-256, no payload file is missing, and no unexpected payload file is
present. Control-code digests recorded in the manifest are checked when the
mirror carries a tools/ directory.

Usage:
  python3 tools/verify_manifest.py --manifest /trusted/manifest.json --root /path/to/mirror
         [--expect-manifest-sha256 HEX] [--json OUT.json]

Pass --expect-manifest-sha256 with the hash pinned in the handoff so a tampered
or regenerated manifest is rejected before any file is compared.
"""
import argparse
import hashlib
import json
import os
import sys

EXCLUDED = {"manifest.json", "MANIFEST.md", ".DS_Store"}


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
    ap.add_argument("--json")
    args = ap.parse_args(argv)

    root = os.path.abspath(args.root)
    mpath = os.path.abspath(args.manifest)
    result = {"root": root, "manifest": mpath, "ok": False, "manifest_sha256": None,
              "verified": [], "mismatched": [], "missing": [], "extra": [], "controls": []}

    if not os.path.isfile(mpath):
        print(f"VERIFY ERROR — manifest not found: {mpath}")
        return 2
    result["manifest_sha256"] = sha256(mpath)
    if args.expect_manifest_sha256 and args.expect_manifest_sha256.lower() != result["manifest_sha256"]:
        print(f"VERIFY FAIL — manifest hash {result['manifest_sha256']} != expected {args.expect_manifest_sha256}")
        return 1
    with open(mpath) as f:
        manifest = json.load(f)

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

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in (".git", "tools"))
        for fn in sorted(filenames):
            if fn in EXCLUDED:
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), root)
            if rel not in expected:
                result["extra"].append(rel)

    for c in manifest.get("controls", []):
        p = os.path.join(root, c["path"])
        if os.path.isfile(p):
            actual = sha256(p)
            result["controls"].append({"path": c["path"], "ok": actual == c["sha256"], "actual": actual})
        else:
            result["controls"].append({"path": c["path"], "ok": None, "actual": None})

    bad_controls = [c for c in result["controls"] if c["ok"] is False]
    result["ok"] = not (result["missing"] or result["mismatched"] or result["extra"] or bad_controls)

    if args.json:
        with open(args.json, "w") as f:
            json.dump(result, f, indent=2)
            f.write("\n")

    print(f"root: {root}")
    print(f"manifest: {mpath}  sha256 {result['manifest_sha256']}  version {manifest.get('version')}")
    print(f"verified {len(result['verified'])} / {len(expected)} payload files")
    for m in result["mismatched"]:
        print(f"  MISMATCH {m['path']}: expected {m['expected'][:16]}… ({m['expected_bytes']} B) got {m['actual'][:16]}… ({m['actual_bytes']} B)")
    for m in result["missing"]:
        print(f"  MISSING  {m}")
    for x in result["extra"]:
        print(f"  EXTRA    {x}")
    for c in result["controls"]:
        state = "ok" if c["ok"] else ("MISMATCH" if c["ok"] is False else "absent")
        print(f"  control  {c['path']}: {state}")
    print("VERIFY OK — mirror matches the trusted manifest" if result["ok"] else "VERIFY FAIL — mirror does not match the trusted manifest")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
