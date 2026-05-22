#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT_DIR/native-host/pq_uv_host.swift"
OUT_DIR="${NATIVE_HOST_BUILD_DIR:-$ROOT_DIR/.native-host/bin}"
OUT="$OUT_DIR/pq_uv_host"
MODULE_CACHE_DIR="${NATIVE_HOST_MODULE_CACHE_DIR:-$ROOT_DIR/.native-host/module-cache}"

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "[build:native-host] macOS only" >&2
  exit 1
fi

if ! command -v xcrun >/dev/null 2>&1; then
  echo "[build:native-host] xcrun not found (install Xcode command line tools)" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"
mkdir -p "$MODULE_CACHE_DIR"

SDK_PATH="$(xcrun --sdk macosx --show-sdk-path)"

echo "[build:native-host] compiling $SRC -> $OUT"
xcrun --sdk macosx swiftc \
  -O \
  -sdk "$SDK_PATH" \
  -module-cache-path "$MODULE_CACHE_DIR" \
  -framework Foundation \
  -framework LocalAuthentication \
  "$SRC" \
  -o "$OUT"

chmod +x "$OUT"
echo "[build:native-host] done: $OUT"
