"""Path helpers for the build scripts in this directory. ROOT is the package root (the Due Diligence folder)."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def sub(path, old, new, count=1):
    """Replace exactly one occurrence of old with new in the file at path (relative to ROOT); fail loudly otherwise."""
    p = os.path.join(ROOT, path)
    s = open(p, encoding="utf-8").read()
    n = s.count(old)
    if n == 0:
        raise SystemExit(f"MISSING in {path}: {old[:140]!r}")
    if count == 1 and n > 1:
        raise SystemExit(f"AMBIGUOUS ({n}) in {path}: {old[:140]!r}")
    s = s.replace(old, new) if count == -1 else s.replace(old, new, count)
    open(p, "w", encoding="utf-8").write(s)

def read(path):
    return open(os.path.join(ROOT, path), encoding="utf-8").read()

def write(path, s):
    open(os.path.join(ROOT, path), "w", encoding="utf-8").write(s)
