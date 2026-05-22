# `src/background/`

MV3 service worker runtime and authenticator core.

## File Map

1. `index.ts`
   1. background message entrypoint
   2. sender origin allowlist check
   3. error normalization
2. `authenticator.ts`
   1. create/get core logic
   2. COSE key construction
   3. authenticatorData/clientDataJSON assembly
   4. signCount update and persistence
3. `liboqs-wasm-bridge.ts`
   1. wasm loading
   2. WASI import shim
   3. raw memory bridge to exported C functions
4. `liboqs-wasm-signer.ts`
   1. signer adapter backed by wasm bridge
5. `pq-signer.ts`
   1. signer interface + algorithm byte-size constants
6. `native-uv.ts`
   1. Native Messaging bridge to macOS Touch ID host
   2. per-request UV prompt result handling
   3. native host health check (`uv-status`) for options UI
7. `store.ts`
   1. settings/credential persistence
   2. legacy migration
8. `*.test.ts`
   1. deterministic unit tests for storage and authenticator behavior
9. `test-utils.ts`
   1. deterministic fake data helpers
   2. `chrome.storage.local` test double

## Runtime Data Boundaries

1. trusted input boundary: messages from content script
2. cryptographic boundary: wasm bridge calls into `liboqs`
3. persistence boundary: `chrome.storage.local`

## Current Security Limitations

1. Touch ID UV depends on correctly installed native host manifest + extension id binding
2. private keys are stored unwrapped in extension storage
3. request schema validation is manual and selective (not full strict parser yet)
