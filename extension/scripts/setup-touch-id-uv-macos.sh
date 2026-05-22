#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "[setup:touch-id] macOS only" >&2
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_SCRIPT="$ROOT_DIR/scripts/build-native-host-macos.sh"
INSTALL_SCRIPT="$ROOT_DIR/scripts/install-native-host-macos.sh"

EXTENSION_ID="${1:-${CHROME_EXTENSION_ID:-}}"

if [[ -z "$EXTENSION_ID" ]]; then
  cat <<'MSG'
[setup:touch-id] Missing CHROME_EXTENSION_ID.

Find it in:
  chrome://extensions

Then run either:
  1) bun run setup:touch-id:macos -- <CHROME_EXTENSION_ID>
  2) CHROME_EXTENSION_ID=<id> bun run setup:touch-id:macos
MSG
  exit 1
fi

if [[ ! "$EXTENSION_ID" =~ ^[a-p]{32}$ ]]; then
  echo "[setup:touch-id] invalid extension id format: $EXTENSION_ID" >&2
  exit 1
fi

echo "[setup:touch-id] step 1/2: build native host"
bash "$BUILD_SCRIPT"

echo "[setup:touch-id] step 2/2: install native host manifest"
bash "$INSTALL_SCRIPT" "$EXTENSION_ID"

cat <<MSG
[setup:touch-id] done.

Manual final steps:
  1) reload extension in chrome://extensions
  2) open extension options page
  3) set UV mode = native-touch-id
MSG
