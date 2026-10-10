#!/usr/bin/env bash
# All Gradle/dependency downloads for development go through this script.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
export JAVA_HOME="${JAVA_HOME:-$HOME/.local/opt/slavic-cases/android-studio-rabbit1/jbr}"
export ANDROID_HOME="${ANDROID_HOME:-$HOME/Android/Sdk}"
export PATH="$JAVA_HOME/bin:$PATH"
gradle_version=9.3.1
gradle_sha=b266d5ff6b90eada6dc3b20cb090e3731302e553a27c5d3e4df1f0d76beaff06
gradle_dir="$HOME/.local/share/slavic-cases/gradle-$gradle_version"
if [[ ! -x "$gradle_dir/bin/gradle" ]]; then
  [[ ! -e "$gradle_dir" ]] || { echo "Incomplete installation: $gradle_dir" >&2; exit 1; }
  build_tmp=$(mktemp -d)
  trap 'rm -rf -- "$build_tmp"' EXIT
  curl --fail --location --retry 3 --proto '=https' --tlsv1.2 \
    "https://services.gradle.org/distributions/gradle-$gradle_version-bin.zip" -o "$build_tmp/gradle.zip"
  printf '%s  %s\n' "$gradle_sha" "$build_tmp/gradle.zip" | sha256sum --check --status
  unzip -q "$build_tmp/gradle.zip" -d "$build_tmp"
  mkdir -p -- "$(dirname -- "$gradle_dir")"
  mv -- "$build_tmp/gradle-$gradle_version" "$gradle_dir"
fi
if [[ ! -f gradle/wrapper/gradle-wrapper.jar ]]; then
  "$gradle_dir/bin/gradle" --no-daemon wrapper --gradle-version "$gradle_version" \
    --distribution-type bin --gradle-distribution-sha256-sum "$gradle_sha"
fi
# Official wrapper JAR hash, independently checked after generation.
printf '%s  %s\n' 'b3a875ddc1f044746e1b1a55f645584505f4a10438c1afea9f15e92a7c42ec13' \
  'gradle/wrapper/gradle-wrapper.jar' | sha256sum --check --status
# Prime the wrapper's distribution cache here, so offline builds cannot trigger
# its separate bootstrap download. The wrapper verifies the same published SHA.
bash ./gradlew --version >/dev/null
if [[ $# -eq 0 ]]; then set -- assembleDebug testDebugUnitTest lintDebug; fi
# Pinned direct dependencies; Gradle verifies artifact hashes against the checked-in
# verification metadata once generated during first bootstrap.
"$gradle_dir/bin/gradle" --no-daemon "$@"
