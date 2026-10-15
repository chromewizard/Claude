#!/usr/bin/env python3
"""Forbidden-label scan for the EnergyWave Due Diligence package.

Fail-closed. Exit codes:
  0  every file fully scanned, nothing matched
  1  a forbidden label was found (path, text, PDF text/metadata, Office XML,
     archive member name, nested archive, raw bytes)
  2  nothing matched, but at least one surface could not be scanned (missing
     extractor, unreadable archive, extraction error) — not a pass

Usage:
  python3 tools/lint.py [--root DIR] [--json OUT.json] [--quiet]

--root defaults to the package directory that contains this tools/ folder.
The resolved root, the file count and the number of recognized control files
skipped are always printed, so a run can never silently certify the wrong
directory.

Control-file policy (target-aware, shared with build_manifest.py and
verify_manifest.py): the only files not scanned are the recognized control
files at exactly <root>/tools/{lint.py, lint.sh, build_manifest.py,
verify_manifest.py, tests/run_probes.py}. Every other file under
<root>/tools/ and every nested directory named "tools" is scanned. The policy
depends on the selected root, not on where this script lives, so a trusted
external copy of the scanner gives the same result as the mirror's own copy.
The pattern lives only in this file. Python 3.8+ standard library;
pdftotext/pdfinfo/pdfdetach (poppler) are required for PDFs and their absence
is reported as UNSCANNED, never as a pass.
"""
import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from xml.etree import ElementTree as ET

PATTERN = re.compile(r"pharaoh", re.IGNORECASE)
PATTERN_BYTES = re.compile(rb"pharaoh", re.IGNORECASE)

# Shared control-file policy. Keep identical in build_manifest.py and verify_manifest.py.
CONTROL_DIR = "tools"
CONTROL_FILES = ("lint.py", "lint.sh", "build_manifest.py", "verify_manifest.py",
                 os.path.join("tests", "run_probes.py"))

OOXML_EXT = {".docx", ".xlsx", ".pptx", ".dotx", ".xltx", ".potx", ".docm", ".xlsm", ".pptm"}
ZIP_EXT = {".zip"}
PDF_EXT = {".pdf"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".tif", ".tiff", ".bmp", ".heic", ".svg", ".ico"}

MIN_TEXT_CHARS_PER_PAGE = 20  # below this a PDF is treated as image-only → visual review


def control_paths(root):
    """Absolute paths of the recognized control files for the package at root."""
    return {os.path.join(root, CONTROL_DIR, rel) for rel in CONTROL_FILES}


class Report:
    def __init__(self, root):
        self.root = root
        self.files = 0
        self.controls_skipped = []
        self.matches = []        # {"file", "surface", "evidence"}
        self.unscanned = []      # {"file", "surface", "reason"}
        self.visual_review = []  # {"file", "surface", "note"}
        self.tools = {t: shutil.which(t) for t in ("pdftotext", "pdfinfo", "pdfdetach")}

    def match(self, file, surface, evidence):
        self.matches.append({"file": file, "surface": surface, "evidence": evidence[:200]})

    def unscan(self, file, surface, reason):
        self.unscanned.append({"file": file, "surface": surface, "reason": reason})

    def visual(self, file, surface, note):
        self.visual_review.append({"file": file, "surface": surface, "note": note})

    @property
    def status(self):
        if self.matches:
            return "FAIL"
        if self.unscanned:
            return "UNSCANNED"
        return "OK"


def excerpt(text, m):
    a, b = max(0, m.start() - 40), min(len(text), m.end() + 40)
    return text[a:b].replace("\n", " ")


def scan_text(rep, label, surface, text):
    for m in PATTERN.finditer(text):
        rep.match(label, surface, excerpt(text, m))
        return True
    return False


def scan_bytes(rep, label, surface, data):
    m = PATTERN_BYTES.search(data)
    if m:
        a, b = max(0, m.start() - 40), min(len(data), m.end() + 40)
        rep.match(label, surface, data[a:b].decode("latin-1").replace("\n", " "))
        return True
    return False


def local_tag(tag):
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


# Elements whose descendant text forms one logical string (split runs are joined).
CONTAINER_TAGS = {"p", "si", "is", "text", "comment", "v", "f", "title", "description",
                  "subject", "creator", "keywords", "category", "contentStatus", "lastModifiedBy"}


