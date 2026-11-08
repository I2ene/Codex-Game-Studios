## Project engine reference contract

When engine facts or APIs matter, explicitly run the native engine-reference command
and read .game-studio/resources/docs/engine-reference-resolution.md. <project-engine-reference> means its resolved
project.root and project.documents. Use actual project version/verification records;
missing records remain unknown. Packaged engine versions are historical background,
never project authority. Confirm current official APIs and actual toolchain before claims.

## Native execution contract

Use current project instructions, user authorization and inherited model/permissions.
Read `.game-studio/resources/docs/native-runtime.md` for platform mechanics and only
the domain references needed for this task. Config is an explicit command, not shell
preprocessing. Workflow inputs come from the user's request, not injected variables.
Tool-shaped examples below are procedural briefs; use tools actually exposed by the
host. They do not declare APIs or grant permissions. Existing task authorization
satisfies routine writes already in scope; do not repeat per-file approval questions.

Roles describe expertise. Delegate only when authorized and useful; otherwise apply
the role yourself and label the review as performed by the parent. Never fabricate
participant IDs, independent reviews or sign-off. Record real delegated participants.
Missing evidence means NOT ASSESSED — NO DATA. Resolve engine/version from this
project; engine reference versions are examples and require current verification.


Explicitly resolved — use as-is; `--review` overrides `review_mode`. No block →
defaults in `.game-studio/resources/docs/config-resolution.md`.

## Resolve this run's settings

Run `python .game-studio/runtime/studio.py config --root <project-root>` explicitly. Use effective values and provenance. Duplicate keys or malformed YAML are errors: inspect and repair the source configuration before dependent writes or commands; no merged values are authoritative after an error.



## Native phase execution

Every referenced phase inherits the native contracts above. Role or agent wording
describes a professional responsibility: apply it in the parent when delegation is
unavailable or unauthorized, read its gate file yourself, and label parent work.
Only actual delegated participants count as independent reviews. Existing task
authorization covers in-scope writes and implementation; later example approval
questions are for unresolved choices, not a requirement to ask again per file.
Bash helpers under .game-studio/scripts require a compatible shell and the consumer
root as working directory; inspect their TSV output. Native studio.py commands use
--root explicitly and emit JSON; never parse them as historical colon-prefixed rows.

# Phase Gate Validation

This skill validates whether the project is ready to advance to the next development
phase. It checks for required artifacts, quality standards, and blockers.

**Distinct from `$gs-project-stage-detect`**: That skill is diagnostic ("where are we?").
This skill is prescriptive ("are we ready to advance?" with a formal verdict).

## Production Stages (7)

The project progresses through these stages:

1. **Concept** — Brainstorming, game concept document
2. **Systems Design** — Mapping systems, writing GDDs
3. **Technical Setup** — Engine config, architecture decisions
4. **Pre-Production** — Prototyping, vertical slice validation
5. **Production** — Feature development (Epic/Feature/Task tracking active)
6. **Polish** — Performance, playtesting, bug fixing
7. **Release** — Launch prep, certification

**When a gate passes**, or a CONCERNS override is valid and explicitly accepted, use [6-update-stage.md](6-update-stage.md) to update project.stage and verify the native result.

---

## 1. Parse Arguments

**Target phase:** `the workflow inputs` with any `--review <mode>` pair removed (blank = auto-detect current stage, then validate next transition). `$gs-gate-check --review full` names no phase.

Note: in `solo` mode, director reviews (CD-PHASE-GATE, TD-PHASE-GATE, PR-PHASE-GATE, AD-PHASE-GATE) are skipped — gate-check still applies artifact and quality checks but skips director review. In `lean` mode, the phase-gate directors still run (phase gates are the purpose of lean mode); how many of them run is set by `workflow` below.

**`workflow`** (per `.game-studio/resources/docs/workflow-modes.md`):

`gate-check` runs project-wide, so it uses the project-level `workflow` for the
gate's overall artifact checklist (the loaded gate file), AND consults
`workflow_overrides.system_overrides.<system>` per-system when validating MVP
GDDs — a system pinned to a higher tier must meet that tier's section count
before the gate passes, regardless of the project-level workflow (see Section 2b,
"Per-system overrides").

> **gate-check honors `workflow` but is exempt from `automation`.** The artifact
> checklist changes per tier; the collaborative prompting protocol (the
> Collaborative Protocol section) always applies — a phase gate is a deliberate
> human checkpoint, never auto-run.

