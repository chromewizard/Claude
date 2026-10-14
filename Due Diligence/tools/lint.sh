#!/usr/bin/env bash
# Forbidden-label scan for the Due Diligence package.
# Exit 1 if any file path, text file, PDF text layer, PDF metadata, or Office/ZIP XML
# contains the forbidden label. Case-insensitive. The pattern lives only here.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PATTERN='pharaoh'
fail=0

report() { # $1 = label, $2 = matched lines (may be empty)
  if [ -n "$2" ]; then
    printf '%s\n' "$2" | sed "s|^|  $1: |"
    fail=1
  fi
}

while IFS= read -r -d '' f; do
  rel="${f#"$ROOT"/}"
  case "$rel" in tools/*) continue ;; esac

  if printf '%s' "$rel" | grep -iqE "$PATTERN"; then
    echo "  PATH: $rel"; fail=1
  fi

  lower="$(printf '%s' "$f" | tr '[:upper:]' '[:lower:]')"
  case "$lower" in
    *.pdf)
      if command -v pdftotext >/dev/null; then
        report "$rel (text layer)" "$(pdftotext -q "$f" - 2>/dev/null | grep -inE "$PATTERN" | head -5)"
      fi
      if command -v pdfinfo >/dev/null; then
        report "$rel (PDF metadata)" "$(pdfinfo "$f" 2>/dev/null | grep -iE "$PATTERN" | head -5)"
      fi ;;
    *.docx|*.xlsx|*.pptx|*.zip)
      report "$rel (Office/ZIP XML)" "$(unzip -p "$f" 2>/dev/null | tr -d '\000' | grep -ioE ".{0,40}$PATTERN.{0,40}" | head -5)" ;;
    *)
      if file -b --mime "$f" | grep -q text; then
        report "$rel" "$(grep -inE "$PATTERN" "$f" | head -5)"
      fi ;;
  esac
done < <(find "$ROOT" -type f -print0)

count="$(find "$ROOT" -type f ! -path "$ROOT/tools/*" | wc -l | tr -d ' ')"
if [ "$fail" -eq 0 ]; then
  echo "LINT OK — no forbidden labels in $count files"
  exit 0
fi
echo "LINT FAIL — forbidden label found (see above)"
exit 1
