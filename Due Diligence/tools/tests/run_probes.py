#!/usr/bin/env python3
"""Regression probes for tools/lint.py.

Every fixture is generated at run time inside a temporary directory and deleted
afterwards; no file containing the forbidden label is ever committed. Each probe
runs the real scanner as a subprocess with --root pointing at an isolated
directory and checks the machine-readable report.

Run:  python3 tools/tests/run_probes.py
Exit 0 when every probe passes.
"""
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
LINT = os.path.join(os.path.dirname(HERE), "lint.py")
LABEL = "Phar" + "aoh"          # assembled so this source file never spells the label
SPLIT_A, SPLIT_B = "Phar", "aoh"


# ---------- fixture builders ----------

def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = "wb" if isinstance(data, bytes) else "w"
    with open(path, mode) as f:
        f.write(data)


def zip_bytes(parts):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in parts.items():
            z.writestr(name, data)
    return buf.getvalue()


CT = '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>'
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
S = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def docx(paragraph_runs, core_creator="Ian McLean"):
    runs = "".join(f"<w:r><w:t xml:space=\"preserve\">{t}</w:t></w:r>" for t in paragraph_runs)
    doc = f'<?xml version="1.0"?><w:document xmlns:w="{W}"><w:body><w:p>{runs}</w:p></w:body></w:document>'
    core = ('<?xml version="1.0"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:creator>' + core_creator + '</dc:creator></cp:coreProperties>')
    return zip_bytes({"[Content_Types].xml": CT, "word/document.xml": doc, "docProps/core.xml": core})


def xlsx(shared_string_runs):
    si = "".join(f"<r><t xml:space=\"preserve\">{t}</t></r>" for t in shared_string_runs)
    sst = f'<?xml version="1.0"?><sst xmlns="{S}" count="1" uniqueCount="1"><si>{si}</si></sst>'
    sheet = f'<?xml version="1.0"?><worksheet xmlns="{S}"><sheetData><row r="4"><c r="A4" t="s"><v>0</v></c></row></sheetData></worksheet>'
    return zip_bytes({"[Content_Types].xml": CT, "xl/sharedStrings.xml": sst, "xl/worksheets/sheet1.xml": sheet})


def pptx(text, shape_name="Title 1", embedded=None):
    slide = (f'<?xml version="1.0"?><p:sld xmlns:p="{P}" xmlns:a="{A}"><p:cSld><p:spTree><p:sp><p:nvSpPr>'
             f'<p:cNvPr id="2" name="{shape_name}"/></p:nvSpPr><p:txBody><a:p><a:r><a:t>{text}</a:t></a:r></a:p>'
             f'</p:txBody></p:sp></p:spTree></p:cSld></p:sld>')
    parts = {"[Content_Types].xml": CT, "ppt/slides/slide1.xml": slide}
    if embedded is not None:
        parts["ppt/embeddings/Microsoft_Excel_Worksheet1.xlsx"] = embedded
    return zip_bytes(parts)


