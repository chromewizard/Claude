#!/usr/bin/env bash
# Compatibility wrapper. The scanner is tools/lint.py (fail-closed, Python 3.8+).
# All arguments are passed through, e.g.:  bash tools/lint.sh --root "/path/to/mirror"
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lint.py" "$@"
