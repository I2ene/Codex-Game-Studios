# Automation migration

Source shell/settings files are retained only as upstream audit material; they are
excluded from consumer installs. Native commands take an explicit project root and
emit JSON observations or actual execution receipts. No script selects a model,
grants an approval, commits, pushes, trusts hooks or installs an engine.

| Upstream file | Native treatment | Verification / limitation |
|---|---|---|
| yaml-helper.sh | config.py, explicit config/settings CLI | per-leaf/local/rigor, enums, malformed/duplicate YAML, legacy mirrors, scalar testing.strict |
| artifact-check.sh | artifacts | catalog globs, any_of, patterns, denominators, NO_CHECK; presence is not quality |
| story-status.sh | stories | actual story status enumeration; empty inputs NOT ASSESSED |
| adr-dep-graph.sh | dependencies | declared dependency edges, cycles and missing targets; professional review applies verdict |
| gdd-structure-check.sh | gdd-structure | headings only, tier judgments remain in skill |
| review-receipts.sh | receipts | SHA-256 JSON content/section receipts, changes/removals/unresolved patterns; legacy SHA-1 logs need fresh baseline |
| review-scope.sh | review-scope | native hash baseline plus declared dependency context; conservative full scope without baseline |
| project-coherence.sh | coherence | config/engine markers; engine-specific executable/preset checks remain explicit project checks |
| rotate-session-state.sh | checkpoint --save | explicit authored state and content-hash backup; no inferred completion or automatic pruning |
| migrate-v1-config.sh | manual gs-adopt + settings | automatic Markdown conversion/finalization unsupported; preserve old values/mirrors until reconciled |
| godot-parse-check.gd | project-provided parse adapter / run | no engine in framework test environment; Godot execution NOT ASSESSED |
| session-start.sh | optional SessionStart + recover | native handler I/O; actual trusted callback NOT ASSESSED |
| detect-gaps.sh | explicit artifacts/coherence + relevant skill | observable gaps; no full scan before every task |
| pre-compact.sh | optional PreCompact reminder + checkpoint | hook cannot summarize unseen activity |
| post-compact.sh | optional PostCompact recovery | event output shape tested; runtime delivery requires trust |
| session-stop.sh | Stop no-op + explicit authored checkpoint | no forced loop, fabricated session summary or automatic next step |
| log-agent.sh, log-agent-stop.sh | SubagentStart/SubagentStop observations | actual runtime agent fields; parent records real returned work; fixture IDs are not participation |
| log-instructions.sh | unsupported | no stable instruction-read/transcript interface; current instructions are read explicitly |
| notify.sh | unsupported event | no Notification event; use host notifications when separately authorized |
| validate-commit.sh | explicit relevant design/code/data checks | shell parsing interceptor retired; no complete enforcement claim; user/native approvals govern commit |
| validate-push.sh | explicit tests/release checklist | original push gate was advisory; no automatic build or blanket push interception |
| validate-assets.sh | gs-asset-audit + project validators | needs real assets/standards; empty assets NOT ASSESSED |
| validate-skill-change.sh | tools/validate.py + gs-skill-test | native format separately from actual skill task execution |
| statusline.sh | unsupported | host UI remains responsible for status display |
| settings.json | unsupported Claude settings | permissions/statusline ignored; optional native hook definitions generated separately |

Callbacks are not installed automatically. Review generated definitions through
Codex's native hooks browser; changed definitions need trust again. Explicit helpers
work without hooks, custom roles or a team runtime. Shell-based engine examples need
reviewed argv or a project-owned script before execution with the native runner.
