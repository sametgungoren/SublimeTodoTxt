#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="${ROOT}/dist"
PACKAGE_NAME="TodoTxt.sublime-package"

mkdir -p "${OUT_DIR}"

FILES=(
  plugin.py
  Default.sublime-commands
  TodoTxt.sublime-syntax
  TodoTxt.sublime-settings
  TodoTxt.sublime-color-scheme
  Miscellaneous.tmPreferences
  Symbol\ List.tmPreferences
)

rm -f "${OUT_DIR}/${PACKAGE_NAME}"

python3 - "${OUT_DIR}/${PACKAGE_NAME}" "${ROOT}" "${FILES[@]}" <<'PY'
import sys
import zipfile
from pathlib import Path

archive = Path(sys.argv[1])
root = Path(sys.argv[2])
names = sys.argv[3:]

with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for name in names:
        path = root / name
        zf.write(path, arcname=Path(name).name)

print(f"Built {archive}")
PY
