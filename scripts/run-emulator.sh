#!/usr/bin/env bash
# Starts the optional emulator installed by install-test-emulator.sh; no downloads.
set -euo pipefail
export ANDROID_HOME="${ANDROID_HOME:-$HOME/Android/Sdk}"
exec "$ANDROID_HOME/emulator/emulator" -avd slavic-cases-api36 \
  -no-snapshot -no-audio -no-boot-anim "$@"
