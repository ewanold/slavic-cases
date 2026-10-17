#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
editor_python="${SAMPLE_EDITOR_PYTHON:-$HOME/.local/share/slavic-cases/sample-editor-venv/bin/python}"
if [[ ! -x "$editor_python" ]]; then
  editor_python="${CONTENT_VENV_DIR:-$HOME/.local/share/slavic-cases/content-venv}/bin/python"
fi
if [[ ! -x "$editor_python" ]]; then editor_python=python3; fi
exec "$editor_python" "$project_dir/tools/sample_editor/app.py" "$@"
