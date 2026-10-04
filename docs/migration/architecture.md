# Codex Game Studios 2.0 architecture

Approved scope: a reusable framework installed into arbitrary game repositories;
no game development, private project integrations, global settings or automatic main merge.
Baseline: b21fa0f7f289fc3e726cf36fb12b9bc1e7a51e4d (upstream 1.1.2).

## Distribution

74 namespaced gs-* skills in .agents/skills, 49 inheriting project roles in
.codex/agents, professional resources in .game-studio, and a short managed AGENTS.md
block. Complete workflow procedures and contracts are retained with targeted native
entrypoints. Shared professional content is retained; platform-specific instructions
are replaced, not counted as new game-design knowledge. Original source stays in Git
history and the migration inventory records its hash, disposition and destination.

## Runtime and permissions

Python 3.11+ and PyYAML 6.x. Explicit commands resolve settings, inspect artifacts,
compare review receipts, inspect stories/dependencies, recover context and execute
user-configured test/build commands as argv without a shell. Outputs are observations
or execution receipts; only the relevant skill applies quality judgments. No default
engine, model, approval mode, sandbox setting or agent count is installed.

Roles are expertise, not evidence of delegation. Use them locally unless actual
delegation is authorized and useful. Record participant IDs and returned work. Context
recovery is an optional repository-relative interface, never a personal integration.
Hooks are optional command hooks with event-specific JSON stdin/stdout. They do not
grant approvals, rewrite tools, scrape transcripts, infer completed work or silently
enforce every shell operation. Trust remains a native Codex decision.

## Consumer installation

Preflight all managed files before writing. Preserve existing project configuration,
instructions outside the bounded block, engine files and records. Hash ownership
ledger prevents overwriting edited managed files. Reject unsafe paths, symlink/reparse
traversal, overlapping source/target and corrupt ledgers. Dry runs never write. Roll
back failed writes; unmanaged files are never pruned. Upgrades use the same operation.

## Evidence

Separate format validation, actual helper execution, actual native discovery, and
unassessed game outcomes. Isolated non-game fixtures exercise installation, upgrades,
config/recovery and an applicable design-to-delivery sequence. Synthetic balancing,
performance, build plans or empty inputs do not become game quality evidence.

## Review focus

Existing AGENTS.override.md; duplicate/invalid YAML; managed-file edits; symlinks and
path escapes; unknown engine/version; changed/deleted review inputs; failed commands;
hook trust and event delivery. Keep MIT and original Donchitos attribution unchanged.
