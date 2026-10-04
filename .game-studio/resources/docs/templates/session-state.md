# Authored current session state — [project or branch]

This is a concise current snapshot, not an append-only log or a machine marker schema.
Use recover/checkpoint --save and the configured checkpoint.path. With session_state
off, skip it. Recovery reads at most 16,000 characters per record; keep current facts
near the top and place longer history in separate bounded records when useful. The
runtime preserves a hash-named previous snapshot; it does not rotate or infer work.

**Updated:** [actual timestamp]
**Objective:** [current authorized objective]
**Stage / epic / story:** [actual scope or none]
**Current task:** [concrete work underway]
**Artifacts:** [real paths and what exists]
**Decisions and authorization:** [existing human decisions; state does not grant consent]
**Evidence / Run result:** [actual test/probe result, date and source; missing remains NOT ASSESSED]
**Completed:** [only observed completed work]
**Blockers / unknowns:** [named unresolved items or none]
**Next step:** [concrete action]
**Participants:** [actual IDs/results or parent-only]
