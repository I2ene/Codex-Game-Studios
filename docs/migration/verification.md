# Candidate verification — 2026-10-05

Environment: Windows; Python 3.12.14; PyYAML 6.0.3; Codex CLI 0.160.0.
User/session model and permissions inherited. No private game project installed,
edited or used as a sample. MIT/Donchitos license unchanged.

| Check | Actual result | Boundary |
|---|---|---|
| python tools/validate.py | FORMAT: 74 skills, 49 roles, 485 sources, zero errors | Metadata, entry links, obsolete paths/private coupling; not inference quality |
| python tools/audit_inventory.py | 485 original SHA-256 hashes verified; 123 native/68 replace/289 retain/5 unsupported | Coverage/declared targets; not game outcomes |
| python tools/build_release.py | FORMAT: 2.0.0; 394 payload files | Integrity manifest; not publisher authenticity |
| python -m unittest discover -s tests -v | EXECUTED: 32 tests, 31 passed, one skipped | Windows denied symlink fixture creation; normal/dangling junction rejection executed |
| python tools/integration_sample.py --native-discovery | EXECUTED: installed 74 skills, zero framework/protocol errors; 2 tests and source packaging exit 0; checkpoint PRESENT; reinstall writes 0 | Non-game fixture/read-only discovery; no model inference |

[sample-evidence.json](sample-evidence.json) preserves sanitized actual receipts and
native skill names. The fixture authored a brief/story, copied implementation/tests,
applied a parent review, retained input hashes and completed the story. It exercises
artifacts/helpers, not an autonomous skill-behavior suite or independent director
review. Source ZIP is not an engine/game build or platform release.

Tests cover YAML leaf precedence/local locks/rigor/system overrides, malformed input,
enums/legacy/scalar strict flags, custom engines, optional confined recovery, existing
consumer preservation, edited managed files/blocks, corrupt state/overlap, upgrades,
dry run/removal/normal-failure rollback/locking, temp collision preservation, Windows
junctions, actual success/failure commands, missing evidence, artifacts/story/dependency
observations, review changes/deletions and event-specific hook JSON/date serialization.

Actual independent runtime reviewer: /root/runtime_review, read-only confined repros.
Six material findings repaired and regression-checked. Its suite overlapped edits;
the parent's fresh run above establishes current results. The later user-assigned
Astra candidate review is tracked separately in the review handoff.

NOT ASSESSED: full inference behavior of 74 workflows/49 roles; custom-role launch;
trusted callbacks; game balance/performance; visual/UI/assets/playtests; engine
parse/tests/builds; certification/deployment/live operations. Missing data never
became a pass. No hook was automatically registered or trusted.

CI is configured for Windows/macOS/Linux with Python 3.11/3.12. Local results do not
prove remote environments passed; consult actual PR checks. Abrupt process/OS
termination is nontransactional: inspect/restore before removing orphan install locks.
Section receipts reject # filenames; whole-file receipts support them. Unresolved
dependencies widen review scope. Commands are reviewed argv, not a sandbox.
