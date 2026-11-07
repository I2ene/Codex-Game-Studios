# Evaluation scenarios: gs-settings

Use the [evaluation policy](../README.md), current native skill and configuration contract.

### Case 1: Inspect actual configuration

Fixture: project YAML selects full rigor but explicitly overrides QA. Resolve per-leaf
values and sources; report the explicit override rather than inferring it from rigor.

### Case 2: Local scope

Fixture: local settings contain a permitted testing leaf and an engine override.
Apply only whitelisted leaves and report the ignored override; preserve unrelated YAML.

### Case 3: Malformed configuration

Fixture: duplicate keys or invalid YAML. Surface the error and preserve the file;
never silently reset it to defaults or borrow a neighboring project's configuration.

### Case 4: Authorized edit and dry run

Fixture: a supported assignment, with an existing human request to edit it. Dry run
reports the intended change without writes. An authorized actual edit updates only
the selected scope and preserves other project facts; no global Codex changes.
- [ ] Do not overwrite an existing YAML mapping with an assignment or silently reset a malformed
  file. Preserve unrelated comments and formatting under the native settings edit contract.

---

### Case 5: View all shows explicit, derived and local values

**Fixture:** Root YAML selects full rigor and collaborative automation, sets Godot and explicit
`docs.density: terse`. Local YAML sets automation autonomous.

**Input:** `$gs-settings` (view all)

**Domain checks:**
- [ ] Resolve the root with native `config`. Show workflow, QA, story granularity, review and
  team size derived from full, with their actual sources. Explicit terse overrides the density
  preset.
- [ ] Report automation as a permitted local override shadowing collaborative. Explain that a
  project-wide key is editable in the shared scope, not locally. Nothing is written.

---

### Case 6: Inspect one derived key and explain the explicit override

**Fixture:** Root sets standard rigor with no `qa.level` and no local override.

**Input:** `$gs-settings qa.level`

**Domain checks:**
- [ ] From native config, show effective standard and its rigor provenance. Explain how an
  explicit shared `qa.level` overrides the preset and is locked against local override. No
  writes.

---

### Case 7: Changing rigor preserves explicit leaves

**Fixture:** Root YAML has minimal rigor, collaborative automation and explicit thorough density. User
authorizes changing rigor to standard.

**Input:** `$gs-settings modes.rigor=standard`

**Domain checks:**
- [ ] Preview/validate the intended shared edit with the native contract and apply only that
  authorization. Keep one modes block and do not modify other leaves.
- [ ] Re-read effective values: standard workflow/QA, balanced granularity, lean review and
  individual team, with explicit thorough density unchanged. Report sources rather than writing
  derived values.

---

### Case 8: Reject an invalid enum without changing files

**Fixture:** Root YAML sets `modes.review_mode: lean`.

**Input:** `$gs-settings modes.review_mode=chaotic`

**Domain checks:**
- [ ] Report the invalid assignment and the allowed review modes; do not ask approval for or
  apply an invalid edit. Keep both configuration files unchanged.

---

### Case 9: A locked local setting leaves both files alone

**Fixture:** Root sets `engine.name: Godot`; no local YAML.

**Input:** `$gs-settings --local engine.name=Unity`

**Domain checks:**
- [ ] Explain that engine.name is project-wide. If the user intends an engine change, direct
  them to the shared engine configuration path under the native contract. Do not create local
  YAML or switch the engine implicitly.

---

### Case 10: A supported local assignment creates only the override

**Fixture:** Root exists with collaborative automation; no local YAML. User authorizes the personal override.

**Input:** `$gs-settings --local modes.automation=autonomous`

**Domain checks:**
- [ ] Validate the permitted assignment, then create `project.local.yaml` with `automation`
  nested beneath `modes`. Root YAML remains unchanged; effective source is local. Variant: no
  root YAML, refuse to create a local-only project.

---

### Case 11: A reserved value is stored but does not enable behavior

**Fixture:** The native effects map marks `accessibility.target` reserved; the key is unset and the user
authorizes a shared assignment. Use a documented nonreserved key as a contrast.

**Input:** `$gs-settings accessibility.target=standard`; then inspect all and inspect the key

**Domain checks:**
- [ ] Before the authorized write, distinguish stored preference from an implemented effect.
  Verify the value persists and surface the documented reservation when inspecting it, without
  inventing runtime readers or claiming the CLI emitted prose it did not.
- [ ] Do not mark a nonreserved key as reserved merely because it mentions reservations in
  prose.

---

### Case 12: An authorized shared write may remain locally shadowed

**Fixture:** Root review lean and automation autonomous; allowed local review override solo. User explicitly
authorizes setting shared review to full.

**Input:** `$gs-settings modes.review_mode=full`

**Domain checks:**
- [ ] Report the solo shadow and unchanged effective value before writing. Automation does not
  expand scope; existing human authorization suffices for the stated write.
- [ ] Only shared review becomes full; local stays solo. Re-read native config to report the
  actual effective value and source.

---

### Case 13: Malformed assignments do not mutate configuration

**Fixture:** Root YAML exists. Test an empty value and an empty key separately.

**Input:** `$gs-settings --local modes.automation=`; separately `$gs-settings =full`

**Domain checks:**
- [ ] Explain the rejected syntax/value and show the applicable assignment form. Both calls
  leave shared and local files unchanged and do not ask to approve malformed input.
