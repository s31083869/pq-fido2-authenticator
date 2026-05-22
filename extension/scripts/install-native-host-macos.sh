#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  cat >&2 <<'USAGE'
Usage:
  bash scripts/install-native-host-macos.sh <CHROME_EXTENSION_ID> [HOST_BINARY_PATH]

Example:
  bash scripts/install-native-host-macos.sh abcdefghijklmnopqrstuvwxyzabcdef
USAGE
  exit 1
fi

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "[install:native-host] macOS only" >&2
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
EXTENSION_ID="$1"
HOST_BINARY_PATH="${2:-$ROOT_DIR/.native-host/bin/pq_uv_host}"
HOST_NAME="com.scalebear.pqwebauthn_uv"
MANIFEST_DIR="$HOME/Library/Application Support/Google/Chrome/NativeMessagingHosts"
MANIFEST_PATH="$MANIFEST_DIR/$HOST_NAME.json"

if [[ ! -x "$HOST_BINARY_PATH" ]]; then
  cat >&2 <<MSG
[install:native-host] host binary not found or not executable:
  $HOST_BINARY_PATH

Build it first:
  bash scripts/build-native-host-macos.sh
MSG
  exit 1
fi

mkdir -p "$MANIFEST_DIR"

cat > "$MANIFEST_PATH" <<EOF
{
  "name": "$HOST_NAME",
  "description": "PQ WebAuthn native UV host (Touch ID)",
  "path": "$HOST_BINARY_PATH",
  "type": "stdio",
  "allowed_origins": [
    "chrome-extension://$EXTENSION_ID/"
  ]
}
EOF

echo "[install:native-host] installed manifest:"
echo "  $MANIFEST_PATH"
echo "[install:native-host] extension id:"
echo "  $EXTENSION_ID"
