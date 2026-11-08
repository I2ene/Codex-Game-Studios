# Optional native hooks

Generate definitions with `hooks --root <project-root> --python <runtime-python>`.
The command prints JSON; save/review it separately before configuring Codex. Installer
never writes .codex/hooks.json, .codex/config.toml or trust state. Existing hook sources
are additive, so inspect them before manually integrating definitions.

Supported definitions: SessionStart recovery; PreCompact checkpoint reminder;
PostCompact recovery; Stop no-op; SubagentStart/SubagentStop actual participant fields.
Handlers consume one native event object on stdin and return event-appropriate JSON
on stdout. cwd locates the installed project within a Git boundary. Windows uses
commandWindows and an encoded PowerShell invocation to preserve path quoting.

Non-managed hooks need native review and exact-definition trust; changed hooks need
review again. Never bypass that mechanism. Handler tests do not prove callback delivery.
No PermissionRequest hooks, allow decisions, tool rewriting, transcript parsing,
Notification emulation or automatic commits/pushes. Shell interceptors cannot cover
every tool path or command continuation. Use explicit checks in skills and CI.

Read native-runtime.md for explicit helper interfaces and verification boundaries.
Source: https://learn.chatgpt.com/docs/hooks (verified 2026-10-05).

Use explicit read-guard, write-guard, input and registry checks when relevant.
The upstream read/write/commit interceptors, notification channels, update
cache and role artifact checks are not native hook contracts. Inspect the actual
staged inputs for a commit review; report a Git LFS object you cannot inspect
rather than passing its pointer as parsed game data. A role result names actual
artifacts; missing required work remains a blocker.
