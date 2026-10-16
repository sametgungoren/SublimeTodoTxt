#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="${ROOT}/dist"
PACKAGE_NAME="TodoTxt.sublime-package"
PLUGIN="${ROOT}/plugin.py"

mkdir -p "${OUT_DIR}"

VERSION="v$(date -u +%Y.%m.%d.%H.%M.%S)"
python3 - "${PLUGIN}" "${VERSION}" <<'PY'
import re
import sys
from pathlib import Path

plugin_path = Path(sys.argv[1])
version = sys.argv[2]
text = plugin_path.read_text(encoding='utf-8')
if 'VERSION = ' in text:
    text = re.sub(r'^VERSION = ".*"', f'VERSION = "{version}"', text, count=1, flags=re.M)
else:
    text = text.replace('import sublime_plugin\n', f'import sublime_plugin\n\nVERSION = "{version}"\n', 1)
plugin_path.write_text(text, encoding='utf-8')
print(f'Version set to {version}')
PY

FILES=(
  plugin.py
  todotxt_subtask_sync.py
  Default.sublime-commands
  TodoTxt.sublime-syntax
  Todo.txt.sublime-settings
  TodoTxt.sublime-settings
  TodoTxt.sublime-color-scheme
  Miscellaneous.tmPreferences
  Symbol\ List.tmPreferences
  messages.json
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
        if not path.is_file():
            raise SystemExit(f'Missing package file: {path}')
        zf.write(path, arcname=Path(name).name)

print(f'Built {archive}')
PY

echo "Package ${VERSION} -> ${OUT_DIR}/${PACKAGE_NAME}"
