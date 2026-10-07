# Runtime and maintainer tools

Installed commands use the consumer's Python environment and an explicit project root:

```text
<runtime-python> <project-root>/.game-studio/runtime/studio.py --help
<runtime-python> <project-root>/.game-studio/runtime/studio.py config --root <project-root>
<runtime-python> <project-root>/.game-studio/runtime/studio.py recover --root <project-root>
```

| Command | Purpose and boundary |
|---|---|
| `config`, `settings` | Resolve YAML precedence or edit supported settings; configuration grants no permissions |
| `recover`, `checkpoint` | Read optional context or save an explicitly authored checkpoint; no inferred completion |
| `artifacts` | Observe catalog paths, alternatives, patterns and denominators; presence is not quality |
| `stories` | Enumerate story status, counts and next action; missing inputs do not imply completion |
| `dependencies` | Inspect declared ADR edges, missing targets/declarations, cycles and order |
| `gdd-structure` | Observe GDD headings; professional tier/quality verdicts remain in the skill |
| `receipts`, `review-scope` | Link SHA-256 inputs and context to an actual review report; drift widens scope |
| `engine-reference`, `coherence` | Resolve project authority and compare recorded toolchain facts; probe only when explicitly requested |
| `run` | Execute a reviewed configured argv command and record exit code/output/time; `shell=False` is not a sandbox |
| `hooks` | Print optional native definitions; no automatic registration or trust |

Use each command's `--help` for arguments. Read
[review receipts](../.game-studio/resources/docs/review-receipts.md),
[engine resolution](../.game-studio/resources/docs/engine-reference-resolution.md),
[context](../.game-studio/resources/docs/context-management.md) and
[hooks](../.game-studio/resources/docs/hooks-reference.md) for detailed contracts.
There is no automatic legacy Markdown conversion, notification emulation,
instruction transcript scraping, statusline replacement or shell approval interceptor.

## Maintainer commands

| Tool | Purpose |
|---|---|
| `tools/studio.py` | Distribution install/upgrade and runtime command entry point |
| `tools/validate.py` | Native metadata, interfaces, document links/anchors, evaluation catalog and payload hashes |
| `tools/build_release.py` | Validate reviewed content, then rebuild release integrity hashes |
| `tools/integration_sample.py` | Install/recover/reinstall and execute test/source packaging in a temporary nongame consumer; print JSON |
| `tools/probe_codex.py` | Optional read-only installed skill discovery through Codex CLI app-server; no model calls or trust changes |

Tests and samples use temporary directories and do not require historical host files
or Git history. The integration sample prints evidence to stdout without updating
tracked documents. CI runs validation, unittests and the sample on Windows, macOS and
Linux with Python 3.11/3.12. Use the [contributor guide](../CONTRIBUTING.md) for the sequence.
