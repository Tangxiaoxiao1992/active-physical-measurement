# Read-only smoke diagnostic

Updated: 2026-09-09 (Asia/Shanghai)

## Failed command

- Task: `smoke-readme-20260909-001`
- Sequence: `2`
- Recorded result: `failed`
- The failure occurred while creating the Codex thread, before any model turn or research command ran.
- The deduplication record was preserved; this task will not be retried automatically.

## Sanitized exception

- Exception type: `openai_codex.errors.InvalidRequestError`
- JSON-RPC code: `-32600`
- Key error: `failed to load configuration: config.toml:119:1: invalid type: map, expected a boolean`
- No credential, user-home path, workspace path, or other personal value is included here.

## Root cause

The installed Python package (`openai-codex==0.147.0`) started its pinned Codex CLI runtime (`0.147.0`). That older runtime interpreted the current nested `features.context_management` configuration as an invalid boolean value. The active desktop Codex runtime (`0.153.4`) successfully parses the same local configuration and can read the existing authenticated account.

## Fix and verification

- Added optional `codex_bin` support to the bridge worker and selected the locally installed desktop Codex runtime in the ignored local configuration.
- Kept `Sandbox.read_only` for remote tasks; `write_enabled` remains `false`.
- Verified SDK initialization and authenticated account access through the selected runtime without running a model task.
- Unit tests after the fix: 10 discovered, 9 passed, 1 upstream Windows-only test skipped as designed. A separate live Windows process-tree check had already passed.
- Restarted the bridge successfully. It is idle and waiting for a new task with a sequence number greater than `2`.
- No research experiment was run, and automatic report publication remains disabled.
