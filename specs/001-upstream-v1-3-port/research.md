# Research decisions

## Frozen sources
- Fork/base: `d25f763918e568cd90c009b84680d21f3f615148` (2.1.0).
- Previously integrated upstream: `05ad7c8a5b8aa2aa86bbd3439ae7cf7295cac418` (1.2.0).
- Target upstream: `abc0de79d6ceb0b5d7aa693945849b3937afbe6a` (1.3.0).
- Verified remote heads at start; 409 entries: 156 added, 250 modified, three renamed.

## Reuse instead of substitution
Decision: reuse upstream scripts/data/templates and port changed workflow blocks into reviewed native shells. Existing native settings/receipts/checkpoints remain their canonical interfaces. Rationale: full upstream behavior plus preserved reviewed fixes. Alternative rejected: wholesale regeneration would regress native authorizations and evidence.

## Configuration and engine facts
Decision: one engines.tsv, nested root precedence with legacy fallback, explicit invalid override diagnostics, explicit argv execution. Rationale: new upstream keys must not strand existing users. Alternatives rejected: duplicate engine constants, guessed root fallback and automatic evaluation of command strings.

## Source ambiguities and reviewed differences
Decision: distinguish engine browser-sketch from one-shot Grow; preserve testable-criterion evidence and path-scoped Git; label parent work and sampled replay bounds. Rationale: conflicting source prose cannot authorize independent signoff, staged-file inclusion or false proof. Native evidence and ownership contracts remain binding.

## Spec Kit onboarding
Decision: official GitHub source tag v1.4.5, isolated uv tool run, Codex skills integration, Python scripts and disabled native events. Initializer ran in an empty ignored staging directory; only non-payload project infrastructure was adopted after managed-file and collision checks. Generated skill instructions are executed by the development agent from staging. Rationale: protect existing AGENTS, native skills and configuration, and exclude all development tooling from consumers. Alternative rejected: force-initializing over non-empty framework paths.

## Validation boundaries
Decision: compare real helper outputs and mutate temporary installed consumers, with a real browser where available. Rationale: static structure is insufficient, while synthetic game exercise does not prove all model scenarios or game quality. Unavailable true Codex sessions, host events, engine builds and human playtests are separately reported.
