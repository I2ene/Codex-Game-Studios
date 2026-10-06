# Limits — synthetic GDD-shaped input
## Summary
Shared integer maximum for counter utility inputs.
## Overview
Defines the allowed inclusive maximum as 3.
## Player Fantasy
N/A — nongame fixture.
## Detailed Rules
Configured maximum is 3. Callers may choose lower nonnegative integer limits.
## Formulas
0 <= limit <= maximum; maximum = 3.
## Edge Cases
Zero is valid; boolean/string values are not integers for this contract.
## Dependencies
None
## Tuning Knobs
maximum = 3, intentionally one shared source.
## Acceptance Criteria
- TR-limits-001: chosen limit stays in 0..3; invalid choices are rejected by the caller.
