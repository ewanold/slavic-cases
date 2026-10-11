#!/usr/bin/env bash
# Install the already-built debug APK and open it; no downloads or Google account.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
export ANDROID_HOME="${ANDROID_HOME:-$HOME/Android/Sdk}"
adb_args=()
if [[ $# -gt 0 ]]; then adb_args=(-s "$1"); fi
apk=app/build/distributions/learn-grammatical-cases-debug.apk
[[ -f "$apk" ]] || { printf 'Build first: bash scripts/build.sh\n' >&2; exit 1; }
"$ANDROID_HOME/platform-tools/adb" "${adb_args[@]}" install -r "$apk"
"$ANDROID_HOME/platform-tools/adb" "${adb_args[@]}" shell am start -n org.slaviccases.app/.MainActivity
