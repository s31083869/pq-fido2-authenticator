# `src/options/`

React options page for local extension settings.

## Current Settings

1. `enabled`
   1. toggle hook injection
2. `defaultAlgorithm`
   1. fallback algorithm when RP params are absent
3. `uvMode`
   1. `soft-auto` (trial)
   2. `native-touch-id` (macOS Native Messaging host required)
4. native host status panel
   1. shows ready/not-ready state for Touch ID host
   2. supports manual refresh

## Persistence

1. data key: `pq_settings_v1`
2. storage backend: `chrome.storage.local`
