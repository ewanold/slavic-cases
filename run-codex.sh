#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
exec codex resume 01a125a2-e082-7913-92e6-699493f09cca "$@"
