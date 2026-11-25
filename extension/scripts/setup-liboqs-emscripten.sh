#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DEPS_DIR="$ROOT_DIR/.deps"
EM_CACHE_DIR="${EM_CACHE:-$DEPS_DIR/emscripten-cache}"
LIBOQS_SRC_DIR="${LIBOQS_SRC_DIR:-$DEPS_DIR/liboqs-emscripten-src}"
LIBOQS_BUILD_DIR="${LIBOQS_BUILD_DIR:-$DEPS_DIR/liboqs-emscripten-build}"
LIBOQS_REPO="${LIBOQS_REPO:-https://github.com/open-quantum-safe/liboqs.git}"
# liboqs 固定在這個 commit（決策 D4，0.15.0-60-g33815beb），不再追 main：上游變動不會悄悄改變 WASM 的行為。
# 要升級時改這一行，並且必須重跑官方 KAT（CLAUDE.md「KAT」：bun test tests/kat）。
LIBOQS_REF="${LIBOQS_REF:-33815beb2ac404cba36ecf713f9fd5f1d868763a}"
# 只編專案用到的 5 個簽章演算法：ML-DSA-44/65/87 與 FN-DSA 的 Falcon-512/1024（不補滿格式，決策 D2）。
# 這份清單必須和 wasm/pq_bridge.c 的 pq_alg_name() 一致，少編一個時該演算法的 OQS_SIG_new() 會回傳 NULL。
LIBOQS_MINIMAL_BUILD="${LIBOQS_MINIMAL_BUILD:-SIG_ml_dsa_44;SIG_ml_dsa_65;SIG_ml_dsa_87;SIG_falcon_512;SIG_falcon_1024}"

# shellcheck disable=SC1091
source "$ROOT_DIR/scripts/emscripten-env.sh"

add_windows_build_tool_paths

if ! command -v git >/dev/null 2>&1; then
  echo "[setup:liboqs] git not found" >&2
  exit 1
fi

ensure_emscripten_tool emcmake "setup:liboqs"

if ! command -v cmake >/dev/null 2>&1; then
  echo "[setup:liboqs] cmake not found" >&2
  exit 1
fi

GENERATOR="${CMAKE_GENERATOR:-}"
if [[ -z "$GENERATOR" ]]; then
  if command -v ninja >/dev/null 2>&1; then
    GENERATOR="Ninja"
  elif command -v mingw32-make >/dev/null 2>&1; then
    GENERATOR="MinGW Makefiles"
  else
    if command -v make >/dev/null 2>&1; then
      GENERATOR="Unix Makefiles"
    else
      echo "[setup:liboqs] no CMake build tool found. Install Ninja, MSYS2 make, or MinGW make." >&2
      exit 1
    fi
  fi
fi

mkdir -p "$DEPS_DIR"
mkdir -p "$EM_CACHE_DIR"
export EM_CACHE="$EM_CACHE_DIR"

if [[ ! -d "$LIBOQS_SRC_DIR/.git" ]]; then
  echo "[setup:liboqs] cloning $LIBOQS_REPO -> $LIBOQS_SRC_DIR"
  git clone "$LIBOQS_REPO" "$LIBOQS_SRC_DIR"
fi

echo "[setup:liboqs] preparing source ref: $LIBOQS_REF"
cd "$LIBOQS_SRC_DIR"
git fetch --all --tags --quiet || true
git checkout "$LIBOQS_REF"

if [[ -d "$LIBOQS_BUILD_DIR" ]]; then
  echo "[setup:liboqs] resetting build dir: $LIBOQS_BUILD_DIR"
  rm -rf "$LIBOQS_BUILD_DIR"
fi
mkdir -p "$LIBOQS_BUILD_DIR"

echo "[setup:liboqs] configuring emscripten build"
emcmake cmake -S "$LIBOQS_SRC_DIR" -B "$LIBOQS_BUILD_DIR" \
  -G "$GENERATOR" \
  -DBUILD_SHARED_LIBS=OFF \
  -DOQS_BUILD_ONLY_LIB=ON \
  -DOQS_USE_OPENSSL=OFF \
  -DOQS_DIST_BUILD=OFF \
  -DOQS_MINIMAL_BUILD="$LIBOQS_MINIMAL_BUILD" \
  -DCMAKE_BUILD_TYPE=Release

echo "[setup:liboqs] building liboqs.a"
cmake --build "$LIBOQS_BUILD_DIR" -j

echo "[setup:liboqs] done"
echo "[setup:liboqs] minimal build: $LIBOQS_MINIMAL_BUILD"
echo "[setup:liboqs] include: $LIBOQS_BUILD_DIR/include"
echo "[setup:liboqs] static lib: $LIBOQS_BUILD_DIR/lib/liboqs.a"
