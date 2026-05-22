# `src/lib/`

Shared utility modules used across injected/content/background layers.

## Modules

1. `base64url.ts`
   1. base64url <-> bytes
   2. base64 -> bytes fallback helper
2. `binary.ts`
   1. concatenation helpers
   2. binary-like input normalization
3. `hash.ts`
   1. SHA-256 wrapper around `crypto.subtle.digest`
4. `cbor.ts`
   1. minimal encoder used for COSE/authData payload assembly

## Notes

1. CBOR implementation is intentionally minimal for this project shape.
2. No decoder is included currently.
