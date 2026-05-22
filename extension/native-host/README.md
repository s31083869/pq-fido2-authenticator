# `native-host/`

Native Messaging hosts for platform user verification.

## Files

1. `pq_uv_host.swift`
   1. macOS Touch ID native host executable source
   2. reads one Native Messaging request from stdin
   3. supports:
      1. `uv-request` -> Touch ID prompt
      2. `uv-status` -> readiness/version check (no prompt)
   4. returns one JSON response to stdout, then exits
2. `pq_uv_host_windows.ps1`
   1. Windows Hello native host source
   2. uses `Windows.Security.Credentials.UI.UserConsentVerifier`
   3. supports:
      1. `uv-request` -> Windows Hello prompt
      2. `uv-status` -> readiness/version check (no prompt)
3. `pq_uv_host_windows.cmd`
   1. Windows launcher used by the Chrome Native Messaging manifest

## Native host name

1. `com.scalebear.pqwebauthn_uv`

## Build and install

Use scripts under `scripts/`:

1. `bash scripts/build-native-host-macos.sh`
2. `bash scripts/install-native-host-macos.sh <CHROME_EXTENSION_ID>`
3. `bun run setup:windows-hello -- <CHROME_EXTENSION_ID>`

Notes:

1. installation is one-time per extension id
2. if extension id changes (new unpacked key/profile), re-run install script
