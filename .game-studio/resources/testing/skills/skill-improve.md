# Evaluation scenarios: gs-skill-improve

Professional improvement cases adapted from upstream testing guidance; see
[source attribution](../../../NOTICE.md). Use [evaluation policy](../README.md),
the current native procedure and [quality rubric](../quality-rubric.md).

### Case 1: Observed authorization defect and missing handoff

Fixture: a temporary skill uses an unavailable tool, exceeds human authorization
and omits its next step. Record the actual baseline, diagnose both defects and
propose a bounded correction. Recheck format and affected behavior after the edit;
compare before/after evidence and retain useful domain guidance.

### Case 2: A fix causes a regression

Fixture: adding the handoff accidentally removes a required domain verdict or
prerequisite. Surface the regression and do not claim improvement. Preserve a known
before-copy and restore it within human authorization; do not use a broad Git reset
that discards unrelated work. Report the rollback and remaining failures.
- [ ] The after result must match the observed rerun even if the proposed edit was expected to
  resolve the defect; a predicted improvement is not measured evidence.

### Case 3: Gate skill needs structural and domain correction

Fixture: native metadata has one defect and the category rubric identifies two
mode-coverage defects. Capture both dimensions, correct all three bounded issues,
then recheck metadata and actual gate behavior. A format-only fix cannot pass the
domain review. Preserve the full/lean/solo applicability and missing-input verdicts.
- [ ] Use a sandbox with planted defects rather than relying on the live gate skill to be
  broken. Repair entry metadata in the entry and panel applicability/omission rules in their
  owning procedure; report each touched file.

### Case 4: The skill is already compliant

Fixture: structural checks and representative domain behavior reveal no failure.
Report the evidence and avoid unnecessary rewrites. Unexecuted behavior remains
NOT ASSESSED rather than being declared clean from a static score.
- [ ] Use a purpose-built compliant sandbox fixture. Treat the clean live state as unproven
  until actual inspection and representative exercise.

### Case 5: Meta-utility does not require a director gate

Fixture: the improvement targets a bounded native skill defect. No game production
phase is advancing. Do not invent director sign-off or launch a mandatory roster.
Use actual authorized review evidence and report participants accurately.

### Case 6: Equal results do not establish improvement

Fixture: the proposed edit leaves the original defect and introduces no measurable
benefit. Compare observed results and report no improvement. Do not describe the
change as a successful repair, silently keep a regression or turn missing evidence
into a pass; explain the remaining issue and justified rollback decision.

---

### Case 7: Multi-file regression restores exactly the changed files

**Fixture:** Sandbox skill has `SKILL.md`, `references/1-gather.md` and `references/2-report.md`. Metadata
and report handoff have planted defects. Proposed patch touches entry and report only, but rerun
finds the report has lost a required verdict and prerequisite. Rollback is authorized.

**Input:** `$gs-skill-improve <sandbox-skill>`

**Domain checks:**
- [ ] Inspect the relevant linked files and locate each defect in its owning file. Record the
  exact pre-edit contents of both changed files; keep report fixes in the report reference.
- [ ] Recheck affected structure and behavior; derive the regression finding from the rerun, not
  expected improvement. Restore exactly both changed files from saved contents; leave
  `1-gather.md` and unrelated edits alone, without a broad Git reset.
