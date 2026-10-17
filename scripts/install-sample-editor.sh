#!/usr/bin/env bash
# All package downloads happen through the hash-verified Python installer below.
set -euo pipefail
project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ " $* " == *'--ui tk'* ]] && ! python3 -c 'import tkinter' 2>/dev/null; then
  sudo apt install python3-tk
fi
exec python3 "$project_dir/scripts/install-sample-editor.py" "$@"
