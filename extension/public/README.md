# `public/`

Static files copied into `dist/` during Vite build.

## Files

1. `manifest.json`
   1. MV3 manifest template
   2. background worker/content script entries
   3. CSP and host permissions
2. `wasm/`
   1. generated runtime wasm artifact location

## Build Note

1. `public/wasm/pq_bridge.wasm` must exist before loading wasm signer path.
