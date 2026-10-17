#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
pc_hostname=$(hostname -s)
case "$pc_hostname" in
  optiplex-3060-2) session_id=01a125a2-e082-7913-92e6-699493f09cca ;;
  optiplex-3060-3) session_id=01a125a2-e082-7913-92e6-699493f09cca ;;
  latitude5540)    session_id=01a13997-558e-75f3-860e-c5b148e07d80 ;;
  *)
    printf 'No Codex session configured for hostname %s. Add a mapping in run-codex.sh.\n' "$pc_hostname" >&2
    exit 1
    ;;
esac
exec codex resume "$session_id" "$@"