def scan_xml_part(rep, label, surface, data):
    """Join text inside each logical container, scan attributes, scan every text node."""
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        rep.unscan(label, surface, f"XML parse error: {e}")
        return
    found = False
    for el in root.iter():
        for v in el.attrib.values():
            if PATTERN.search(v):
                rep.match(label, surface + " (attribute)", v)
                found = True
        tag = local_tag(el.tag)
        if tag in CONTAINER_TAGS:
            joined = "".join(el.itertext())
            if joined and scan_text(rep, label, surface, joined):
                found = True
    if not found:
        for el in root.iter():
            if el.text and PATTERN.search(el.text):
                rep.match(label, surface, excerpt(el.text, PATTERN.search(el.text)))
                break
            if el.tail and PATTERN.search(el.tail):
                rep.match(label, surface, excerpt(el.tail, PATTERN.search(el.tail)))
                break


def scan_zip_bytes(rep, label, data, depth):
    """Scan an OOXML or ZIP container: member names, XML parts, nested containers."""
    if depth > 6:
        rep.unscan(label, "archive", "nesting deeper than 6 levels")
        return
    try:
        zf = zipfile.ZipFile(io.BytesIO(data))
        names = zf.namelist()
    except (zipfile.BadZipFile, RuntimeError, OSError) as e:
        rep.unscan(label, "archive", f"cannot open: {e}")
        return
    for name in names:
        if PATTERN.search(name):
            rep.match(label, "archive member name", name)
        if name.endswith("/"):
            continue
        try:
            member = zf.read(name)
        except (RuntimeError, OSError, zipfile.BadZipFile) as e:
            rep.unscan(label, f"member {name}", f"cannot read: {e}")
            continue
        mlabel = f"{label}::{name}"
        ext = os.path.splitext(name)[1].lower()
        if ext in (".xml", ".rels") or name.endswith(".xml.rels"):
            scan_xml_part(rep, label, f"xml {name}", member)
        elif ext in OOXML_EXT or ext in ZIP_EXT or member[:2] == b"PK":
            scan_zip_bytes(rep, mlabel, member, depth + 1)
        elif ext in PDF_EXT:
            scan_pdf_bytes(rep, mlabel, member)
        elif ext in IMAGE_EXT:
            rep.visual(label, f"embedded image {name}", "image content requires visual review")
            scan_bytes(rep, label, f"embedded image {name} (raw bytes)", member)
        else:
            text = try_decode(member)
            if text is not None:
                scan_text(rep, label, f"member {name}", text)
            else:
                scan_bytes(rep, label, f"member {name} (raw bytes)", member)


def try_decode(data):
    if b"\x00" in data[:4096]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return data.decode("latin-1")
        except UnicodeDecodeError:
            return None


def run(cmd, stdin_bytes=None):
    try:
        p = subprocess.run(cmd, input=stdin_bytes, capture_output=True, timeout=120)
        return p.returncode, p.stdout, p.stderr
    except (OSError, subprocess.TimeoutExpired) as e:
        return -1, b"", str(e).encode()


def scan_pdf_bytes(rep, label, data):
    scan_bytes(rep, label, "pdf raw bytes", data)
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tf:
        tf.write(data)
        path = tf.name
    try:
        scan_pdf_path(rep, label, path)
    finally:
        os.unlink(path)


def scan_pdf_path(rep, label, path):
    if not rep.tools["pdftotext"]:
        rep.unscan(label, "pdf text layer", "pdftotext not installed")
    else:
        rc, out, err = run(["pdftotext", "-q", path, "-"])
        if rc != 0:
            rep.unscan(label, "pdf text layer", f"pdftotext exit {rc}: {err.decode(errors='replace')[:120]}")
        else:
            text = out.decode("utf-8", errors="replace")
            scan_text(rep, label, "pdf text layer", text)
            pages = pdf_page_count(rep, path)
            if pages and len(text.strip()) < MIN_TEXT_CHARS_PER_PAGE * pages:
                rep.visual(label, "pdf pages", f"little or no text layer ({len(text.strip())} chars / {pages} pages) — image-only content requires visual review")
    if not rep.tools["pdfinfo"]:
        rep.unscan(label, "pdf metadata", "pdfinfo not installed")
    else:
        rc, out, err = run(["pdfinfo", path])
        if rc != 0:
            rep.unscan(label, "pdf Info metadata", f"pdfinfo exit {rc}")
        else:
            scan_text(rep, label, "pdf Info metadata", out.decode("utf-8", errors="replace"))
        rc, out, err = run(["pdfinfo", "-meta", path])
        if rc != 0:
            rep.unscan(label, "pdf XMP metadata", f"pdfinfo -meta exit {rc}")
        else:
            scan_text(rep, label, "pdf XMP metadata", out.decode("utf-8", errors="replace"))
    if rep.tools["pdfdetach"]:
        rc, out, err = run(["pdfdetach", "-list", path])
        if rc == 0:
            listing = out.decode("utf-8", errors="replace")
            lines = [l for l in listing.splitlines() if l.strip() and not l.lower().startswith("0 embedded")]
            if any(l[:1].isdigit() and ":" in l for l in lines):
                with tempfile.TemporaryDirectory() as td:
                    rc2, _, err2 = run(["pdfdetach", "-saveall", "-o", td, path])
                    if rc2 != 0:
                        rep.unscan(label, "pdf embedded files", f"pdfdetach exit {rc2}")
                    else:
                        for dp, _, fns in os.walk(td):
                            for fn in fns:
                                p = os.path.join(dp, fn)
                                with open(p, "rb") as f:
                                    scan_file_bytes(rep, f"{label}::attachment {fn}", fn, f.read(), depth=1)
        else:
            rep.unscan(label, "pdf embedded files", f"pdfdetach exit {rc}")
    else:
        rep.unscan(label, "pdf embedded files", "pdfdetach not installed")


