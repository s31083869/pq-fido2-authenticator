# PQ WebAuthn Extension (WASM-only)

This package implements a Chrome MV3 WebAuthn hook that intercepts:

1. `navigator.credentials.create`
2. `navigator.credentials.get`

and routes both flows to a software authenticator backed by `liboqs` wasm.

## Scope

1. Target RP: `https://demo.yubico.com/*`
2. Algorithms: `ML-DSA-44/65/87` (`COSE -48/-49/-50`)
3. Attestation format: `none`
4. Runtime mode: wasm-only (no mock signer path)

## Prerequisites

1. Bun `>= 1.2`
2. Emscripten toolchain (`emcc`, `emcmake`)
3. CMake + Git
4. (Optional for Touch ID UV) macOS + Xcode Command Line Tools
5. (Optional for Windows Hello UV) Windows Hello configured on Windows

## Install

```bash
cd extension
bun install
```

## Setup and Build

Recommended first-time setup:

```bash
bun run setup
```

`setup` does:

1. clone/update local `liboqs` source into `.deps/`
2. compile minimal `liboqs.a` with Emscripten
3. build `public/wasm/pq_bridge.wasm`

Build extension bundle:

```bash
bun run build
```

Or run wasm + extension build together:

```bash
bun run build:all
```

## Touch ID UV Setup (optional)

Only required when settings `uvMode` is `native-touch-id`.

1. Build native host:

```bash
bun run build:native-host:macos
```

2. Find extension id from `chrome://extensions` (after loading unpacked `dist/`).
3. Install native host manifest:

```bash
bun run install:native-host:macos -- <CHROME_EXTENSION_ID>
```

Or one-shot:

```bash
bun run setup:touch-id:macos -- <CHROME_EXTENSION_ID>
```

4. Open extension options page and switch `UV mode` to `native-touch-id`.

## Windows Hello UV Setup (optional)

Only required on Windows when settings `uvMode` is `native-windows-hello`.

1. Build the extension and load `dist/` once from `chrome://extensions`.
2. Copy the extension id from `chrome://extensions`.
3. Build and install the Windows native host:

```powershell
bun run setup:windows-hello -- <CHROME_EXTENSION_ID>
```

4. Reload the extension from `chrome://extensions`.
5. Open the extension options page and switch `UV mode` to `native-windows-hello`.

## Test

```bash
bun run typecheck
bun run test
```

Tests use deterministic fake fixtures (seeded values) to reduce flaky behavior.

## Runtime Architecture

Flow summary:

1. `src/injected/` patches WebAuthn APIs in page main-world.
2. `src/content/` relays requests/responses across isolated world boundary.
3. `src/background/` validates request shape/origin and runs authenticator logic.
4. `src/background/liboqs-wasm-bridge.ts` loads `wasm/pq_bridge.wasm` and calls C exports.
5. credential/settings state is persisted in `chrome.storage.local`.

## Key Artifacts

1. `public/manifest.json`: MV3 manifest template
2. `wasm/pq_bridge.c`: C bridge layer for liboqs
3. `public/wasm/pq_bridge.wasm`: generated wasm runtime artifact
4. `dist/`: load-unpacked target directory

## Load in Chrome

1. Open `chrome://extensions`
2. Enable `Developer mode`
3. Click `Load unpacked`
4. Select `extension/dist`

## Security Notes (current milestone)

1. Hook is allowlisted to `demo.yubico.com`.
2. CSP includes `'wasm-unsafe-eval'` for wasm instantiation in extension pages.
3. UV supports:
   1. `soft-auto` (no-op trial gate)
   2. `native-touch-id` (macOS Native Messaging + Touch ID prompt)
   3. `native-windows-hello` (Windows Native Messaging + Windows Hello prompt)
4. Private keys are persisted in extension local storage and are not yet wrapped/encrypted.

## Distribution Note (Native Host)

1. Chrome extension alone cannot silently install Native Messaging host.
2. End users still need a host installer step (or your packaged app installer) to place:
   1. native host binary
   2. native host manifest under Chrome's NativeMessagingHosts directory
3. For production UX, ship both:
   1. extension package
   2. macOS installer (`.pkg`/signed app) that installs and registers native host
