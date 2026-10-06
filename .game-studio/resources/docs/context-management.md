# Context and recovery

Read actual project instructions and run `recover --root <project-root>` after a
restart or compaction when recovery helps. Default checkpoint:
production/session-state/active.md. Optional .game-studio/context.json contains
checkpoint and records (repository-relative paths, at most 20 records). Missing
records are reported; paths escaping the project or crossing links are rejected.

Save actual current objective, phase, artifacts, decisions, evidence, remaining work,
known blockers and existing user authorization. Use the session-state template.
`checkpoint --save notes/next-state.md --root <project-root>` saves an explicitly
authored file and preserves the previous checkpoint by its content hash. A hook
cannot infer unseen activity, turn a plan into completion, or scrape a stable transcript.
With features.session_state=off, recovery/saving checkpoints is disabled.

Read references as needed; do not reload all professional manuals per task. Helpers
emit observations, never verdicts. Hash receipts support focused repeat reviews;
new/changed/removed/unresolved inputs invalidate an unchanged claim.
