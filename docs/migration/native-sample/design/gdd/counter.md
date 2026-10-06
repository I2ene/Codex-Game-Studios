# Counter utility — synthetic GDD-shaped input
## Summary
Pure bounded integer operation for interface tests; not a game design claim.
## Overview
Increment value by exactly one and clamp to an inclusive limit.
## Player Fantasy
N/A — nongame fixture; no evidence of game experience.
## Detailed Rules
Accept integer value and limit with 0 <= value <= limit. Reject booleans/non-int
with TypeError and invalid integer ranges with ValueError. Shared limits supports
maximum 5; counter examples use cap 5. No IO, engine calls or mutable state.
## Formulas
result = min(value + 1, limit).
## Edge Cases
Zero cap gives zero. At cap returns cap. Negative or over-cap integer rejects.
## Dependencies
- limits.md provides the configured maximum 5.
## Tuning Knobs
limit: caller parameter, range 0..5. No engine/global default.
## Acceptance Criteria
- TR-counter-001: increment(2, 5) returns 3.
- TR-counter-002: increment(5, 5) returns 5; increment(0, 0) returns 0.
- TR-counter-003: invalid type and range inputs raise the stated exception type.
