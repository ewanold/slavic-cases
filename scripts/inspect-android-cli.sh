#!/usr/bin/env bash
# The SDK's Android CLI launcher can download/unpack its runtime even for --help.
# Keep this operation scripted. sdkmanager remains our pinned setup path until
# the replacement runtime can be independently pinned and checksum-verified.
set -euo pipefail
export ANDROID_HOME="${ANDROID_HOME:-$HOME/Android/Sdk}"
exec "$ANDROID_HOME/cmdline-tools/15859902/bin/android" --no-metrics "$@"
