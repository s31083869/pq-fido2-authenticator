# `wasm/`

Native bridge source layer compiled by Emscripten.

## File

1. `pq_bridge.c`
   1. maps COSE alg ids (`-48/-49/-50`) to liboqs ML-DSA names
   2. exports C ABI functions for JS wasm bridge
   3. handles keypair/sign calls and size queries

## Output

1. generated artifact target: `public/wasm/pq_bridge.wasm`
2. consumer: `src/background/liboqs-wasm-bridge.ts`
