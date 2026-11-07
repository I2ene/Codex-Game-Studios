# Phase gate stage update

A PASS permits the authorized stage advance. If advancement is not already in the
user's request, present the result and ask before changing the stage.

On CONCERNS, advancement requires explicit acceptance of the listed risks. Record
those risks, the user's decision and date in the report. Do not offer this override
while any required check is NOT ASSESSED. FAIL and NOT ASSESSED never permit a stage
advance: fix the blocker or supply the missing evidence and re-run the gate.

## Write and verify the stage

Run the native assignment, quoting the whole argument when the stage has spaces:

```text
python .game-studio/runtime/studio.py settings "project.stage=<new-stage>" --root <project-root>
python .game-studio/runtime/studio.py config --keys project.stage --root <project-root>
```

Inspect the JSON result and effective project.stage value/provenance. A failed
command or mismatched read-back is a failed update, not an advanced stage. Stop and
report the actual failure. Preserve other configuration and explicit rigor leaves;
do not seed modes.review_mode or write a legacy stage mirror.

### 6.3 Rigor-fit check (advisory — never affects the verdict)

After the stage advance is confirmed, apply the raise trigger in
`.game-studio/resources/docs/settings-guidance.md ` 4`: if the new stage is **Production** (or
later) while the resolved `modes.workflow` is `minimal` (the `rigor: minimal`
posture, from the config block above), add one line:

> "You're entering [stage] on `rigor: minimal` — most projects this size run
> `standard`. Revisit with `$gs-settings modes.rigor=standard`?"

Offer it **once**, here at the gate. Route to `$gs-settings` — never change the
setting yourself.

---
