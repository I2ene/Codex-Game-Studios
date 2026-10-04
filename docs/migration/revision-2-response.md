# Astra round 2 response — R7/R8

Reviewed baseline: `3e93dc2842a7bfcd1659bca4266cebd646ed8626` plus test-only
`dd0dc4390bff6c14a73a540809016cff1a15123d`. Astra confirmed the first six repairs
and accepted the declared parent-workflow sample scope. Both remaining P2 were
independently reproduced locally before repair: three focused cases failed.

R7: ordinary relative script paths now resolve from actual run cwd, the consumer
root. engine.project_root inspects marker files and never changes commands/cwd.
Recognized Godot resource URIs and export presets follow actual --path, defaulting
to consumer root when omitted. Custom resource adapters, ambiguous/missing/outside
--path or unobservable paths remain NOT ASSESSED. Regression proves a root Python
runner exits 0/MATCH with a nested engine project, and its absent root counterpart
exits nonzero/DIFFERS even when another copy exists under the engine folder.
Godot resource/preset explicit/omitted --path and unknown adapters are covered.

R8: reviewed patterns are required by default; snapshot generation explicitly
declares applicable optional patterns using repeated --optional-pattern. Companion
JSON saves this classification; check inherits it and rejects late reclassification.
Old companions without optional_patterns remain conservative. Stable absent declared
optional inputs remain named unknowns without widening scope. Appearance, content
change and deletion invalidate scope. Missing required inputs still widen scope and
block unsupported verdict reuse. changed now reports actual GDD changes; wider
scope no longer fabricates changed files. Shared contract and all three review
consumers document the required/optional interface.

Validation: 26 targeted interface/helper tests executed, no failures; this includes
real Python runner positive/negative execution and CLI generation/check/classification.
The original red cases and new required-missing/optional change cases are covered.
Fresh format, payload integrity and cross-platform CI results are tracked separately
in verification.md. No repeated full model-workflow run is needed for the unchanged
professional procedures; the prior sample retains its exact payload hash and scope.

User-assigned Astra/high final re-review: PASS at 81d5877afdfea1754cff89ef28b53e2bd65997e2;
R1–R8 closed. No main merge is authorized.

Follow-up: Astra accepted R8 but found the remaining plain Godot --script branch.
Recognized Godot --script/-s relative paths now use the same run project path as
res://. Host Python paths remain at the consumer root. Both flag forms have a new
red→green root-only/project-only regression; no actual Godot run is implied.
Godot 4.3 explicitly changes cwd for --path and loads --script with ResourceLoader:
[main.cpp](https://github.com/godotengine/godot/blob/4.3-stable/main/main.cpp).
The new expanded matrix plus three related cases passed after correcting the
intermediate short-option ambiguity. Final six-environment CI succeeded; Astra
independently verified these cases and accepted the candidate. See independent-review.md.
