# ADR-0001: Counter utility core — actual parent-authored fixture ADR

## Status
Proposed

## Date
2026-10-05

## Last Verified
2026-10-05 — document/fixture inputs only; current engine validation NOT ASSESSED.

## Decision Makers
Current Codex parent; no independent participant or human acceptance of this ADR.

## Summary
Keep bounded integer arithmetic pure and separate from configured maximum selection.
The caller must validate the shared maximum; conflicting GDD values block that wrapper.

## Engine Compatibility
| Field | Value |
|---|---|
| **Engine** | Godot 4.3 — declared synthetic project record, not installed verification |
| **Domain** | Core |
| **Layer** | Foundation |
| **Knowledge Risk** | NOT ASSESSED — no verified engine docs/probe |
| **References Consulted** | records/toolchain/godot/VERSION.md via engine-reference resolver |
| **Post-Cutoff APIs Used** | None in this pure Python fixture; no Godot API claim |
| **Verification Required** | Actual Godot project/toolchain/API tests before any engine port |

## ADR Dependencies
| Field | Value |
|---|---|
| **Depends On** | None — no prior ADRs found in this fixture |
| **Enables** | None |
| **Blocks** | Future configured-counter wrapper until GDD maximum is reconciled |
| **Ordering Note** | Draft does not unblock stories; only authorized acceptance may do so |

## Context
The current pure function satisfies the minimal arithmetic story, but later synthetic
GDDs add a shared configured maximum and currently disagree (5 versus 3). Preserve
the pure operation and place config validation at a named caller boundary. No engine,
deadline or measured performance requirement was supplied; these remain unknown.

## Decision
Keep increment(value:int, limit:int) -> int pure. It rejects booleans/non-integers
with TypeError, invalid integer ranges with ValueError and returns min(value+1,limit).
A future configured-counter caller must reject limit outside 0..shared maximum,
before calling increment. Do not hardcode either disputed maximum into this ADR.

### Architecture
shared maximum -> configured caller validation -> increment -> bounded result

### Key Interfaces
increment(value, limit): type/range checks and clamp only.
configured caller: maximum resolved from the reconciled shared design source.

### Implementation Guidelines
Must keep arithmetic free of IO/global engine state. Must never silently choose
between contradictory GDD maxima. Must retain actual boundary/type tests. Must not
describe Python tests as engine integration tests.

## Alternatives Considered
1. Hardcode maximum in increment: simple, but duplicates design config and breaks the
   existing generic arithmetic contract; rejected.
2. Engine node/service: integrates lifecycle, but adds unverified engine coupling to
   a pure operation; rejected for this nongame fixture. Reconsider only for an actual port.

## Consequences
Positive: deterministic, independently testable arithmetic; one caller owns config.
Negative: requires a wrapper and GDD reconciliation before configured-limit coverage.

## Risks
Inconsistent maxima can produce contradictory outcomes. Mitigation: fix design
contracts before wrapper implementation; actual current contradiction remains open.
No current Godot compatibility proof. Mitigation: verify real engine/project later.

## GDD Requirements Addressed
| GDD / Requirement | How addressed |
|---|---|
| counter TR-counter-001/002/003 | Proposed pure integer interface/type/range/clamp behavior |
| limits TR-limits-001 | Partial — proposed caller validation; value/ownership must be reconciled |

## Performance Implications
NOT ASSESSED — no actual engine/platform benchmarks or budgets; no invented timings.

## Migration Plan
Existing pure source unchanged. No port or wrapper implemented in this review exercise.

## Validation Criteria
Existing four executed nongame tests confirm the arithmetic story only. After design
reconciliation, add above-maximum caller rejection tests; verify actual engine port
against real toolchain if requested. Neither Proposed status nor test presence is approval.

## Related
design/gdd/counter.md; design/gdd/limits.md; evidence/engine-reference.json.

## Actual strategic review
Parent applying TD-ADR: CONCERNS — design max contradiction and engine unknowns remain.
Engine-specialist responsibility: NOT ASSESSED for actual engine compatibility.
GDD sync: read 2/2 relevant GDDs; no renamed interface, but conflicting values flagged.
No Accepted status or independent sign-off claimed.
