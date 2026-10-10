#!/usr/bin/env bash
set -euo pipefail
if [[ ${1:-} == --help ]]; then
  echo 'Usage: bash scripts/install-content-tools.sh'
  echo 'Linux x86-64/aarch64, Python 3.12 with venv support required.'
  echo 'Creates a user-local virtual environment and installs hash-verified PyYAML 6.0.1.'
  exit 0
fi
[[ $# -eq 0 ]] || { echo 'Unknown argument' >&2; exit 2; }
[[ $(uname -s) == Linux ]] || { echo 'This installer supports Linux only.' >&2; exit 1; }
case $(uname -m) in x86_64|aarch64) ;; *) echo 'Unsupported architecture' >&2; exit 1;; esac
project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
python3 -c 'import sys; assert sys.version_info[:2] == (3, 12), "Python 3.12 is required"'
content_venv_dir="${CONTENT_VENV_DIR:-$HOME/.local/share/slavic-cases/content-venv}"
python3 -m venv "$content_venv_dir"
"$content_venv_dir/bin/python" -m pip install --disable-pip-version-check --only-binary=:all: --require-hashes -r "$project_dir/requirements/content-tools-linux-py312.txt"
printf 'Ready: %s/bin/python %s/scripts/validate-samples.py\n' "$content_venv_dir" "$project_dir"