def pdf(body_text="Hello", info_title=None, xmp=None, image_only=False):
    objs = []
    content = b"" if image_only else f"BT /F1 12 Tf 20 100 Td ({body_text}) Tj ET".encode()
    if image_only:
        content = b"0 0 1 rg 10 10 100 100 re f"
    catalog = b"<< /Type /Catalog /Pages 2 0 R" + (b" /Metadata 7 0 R" if xmp else b"") + b" >>"
    objs.append(catalog)
    objs.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objs.append(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>")
    objs.append(b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream")
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objs.append(b"<< /Producer (probe)" + (f" /Title ({info_title})".encode() if info_title else b"") + b" >>")
    if xmp:
        x = ('<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?><x:xmpmeta xmlns:x="adobe:ns:meta/">'
             '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><rdf:Description rdf:about="" '
             'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:description><rdf:Alt><rdf:li xml:lang="x-default">'
             + xmp + '</rdf:li></rdf:Alt></dc:description></rdf:Description></rdf:RDF></x:xmpmeta><?xpacket end="w"?>').encode()
        objs.append(b"<< /Type /Metadata /Subtype /XML /Length " + str(len(x)).encode() + b" >>\nstream\n" + x + b"\nendstream")
    out = io.BytesIO()
    out.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for i, o in enumerate(objs, 1):
        offsets.append(out.tell())
        out.write(f"{i} 0 obj\n".encode() + o + b"\nendobj\n")
    xref = out.tell()
    out.write(f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n".encode())
    for off in offsets:
        out.write(f"{off:010d} 00000 n \n".encode())
    out.write(f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R /Info 6 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    return out.getvalue()


# ---------- runner ----------

def run_lint(root, env=None):
    rep = os.path.join(root, "..", "report.json")
    p = subprocess.run([sys.executable, LINT, "--root", root, "--json", rep, "--quiet"],
                       capture_output=True, text=True, env=env)
    with open(rep) as f:
        data = json.load(f)
    return p.returncode, data


def expect(name, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  — {detail}" if detail and not cond else ""))
    return cond


def probe(name, files, check, env=None):
    td = tempfile.mkdtemp(prefix="ddprobe_")
    root = os.path.join(td, "root")
    os.makedirs(root)
    try:
        for rel, data in files.items():
            write(os.path.join(root, rel), data)
        rc, rep = run_lint(root, env=env)
        ok = check(rc, rep)
        return expect(name, ok, f"rc={rc} status={rep['status']} matches={[(m['surface']) for m in rep['matches']]} unscanned={[u['surface'] for u in rep['unscanned']]}")
    finally:
        shutil.rmtree(td, ignore_errors=True)


def surfaces(rep):
    return {m["surface"] for m in rep["matches"]}


def main():
    print(f"scanner: {LINT}")
    results = []
    L = LABEL

    results.append(probe("P01 plain text file", {"notes.md": f"Roster\n{L} of AI\n"},
                         lambda rc, r: rc == 1 and "text" in surfaces(r)))
    results.append(probe("P02 docx label split across runs", {"a.docx": docx([f"Ian F. McLean (\"{SPLIT_A}", f"{SPLIT_B}\")"])},
                         lambda rc, r: rc == 1 and any(s.startswith("xml word/document.xml") for s in surfaces(r))))
    results.append(probe("P03 xlsx shared string split across rich-text runs", {"m.xlsx": xlsx([f"Ian F. McLean (\"{SPLIT_A}", f"{SPLIT_B}\")"])},
                         lambda rc, r: rc == 1 and any("sharedStrings" in s for s in surfaces(r))))
    results.append(probe("P04 xlsx exact Roster!A4 shape", {"EnergyWave_Raise_Model_v1.xlsx": xlsx([f"Ian F. McLean (\"{L}\")"])},
                         lambda rc, r: rc == 1 and any("sharedStrings" in s for s in surfaces(r))))
    results.append(probe("P05 pptx slide text", {"d.pptx": pptx(f"Founder {L}")},
                         lambda rc, r: rc == 1 and any("slide1" in s for s in surfaces(r))))
    results.append(probe("P06 pptx shape-name attribute", {"d.pptx": pptx("clean", shape_name=f"{L} box")},
                         lambda rc, r: rc == 1 and any("attribute" in s for s in surfaces(r))))
    results.append(probe("P07 docx core.xml creator metadata", {"a.docx": docx(["clean"], core_creator=f"{L} of AI")},
                         lambda rc, r: rc == 1 and any("core.xml" in s for s in surfaces(r))))
    results.append(probe("P08 pdf Info /Title metadata", {"t.pdf": pdf("clean body", info_title=f"{L} deck")},
                         lambda rc, r: rc == 1 and bool(surfaces(r) & {"pdf Info metadata", "pdf raw bytes"})))
    results.append(probe("P09 pdf XMP dc:description", {"x.pdf": pdf("clean body", xmp=f"{L} xmp")},
                         lambda rc, r: rc == 1 and bool(surfaces(r) & {"pdf XMP metadata", "pdf raw bytes"})))
    results.append(probe("P10 pdf text layer", {"b.pdf": pdf(f"Prepared for {L}")},
                         lambda rc, r: rc == 1 and bool(surfaces(r) & {"pdf text layer", "pdf raw bytes"})))
    results.append(probe("P11 zip member name", {"s.zip": zip_bytes({f"{L}.txt": "clean"})},
                         lambda rc, r: rc == 1 and "archive member name" in surfaces(r)))
    results.append(probe("P12 zip containing docx (nested)", {"n.zip": zip_bytes({"inner/a.docx": docx([SPLIT_A, SPLIT_B])})},
                         lambda rc, r: rc == 1 and any("word/document.xml" in s for s in surfaces(r))))
    results.append(probe("P13 pptx with embedded xlsx", {"e.pptx": pptx("clean", embedded=xlsx([L]))},
                         lambda rc, r: rc == 1 and any("sharedStrings" in s for s in surfaces(r))))
    results.append(probe("P14 label in directory path", {f"{L}-notes/clean.md": "clean\n"},
                         lambda rc, r: rc == 1 and "path" in surfaces(r)))
    results.append(probe("P15 image-only pdf → visual review, no match", {"scan.pdf": pdf(image_only=True)},
                         lambda rc, r: rc == 0 and not r["matches"] and any(v["surface"] == "pdf pages" for v in r["visual_review"])))
    results.append(probe("P16 clean set passes", {"ok.md": "clean\n", "ok.docx": docx(["clean"]), "ok.xlsx": xlsx(["Ian McLean"]), "ok.pdf": pdf("clean")},
                         lambda rc, r: rc == 0 and r["status"] == "OK" and r["files_scanned"] == 4))
    results.append(probe("P17 --root is honored", {"sub/one.md": "clean\n", "two.md": "clean\n"},
                         lambda rc, r: rc == 0 and r["files_scanned"] == 2 and os.path.basename(r["root"]) == "root"))
    empty = tempfile.mkdtemp(prefix="emptypath_")
    try:
        results.append(probe("P18 missing pdftotext/pdfinfo → UNSCANNED, not OK", {"c.pdf": pdf("clean")},
                             lambda rc, r: rc == 2 and r["status"] == "UNSCANNED" and r["tools"]["pdftotext"] is None,
                             env={**os.environ, "PATH": empty}))
    finally:
        shutil.rmtree(empty, ignore_errors=True)
    results.append(probe("P19 corrupt xlsx → UNSCANNED", {"bad.xlsx": b"PK\x03\x04 this is not a zip"},
                         lambda rc, r: rc == 2 and r["unscanned"]))

    # ---- control-policy probes (F-GPT-R2C1 / R2C2 / R2C3) ----
    results.extend(control_policy_probes())

    passed = sum(1 for r in results if r)
    print(f"{passed}/{len(results)} probes passed")
    return 0 if passed == len(results) else 1


# ---------- control-policy probes ----------

TOOLS_DIR = os.path.dirname(HERE)
CONTROL_REL = ["lint.py", "lint.sh", "build_manifest.py", "verify_manifest.py", os.path.join("tests", "run_probes.py")]


def make_package(td):
    """A small canonical package with real control code and a built manifest."""
    pkg = os.path.join(td, "pkg")
    write(os.path.join(pkg, "README.md"), "clean\n")
    write(os.path.join(pkg, "01_Investor", "note.md"), "clean\n")
    write(os.path.join(pkg, "MANIFEST.md"), "# m\n<!-- BEGIN GENERATED -->\n<!-- END GENERATED -->\n")
    for rel in CONTROL_REL:
        src = os.path.join(TOOLS_DIR, rel)
        dst = os.path.join(pkg, "tools", rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
    p = subprocess.run([sys.executable, os.path.join(pkg, "tools", "build_manifest.py")], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("package build failed: " + p.stdout + p.stderr)
    return pkg


def mirror_of(pkg, td, name):
    m = os.path.join(td, name)
    shutil.copytree(pkg, m)
    return m


def verify(trusted_manifest, root, extra_args=()):
    p = subprocess.run([sys.executable, os.path.join(TOOLS_DIR, "verify_manifest.py"), "--manifest", trusted_manifest,
                        "--root", root, *extra_args], capture_output=True, text=True)
    return p.returncode, p.stdout


def external_lint(root):
    rep = os.path.join(root, "..", "ext-report.json")
    p = subprocess.run([sys.executable, LINT, "--root", root, "--json", rep, "--quiet"], capture_output=True, text=True)
    with open(rep) as f:
        return p.returncode, json.load(f)


def control_policy_probes():
    out = []
    td = tempfile.mkdtemp(prefix="ddctl_")
    try:
        pkg = make_package(td)
        manifest = os.path.join(pkg, "manifest.json")

        m = mirror_of(pkg, td, "m_clean")
        rc, o = verify(manifest, m)
        out.append(expect("V01 identical mirror verifies", rc == 0, o))

        m = mirror_of(pkg, td, "m_nested_tools")
        write(os.path.join(m, "01_Investor", "tools", "unlisted.txt"), "x\n")
        rc, o = verify(manifest, m)
        out.append(expect("V02 unlisted file under nested tools/ → EXTRA, FAIL (R2C1)", rc == 1 and "EXTRA    01_Investor/tools/unlisted.txt" in o, o))

        m = mirror_of(pkg, td, "m_root_tools_extra")
        write(os.path.join(m, "tools", "stray.pdf"), b"%PDF-1.4 not really")
        rc, o = verify(manifest, m)
        out.append(expect("V03 unlisted file inside root tools/ → EXTRA, FAIL", rc == 1 and "EXTRA    tools/stray.pdf" in o, o))

        m = mirror_of(pkg, td, "m_missing_control")
        os.remove(os.path.join(m, "tools", "lint.py"))
        rc, o = verify(manifest, m)
        out.append(expect("V04 one control file absent → FAIL (R2C2)", rc == 1 and "tools/lint.py: ABSENT" in o, o))

        m = mirror_of(pkg, td, "m_tampered_control")
        with open(os.path.join(m, "tools", "verify_manifest.py"), "a") as f:
            f.write("\n# tampered\n")
        rc, o = verify(manifest, m)
        out.append(expect("V05 control file altered → MISMATCH, FAIL", rc == 1 and "verify_manifest.py: MISMATCH" in o, o))

        m = mirror_of(pkg, td, "m_payload_only")
        shutil.rmtree(os.path.join(m, "tools"))
        rc_strict, o1 = verify(manifest, m)
        rc_po, o2 = verify(manifest, m, ("--payload-only",))
        out.append(expect("V06 payload-only mirror: strict FAIL, --payload-only OK", rc_strict == 1 and rc_po == 0, o1 + o2))

        m = mirror_of(pkg, td, "m_ds_store")
        write(os.path.join(m, ".DS_Store"), b"\x00\x00\x00\x01Bud1")
        write(os.path.join(m, "01_Investor", ".DS_Store"), b"\x00\x00\x00\x01Bud1")
        rc, o = verify(manifest, m)
        out.append(expect("V07 Finder metadata at any depth is ignored by the verifier (R3C1)", rc == 0 and ".DS_Store" not in o, o))
        p = subprocess.run([sys.executable, os.path.join(m, "tools", "build_manifest.py")], capture_output=True, text=True)
        with open(os.path.join(m, "manifest.json")) as f:
            built = f.read()
        rc2, o2 = verify(os.path.join(m, "manifest.json"), m)
        out.append(expect("B02 build/verify round-trip with nested Finder metadata (R3C1)",
                          p.returncode == 0 and ".DS_Store" not in built and rc2 == 0, p.stdout + o2))

        m = mirror_of(pkg, td, "m_external_lint")
        rc, r = external_lint(m)
        out.append(expect("L20 trusted external scanner passes an identical mirror (R2C3)",
                          rc == 0 and len(r["controls_skipped"]) == len(CONTROL_REL), f"rc={rc} skipped={r['controls_skipped']} matches={r['matches']}"))

        m = mirror_of(pkg, td, "m_nested_tools_label")
        write(os.path.join(m, "02_DoW", "tools", "hidden.md"), f"{LABEL}\n")
        rc, r = external_lint(m)
        out.append(expect("L21 label in a nested tools/ directory is still scanned → FAIL", rc == 1 and any("02_DoW/tools/hidden.md" in x["file"] for x in r["matches"]), f"rc={rc}"))

        m = mirror_of(pkg, td, "m_root_tools_label")
        write(os.path.join(m, "tools", "notes.txt"), f"{LABEL}\n")
        rc, r = external_lint(m)
        out.append(expect("L22 unrecognized file inside root tools/ is scanned → FAIL", rc == 1 and any(x["file"] == "tools/notes.txt" for x in r["matches"]), f"rc={rc}"))

        m = mirror_of(pkg, td, "m_build_refuses")
        write(os.path.join(m, "tools", "stray.txt"), "x\n")
        p = subprocess.run([sys.executable, os.path.join(m, "tools", "build_manifest.py")], capture_output=True, text=True)
        out.append(expect("B01 builder refuses unrecognized files inside tools/", p.returncode == 1 and "BUILD REFUSED" in p.stdout, p.stdout))
    finally:
        shutil.rmtree(td, ignore_errors=True)
    return out


if __name__ == "__main__":
    sys.exit(main())
