#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DEPS_DIR="$ROOT_DIR/.deps"
EM_CACHE_DIR="${EM_CACHE:-$DEPS_DIR/emscripten-cache}"
SRC="$ROOT_DIR/wasm/pq_bridge.c"
OUT_DIR="$ROOT_DIR/public/wasm"
OUT="$OUT_DIR/pq_bridge.wasm"

# shellcheck disable=SC1091
source "$ROOT_DIR/scripts/emscripten-env.sh"

ensure_emscripten_tool emcc "build:wasm"

mkdir -p "$EM_CACHE_DIR"
export EM_CACHE="$EM_CACHE_DIR"

LIBOQS_DIR="${LIBOQS_DIR:-}"
DEFAULT_LOCAL_SRC="$ROOT_DIR/.deps/liboqs-emscripten-src"
DEFAULT_LOCAL_BUILD="$ROOT_DIR/.deps/liboqs-emscripten-build"
LIBOQS_INCLUDE_DIR="${LIBOQS_INCLUDE_DIR:-}"
LIBOQS_STATIC_LIB="${LIBOQS_STATIC_LIB:-}"

if [[ -n "${LIBOQS_DIR:-}" ]]; then
  if [[ -z "${LIBOQS_INCLUDE_DIR:-}" && -d "$LIBOQS_DIR/include" ]]; then
    LIBOQS_INCLUDE_DIR="$LIBOQS_DIR/include"
  fi
  if [[ -z "${LIBOQS_INCLUDE_DIR:-}" && -d "$LIBOQS_DIR/build/include" ]]; then
    LIBOQS_INCLUDE_DIR="$LIBOQS_DIR/build/include"
  fi
  if [[ -z "${LIBOQS_STATIC_LIB:-}" && -f "$LIBOQS_DIR/lib/liboqs.a" ]]; then
    LIBOQS_STATIC_LIB="$LIBOQS_DIR/lib/liboqs.a"
  fi
  if [[ -z "${LIBOQS_STATIC_LIB:-}" && -f "$LIBOQS_DIR/build/lib/liboqs.a" ]]; then
    LIBOQS_STATIC_LIB="$LIBOQS_DIR/build/lib/liboqs.a"
  fi
fi

if [[ -z "${LIBOQS_INCLUDE_DIR:-}" && -d "$DEFAULT_LOCAL_BUILD/include" ]]; then
  LIBOQS_INCLUDE_DIR="$DEFAULT_LOCAL_BUILD/include"
fi

if [[ -z "${LIBOQS_INCLUDE_DIR:-}" && -d "$DEFAULT_LOCAL_SRC/src" ]]; then
  LIBOQS_INCLUDE_DIR="$DEFAULT_LOCAL_SRC/src"
fi

if [[ -z "${LIBOQS_STATIC_LIB:-}" && -f "$DEFAULT_LOCAL_BUILD/lib/liboqs.a" ]]; then
  LIBOQS_STATIC_LIB="$DEFAULT_LOCAL_BUILD/lib/liboqs.a"
fi

if [[ -z "${LIBOQS_INCLUDE_DIR:-}" || ! -d "$LIBOQS_INCLUDE_DIR" ]]; then
  cat >&2 <<MSG
[build:wasm] Missing LIBOQS include path.
Use one of:
  1) bun run setup:liboqs:wasm   (recommended, project-local)
  2) set LIBOQS_INCLUDE_DIR or LIBOQS_DIR manually
MSG
  exit 1
fi

if [[ -z "${LIBOQS_STATIC_LIB:-}" || ! -f "$LIBOQS_STATIC_LIB" ]]; then
  cat >&2 <<MSG
[build:wasm] Missing liboqs static library.
Use one of:
  1) bun run setup:liboqs:wasm   (recommended, project-local)
  2) set LIBOQS_STATIC_LIB or LIBOQS_DIR manually
MSG
  exit 1
fi

mkdir -p "$OUT_DIR"

EXPORTED='["_malloc","_free","_pq_public_key_bytes","_pq_secret_key_bytes","_pq_signature_bytes","_pq_generate_keypair","_pq_sign"]'

echo "[build:wasm] Building $OUT"
emcc "$SRC" \
  -I"$LIBOQS_INCLUDE_DIR" \
  "$LIBOQS_STATIC_LIB" \
  -O3 \
  -s STANDALONE_WASM=1 \
  -s ALLOW_MEMORY_GROWTH=1 \
  -s EXPORTED_FUNCTIONS="$EXPORTED" \
  -Wl,--no-entry \
  -o "$OUT"

echo "[build:wasm] Done"
