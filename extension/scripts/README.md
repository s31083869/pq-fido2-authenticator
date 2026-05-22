# `scripts/`

Automation scripts used by `package.json` commands.

## `run-bash.ts`

Purpose:

1. run shell scripts through Bun
2. on Windows, prefer Git for Windows Bash over WSL Bash
3. allow overriding the bash executable with `GIT_BASH`

## `setup-liboqs-emscripten.sh`

Purpose:

1. prepare local `liboqs` source in `.deps/liboqs-emscripten-src`
2. configure an Emscripten build directory
3. build static library `.deps/liboqs-emscripten-build/lib/liboqs.a`

Important behavior:

1. auto-detects CMake generator (`Ninja`, `MinGW Makefiles`, then `Unix Makefiles`)
2. resets build dir on each run to avoid stale toolchain cache issues
3. sets local `EM_CACHE` under `.deps/emscripten-cache`
4. compiles minimal algorithms only:
   1. `SIG_ml_dsa_44`
   2. `SIG_ml_dsa_65`
   3. `SIG_ml_dsa_87`

Main env vars:

1. `LIBOQS_REPO`
2. `LIBOQS_REF`
3. `LIBOQS_SRC_DIR`
4. `LIBOQS_BUILD_DIR`
5. `LIBOQS_MINIMAL_BUILD`
6. `EM_CACHE`
7. `EMSDK` (optional path to an Emscripten SDK checkout)

Windows note:

1. If `emcmake`/`emcc` are not already available inside Git Bash, scripts try to load Emscripten from `EMSDK`, `~/emsdk`, `C:\emsdk`, then `D:\emsdk`.
2. On Windows, setup also checks common MinGW/MSYS2 paths and uses `MinGW Makefiles` when `mingw32-make` is available.

## `build-liboqs-wasm.sh`

Purpose:

1. compile/link `wasm/pq_bridge.c` + `liboqs.a`
2. output `public/wasm/pq_bridge.wasm`

Input resolution order:

1. explicit env (`LIBOQS_INCLUDE_DIR`, `LIBOQS_STATIC_LIB`)
2. `LIBOQS_DIR` (include/lib or build/include/build/lib)
3. project-local `.deps/liboqs-emscripten-build`

Main env vars:

1. `LIBOQS_DIR`
2. `LIBOQS_INCLUDE_DIR`
3. `LIBOQS_STATIC_LIB`
4. `EM_CACHE`

## Common Failures

1. `Could not resolve host: github.com`
   1. Network/DNS issue when fetching liboqs.
2. `Missing LIBOQS include path`
   1. Run `bun run setup:liboqs:wasm` first.
3. `CMAKE generator mismatch`
   1. Script auto-resets build dir; rerun setup.
4. wasm CSP/runtime errors in extension
   1. Ensure extension reloaded from latest `dist/`.

## `build-native-host-macos.sh`

Purpose:

1. compile `native-host/pq_uv_host.swift`
2. output native host binary at `.native-host/bin/pq_uv_host`

Requirements:

1. macOS
2. Xcode Command Line Tools (`xcrun`, `swiftc`)

## `install-native-host-macos.sh`

Purpose:

1. install Chrome Native Messaging host manifest for Touch ID UV
2. register host name `com.scalebear.pqwebauthn_uv`

Usage:

1. `bash scripts/install-native-host-macos.sh <CHROME_EXTENSION_ID>`
2. optional second arg: host binary absolute path

Behavior:

1. writes manifest to:
   1. `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.scalebear.pqwebauthn_uv.json`
2. allowlist origin:
   1. `chrome-extension://<CHROME_EXTENSION_ID>/`

## `setup-touch-id-uv-macos.sh`

Purpose:

1. one-shot setup for Touch ID UV
2. run build + install in sequence

Usage:

1. `bash scripts/setup-touch-id-uv-macos.sh <CHROME_EXTENSION_ID>`
2. or set env:
   1. `CHROME_EXTENSION_ID=<id> bash scripts/setup-touch-id-uv-macos.sh`

Note:

1. this script cannot auto-reload extension or auto-change options page settings

## Windows Hello Native Host Scripts

Purpose:

1. `build-native-host-windows.ps1`: copy the PowerShell/CMD native host into `.native-host/bin/windows`
2. `install-native-host-windows.ps1`: write the Native Messaging manifest and register it under HKCU
3. `setup-windows-hello.ps1`: run build + install in sequence

Usage:

1. `bun run setup:windows-hello -- <CHROME_EXTENSION_ID>`
2. reload the extension
3. set `UV mode = native-windows-hello`

Requirements:

1. Windows with Windows Hello configured
2. Chrome extension id copied from `chrome://extensions`
