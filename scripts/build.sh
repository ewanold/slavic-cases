#!/usr/bin/env bash
# Offline by default: dependency downloading is isolated in install-build-tools.sh.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
export JAVA_HOME="${JAVA_HOME:-$HOME/.local/opt/slavic-cases/android-studio-rabbit1/jbr}"
export ANDROID_HOME="${ANDROID_HOME:-$HOME/Android/Sdk}"
export PATH="$JAVA_HOME/bin:$PATH"
[[ -f gradle/wrapper/gradle-wrapper.jar ]] || { echo 'Run bash scripts/install-build-tools.sh first.' >&2; exit 1; }
if [[ $# -eq 0 ]]; then set -- assembleDebug testDebugUnitTest lintDebug; fi
gradle_dir="$HOME/.local/share/slavic-cases/gradle-9.3.1"
[[ -x "$gradle_dir/bin/gradle" ]] || { echo 'Run bash scripts/install-build-tools.sh first.' >&2; exit 1; }
# Use the already verified installation: even --offline cannot stop a Gradle
# wrapper from downloading its distribution if that wrapper cache is missing.
"$gradle_dir/bin/gradle" --offline --no-daemon "$@"