**`qa.level`**: controls test enforcement at phase gates, where `workflow`
controls which artifacts are required. `modes.rigor` sets both together; set
`qa.level` explicitly to vary enforcement alone. At `minimal`, no test gates apply — the
test-evidence and unit-test artifact items become non-required and the
Section 3 `testing.strict` check is a no-op; the smoke check is not relaxed (Section 2b) —
but at this level `$gs-smoke-check` runs without game tests (its automated row reads
WAIVED), so the build check (`commands.smoke`, else `commands.build`, when set) and
the launch and critical-path checks are the floor — a build nobody launched is
NOT ASSESSED — and a project with no tests can still pass. At `standard`,
Logic + Integration tests must pass. At `full`, a full coverage check + regression suite are required
(coverage minimum from `qa.coverage_minimum` if set). The retained screenshots
UI and Visual/Feel stories need are not test items: no `qa.level` relaxes them
(Section 2b).

**`team.size`**: does not change how many director perspectives are applied at a phase gate — panel
width is `workflow`'s axis (Section 4b). This value affects only the
**specialist depth within each director's review**.
`individual` uses the core specialist set; `small` the standard set; `studio`
adds engine sub-specialists. It never skips a director — skipping directors is
`review_mode`'s job. Both `review_mode` and `team.size` are set by
`modes.rigor` — one rigor choice sets both — and each still overrides that axis
when set explicitly (a full-rigor project gets the `studio` set; lighter tiers
get `individual`).

- **With argument**: `$gs-gate-check production` — validate readiness for that specific phase
- **No argument**: Auto-detect current stage using the same heuristics as
  `$gs-project-stage-detect`, then **confirm with the user before running**:

  Use `ask the user`:
  - Prompt: "Detected stage: **[current stage]**. Running gate for [Current] → [Next] transition. Is this correct?"
  - Options:
    - `[A] Yes — run this gate`
    - `[B] No — pick a different gate` (if selected, show a second widget listing all gate options: Concept → Systems Design, Systems Design → Technical Setup, Technical Setup → Pre-Production, Pre-Production → Production, Production → Polish, Polish → Release)

  Do not skip this confirmation step when no argument is provided.

---

## 2. Phase Gate Definitions

Each gate's checklist — required artifacts, quality checks, and its workflow-tier
reductions — lives in its own file. **Read only the row for the target phase
transition; never load the others.**

| Gate | Definition file |
|------|-----------------|
| Concept → Systems Design | [gate-systems-design.md](gate-systems-design.md) |
| Systems Design → Technical Setup | [gate-technical-setup.md](gate-technical-setup.md) |
| Technical Setup → Pre-Production | [gate-pre-production.md](gate-pre-production.md) |
| Pre-Production → Production | [gate-production.md](gate-production.md) |
| Production → Polish | [gate-polish.md](gate-polish.md) |
| Polish → Release | [gate-release.md](gate-release.md) |

Each file states the `full` baseline first, then the `standard` and `minimal`
reductions for that gate. Apply the tier resolved in Section 1.

## 2b. Workflow Tier Adjustment

**Read [2b-workflow-tier.md](2b-workflow-tier.md) now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 3. Run the Gate Check

**Read [3-run-gate-check.md](3-run-gate-check.md) now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 4. Collaborative Assessment

**Read [4-assessment.md](4-assessment.md) now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 5. Output the Verdict

**Read [5-verdict.md](5-verdict.md) now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 6. Update Stage on PASS

**Read [6-update-stage.md](6-update-stage.md) now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 7. Closing Next-Step Widget

**Read [7-next-steps.md](7-next-steps.md) now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Collaborative Protocol

This skill follows the collaborative design principle:

1. **Scan first**: Check all artifacts and quality gates
2. **Ask about unknowns**: Don't assume PASS for things you can't verify
3. **Present findings**: Show the full checklist with status
4. **User decides**: The verdict is a recommendation — the user makes the final call on
   what to do next; only the stage write is bound to it (Section 6)
5. **Get approval**: "May I write this gate check report to production/gate-checks/?"
6. **Never auto-fix**: If required artifacts are missing, report the FAIL verdict and
   name the skill to run (e.g. "run `$gs-test-setup`"). Do NOT create missing files or
   re-run the gate automatically. Creating files to manufacture a PASS defeats the
   gate's purpose.

**Never** block a user from working — the verdict decides only whether this skill
writes the new stage. On CONCERNS the user may advance by explicitly accepting the
listed risks, which the report records (Section 6); on FAIL or NOT ASSESSED the
stage stays where it is until a re-run passes, and nothing stops the user working
on the blockers meanwhile.
