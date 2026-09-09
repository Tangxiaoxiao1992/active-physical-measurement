# Remote bridge setup status

Updated: 2026-09-09 (Asia/Shanghai)

## Completed

- The bridge is installed in a local directory separate from the research workspace, using a dedicated virtual environment.
- Python: 3.11.2.
- Official Python Codex SDK: `openai-codex==0.147.0` with bundled runtime `openai-codex-cli-bin==0.147.0`.
- The bridge now explicitly uses the compatible local desktop Codex runtime `0.153.4`; the path is kept only in the ignored local configuration.
- SDK authentication was verified by initializing the bundled runtime and reading the signed-in account state. No model task was run for this check, and no credential values were printed or uploaded.
- GitHub repository read/write was verified by publishing `progress/bridge-status.json` and reading the same payload back through the GitHub API.
- Unit tests after the compatibility fix: 10 discovered; 9 passed and the upstream Windows-specific test was skipped as designed. A separate live Windows validation confirmed that tree termination stopped both a test worker process and its child process.
- The bridge was restarted and its uploaded heartbeat reports `execution_enabled=true`.

## Active safety configuration

- `execution_enabled`: **true**
- `write_enabled`: **false** (remote tasks are read-only)
- `publish_report`: **false** (automatic report return is **not enabled**)
- No paid research experiment has been started.
- GitHub credentials remain in the local credential manager/process environment and are not stored in this repository.

## Pending / unresolved

- The first read-only smoke task (`smoke-readme-20260909-001`, sequence 2) failed before model execution because the SDK's pinned runtime could not parse a newer local configuration shape. The sanitized analysis is in `progress/smoke-diagnostic.md`.
- The runtime compatibility issue is fixed locally, the bridge has been restarted, and it is waiting for a new, unexpired remote read-only smoke command with a sequence number greater than 2.
- Automatic report publication will remain disabled until the smoke result is reviewed for public-safe content.
- End-to-end remote command checks for duplicate suppression, timeout, and targeted stop remain to be completed after the smoke task; local validation and unit coverage have passed.
- Windows sign-in startup registration remains to be finalized after the end-to-end smoke check.
