# Evaluation scenarios: gs-skill-test

Professional cases adapted from upstream testing guidance; see
[source attribution](../../../../NOTICE.md). Use [evaluation policy](../README.md).
Read the native target, complete procedure, relevant rules and category rubric.
These are task-quality criteria, not recorded execution results.

### Case 1: Valid skill structure

Fixture: gs-brainstorm has name/description, a complete linked procedure, appropriate
trigger scope, relevant prerequisites and outputs. Report actual structural checks
and FORMAT success; do not require retired metadata fields or infer task execution.

### Case 2: Authorization and tool boundaries

Fixture: a temporary skill claims an unavailable tool or tells the agent to write
beyond human authorization. Name the defect and its remedy. A valid skill using
existing authorization must not fail merely for omitting blanket per-file prompts.

### Case 3: Gate skill evaluated against its scenario

Fixture: catalog.yaml maps gs-gate-check to its scenario. A balance-rationale criterion
is met by coding-standards.md rather than repeated in the skill; the user declines
an optional results write. Evaluate each applicable domain check, cite the actual
source, retain worst-result handling and do not write declined output. Missing
criteria remain NOT ASSESSED rather than being omitted or marked PASS.

### Case 4: Skill and role coverage audit

Fixture: enumerate installed skills and catalogued roles. Show every entry, accurate
spec coverage and gaps against the actual denominators. Do not sample or imply
behavior passed from coverage. The release catalog covers 74 skills and 49 roles.

### Case 5: Category rubric reveals a gate failure

Fixture: the gate skill omits required discipline coverage at full workflow.
Evaluate every G1–G5 category criterion with individual findings. Name the coverage
gap and reflect it in the overall verdict. Parent-applied reviews may satisfy
applicable discipline coverage when honestly labeled; never invent participation.
Store authorized results outside managed catalog/resources, which are release assets.

### Case 6: Role name resolution and domain redirect

Fixture: gs-creative-director exists as a TOML role, not a skill. Its domain rules
and coordination guidance direct engine decisions to technical-director. Resolve
the role through the catalog, evaluate the redirect and cite both sources. Check
native metadata exactly; settings inherit instead of requiring a model alias.

### Case 7: Unreadable skill is counted

Fixture: one of 74 entries is unreadable, while 73 can be checked. Include the entry
as NOT ASSESSED with its reason, report 73 of 74 checked and reconcile summary
counts. A readable malformed entry is a format failure, a different condition.

### Case 8: Unevaluable assertion affects the verdict

Fixture: one criterion requires a fixture input that is not defined or available.
Report that criterion as NOT ASSESSED with the missing input; the overall result
cannot be a clean PASS. Do not invent data to fill it.

### Case 9: No rubric for a category

Fixture: a catalog entry names a category absent from the quality rubric. Report
NOT ASSESSED and the missing rubric; do not substitute a different category or
produce a zero-failure PASS.

### Case 10: Broken resource link

Fixture: a temporary entry links to a missing procedure. Name the broken link;
static validation cannot report clean format compliance.

### Case 11: Format success without task execution

Fixture: valid metadata has no representative execution evidence. Separate FORMAT
from behavioral NOT ASSESSED, and do not fabricate independent reviewers.

### Case 12: Missing game evidence

Fixture: balance analysis has no formulas or playtest data. Name missing inputs;
no passed game-quality verdict follows from a valid scenario or template.
