"""Marker converters for the founder's [TBD]-in-orange instruction (15 Oct 2026).
HTML: every exact [TBD] token and every bare TBD word that is not part of the founder's quotation or a historical
phrase becomes <span class="need"><b>[TBD]</b></span> in ONE pass (so the inserted span is never re-matched);
existing .need spans are left as they are. Markdown: the same, spelled [TBD]."""
import re

QUOTE = "make the TBD in brackets [TBD] and in orange ink"
HIST = ["cover fields TBD", "six TBD fields", "banner and TBD fields", "TBDs removed", "six TBDs", '"TBD"']
SPAN = '<span class="need"><b>[TBD]</b></span>'

def _protect(s):
    keep = {}
    for ph in [QUOTE] + HIST:
        if ph in s:
            k = f"\x00{len(keep)}\x00"
            keep[k] = ph
            s = s.replace(ph, k)
    return s, keep

def _restore(s, keep):
    for k, v in keep.items():
        s = s.replace(k, v)
    return s

def wrap_html(s):
    spans = {}
    def hold(m):
        k = f"\x01{len(spans)}\x01"
        spans[k] = m.group(0)
        return k
    s = re.sub(r'<span class="need">.*?</span>', hold, s, flags=re.S)
    s, keep = _protect(s)
    s = re.sub(r"\[TBD\]|\bTBD\b", SPAN, s)
    s = _restore(s, keep)
    for k, v in spans.items():
        s = s.replace(k, v)
    return s

def conv_md(s):
    s, keep = _protect(s)
    s = re.sub(r"(?<!\[)\bTBD\b(?!\])", "[TBD]", s)
    return _restore(s, keep)

def repair_html(s):
    """Undo the double-bracket artifact of the earlier two-pass converter."""
    return s.replace("[" + SPAN + "]", SPAN)