def pdf_page_count(rep, path):
    if not rep.tools["pdfinfo"]:
        return None
    rc, out, _ = run(["pdfinfo", path])
    if rc != 0:
        return None
    for line in out.decode("utf-8", errors="replace").splitlines():
        if line.startswith("Pages:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                return None
    return None


def scan_file_bytes(rep, label, name, data, depth):
    ext = os.path.splitext(name)[1].lower()
    if ext in PDF_EXT:
        scan_pdf_bytes(rep, label, data)
    elif ext in OOXML_EXT or ext in ZIP_EXT:
        scan_zip_bytes(rep, label, data, depth)
    elif ext in IMAGE_EXT:
        rep.visual(label, "image", "image content requires visual review")
        scan_bytes(rep, label, "image raw bytes", data)
    else:
        text = try_decode(data)
        if text is not None:
            scan_text(rep, label, "text", text)
        else:
            if data[:2] == b"PK":
                scan_zip_bytes(rep, label, data, depth)
            elif data[:4] == b"%PDF":
                scan_pdf_bytes(rep, label, data)
            else:
                scan_bytes(rep, label, "raw bytes", data)
                rep.visual(label, "binary", "unknown binary format — raw-byte scan only")


def scan_path(rep, root, path):
    rel = os.path.relpath(path, root)
    rep.files += 1
    if PATTERN.search(rel):
        rep.match(rel, "path", rel)
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError as e:
        rep.unscan(rel, "file", f"cannot read: {e}")
        return
    ext = os.path.splitext(path)[1].lower()
    if ext in PDF_EXT:
        scan_bytes(rep, rel, "pdf raw bytes", data)
        scan_pdf_path(rep, rel, path)
    else:
        scan_file_bytes(rep, rel, path, data, depth=0)


def walk(root, rep):
    """Every file under root except the recognized control files at exactly <root>/tools/."""
    skip = control_paths(root)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        for fn in sorted(filenames):
            if fn == ".DS_Store":
                continue
            p = os.path.join(dirpath, fn)
            if p in skip:
                rep.controls_skipped.append(os.path.relpath(p, root))
                continue
            yield p


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    default_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--root", default=default_root, help="directory to scan")
    ap.add_argument("--json", help="write a machine-readable report here")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print(f"LINT ERROR — root is not a directory: {root}")
        return 2
    rep = Report(root)
    for p in walk(root, rep):
        scan_path(rep, root, p)

    out = {"root": root, "files_scanned": rep.files, "controls_skipped": rep.controls_skipped,
           "status": rep.status, "tools": rep.tools, "matches": rep.matches,
           "unscanned": rep.unscanned, "visual_review": rep.visual_review}
    if args.json:
        with open(args.json, "w") as f:
            json.dump(out, f, indent=2)
            f.write("\n")

    if not args.quiet:
        print(f"root: {root}")
        print(f"files scanned: {rep.files}; recognized control files skipped: {len(rep.controls_skipped)}")
        for m in rep.matches:
            print(f"  MATCH    {m['file']} [{m['surface']}]: {m['evidence']}")
        for u in rep.unscanned:
            print(f"  UNSCANNED {u['file']} [{u['surface']}]: {u['reason']}")
        for v in rep.visual_review:
            print(f"  VISUAL   {v['file']} [{v['surface']}]: {v['note']}")
    missing = [t for t, p in rep.tools.items() if not p]
    if rep.status == "OK":
        print(f"LINT OK — no forbidden labels in {rep.files} files; {len(rep.visual_review)} surface(s) need visual review")
        return 0
    if rep.status == "FAIL":
        print(f"LINT FAIL — {len(rep.matches)} forbidden-label match(es) in {rep.files} files")
        return 1
    print(f"LINT UNSCANNED — {len(rep.unscanned)} surface(s) could not be scanned"
          + (f" (missing tools: {', '.join(missing)})" if missing else ""))
    return 2


if __name__ == "__main__":
    sys.exit(main())
