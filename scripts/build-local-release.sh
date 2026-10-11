#!/usr/bin/env bash
# Non-debuggable release APK for private testing of draft lessons.
# Uses the existing development signing key, never a publication key.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
bash scripts/build.sh -PlocalReleasePreview=true assembleRelease
