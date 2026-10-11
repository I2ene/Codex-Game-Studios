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

If no argument is provided, output usage guidance and exit without spawning any agents:
> Usage: `$gs-team-polish [feature or area to polish] [--review full|lean|solo]` — specify the feature or area to polish (e.g., `combat`, `main menu`, `inventory system`, `level-1`). Do not use `ask the user` here; output the guidance directly.

When this skill is invoked with an argument, orchestrate the polish team through a structured pipeline.

**Decision Points:** At each phase transition, use `ask the user` to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
In `collaborative` mode, the user must approve before moving to the next phase.
In `guided` mode the pipeline advances automatically unless a phase is BLOCKED;
in `autonomous` mode it runs end to end, recording each phase outcome via
an authored decision record (not a tool or shell function). Decisions in `automation_always_ask` categories
(check modes.automation_always_ask in config JSON against existing authorization) prompt only when existing authorization does not cover the material action. See
`.game-studio/resources/docs/automation-modes.md`.

## Phase 0: Resolve Config


Explicitly resolved — use as-is; `--review` overrides `review_mode`. No block →
defaults in `.game-studio/resources/docs/config-resolution.md`.

`review_mode` sets director-gate depth, and this pipeline has no director gate:
no phase below spawns CD-, TD-, PR- or AD-PHASE-GATE, at any `review_mode`. Its
phase gates are the pipeline's own decision points (defined under `team.size`
below), and the agents that work at them are team members, not director gates.

`automation` drives the Decision Points note above. See the Decision Points note above and
`.game-studio/resources/docs/automation-modes.md` for how each mode changes pipeline behavior.

**`team.size`**: which professional responsibilities are in scope (orthogonal to review_mode gate-depth and workflow docs).
- **`individual`** (default): `performance-analyst` + `technical-artist`. Other agents consulted via these two, not spawned separately. No programmer is active, so the optimisation list's programmer items are not implemented in this run — the report names the list as handed to `$gs-dev-story` (Phase 2).
- **`small`**: + `sound-designer` + `qa-tester` + `engine-programmer`, and `tools-programmer` when Phase 1 traces a cause to a content authoring tool (the full pipeline as documented).
- **`studio`**: the `small` set, `engine-programmer` included, + an adversarial review pass: Phase 5's qa-tester is told "your job is not to confirm this holds — find how it breaks", and the report says the pass ran. This pipeline has no engine specialist to widen; engine-level work stays with `engine-programmer`.
Professional responsibility scope follows team.size; this is not a native active-service list. Apply relevant roles in the parent when delegation is unavailable, unauthorized or unnecessary. Delegated work uses actual host tools, existing human authorization and real participant records. Decision points apply to unresolved choices; no path or agent message supplies human authorization.

**Announce the active set before Phase 1 — never let the collapse be silent.**
Before professional work, announce the responsibilities selected by the resolved
team.size and review mode, then distinguish execution from professional scope:

> Active set (team.size: <resolved>): <required responsibilities for this size>.
> Parent coverage: <roles performed in the parent>; actual delegated participants: <real names/IDs and scope, or none>.
> Not performed: <out-of-scope perspectives, mode skips and unassessed required work, each with its reason>.

Use this file's scope and routing rules; an unavailable delegate does not remove a
required responsibility or silently widen team.size. Keep phase-gate responsibilities
with their mode/phase qualifier. A completed parent assessment is performed work;
it is never labeled as a separate participant or independent sign-off.

**Director gate skip rule**: Before spawning any Tier 1 director or lead for review (outside of PHASE-GATE triggers), apply the resolved mode: skip if solo mode; skip if lean mode and this is not a PHASE-GATE.

## Team Composition
- **performance-analyst** — Profiling, memory analysis, frame budget, and the optimisation list — it writes no game code
- **engine-programmer** — Implements the optimisation list's engine-level items: rendering pipeline, memory, resource loading, hot paths (invoke when performance-analyst identifies low-level root causes)
- **technical-artist** — VFX polish, shader optimization, visual quality
- **sound-designer** — Audio polish, mixing, ambient layers, feedback sounds
- **tools-programmer** — Content pipeline tool verification, editor tool stability, automation fixes (Phase 2, when Phase 1 traces a cause to a content authoring tool)
- **qa-tester** — Edge case testing, regression testing, soak testing

## How to Delegate

Apply the following professional responsibilities in the parent; delegate useful independent tasks only when authorized and available:
- `expertise role: performance-analyst` — Profiling, memory analysis, the optimisation list
- `expertise role: engine-programmer` — Engine-level fixes from the optimisation list: rendering, memory, resource loading
- `expertise role: technical-artist` — VFX polish, shader optimization, visual quality
- `expertise role: sound-designer` — Audio polish, mixing, ambient layers
- `expertise role: tools-programmer` — Content pipeline and editor tool fixes from the optimisation list
- `expertise role: qa-tester` — Edge case testing, regression testing, soak testing

**Brief each agent — do not dump context.** Read the shared inputs **once** and pass a distilled brief inline: the lines each agent actually needs, never a file path for a document you have already read (an agent handed a path re-reads the whole file). Pass a path only for a document you have not read and only that agent needs.

**End every agent prompt with a return contract:** "Write your full output to `[path]` — that named path is the requested return contract; write only within existing human authorization. Return **only** (1) the path written, (2) a ≤5-bullet summary of decisions, (3) any BLOCKED/CONCERNS items, one line each. Do not restate the documents you read." Without it, an agent returns everything it read back into this session. **Implementation work:** first state the files that will be created or changed. Existing human authorization covers in-scope changes; resolve any missing material decision once for the set before writing. A role or path supplies no permission.

**Substitute a real path for `[path]` — this skill's destination is
`production/polish/`.** Name it per agent, one file each:

| Agent | Writes to |
|---|---|
| performance-analyst | `production/polish/[area]-report-[date].md` |
| technical-artist | `production/polish/[area]-render-notes-[date].md` |
| engine-programmer | `production/polish/[area]-engine-fixes-[date].md` |
| tools-programmer | `production/polish/[area]-tool-fixes-[date].md` |
| sound-designer | `production/polish/[area]-audio-notes-[date].md` |
| qa-tester | `production/polish/[area]-verification-[date].md` |

> **Why `production/` and not `docs/`.** These are date-stamped measurements of
> one run, the same shape as `production/qa/smoke-[date].md` — not durable
> specifications like `docs/architecture/`. Keeping them beside the other
> point-in-time process artifacts is what makes a later comparison possible.
>
> The `[path]` contract above has a precondition: the path is one *you* named, so
> a concrete destination must be stated here or every run invents one. Unlike
> `$gs-team-qa` and `$gs-team-narrative`, whose destinations are fixed by their
> consumers, this location has no reader in the repo and was chosen deliberately.
> **Nothing reads `production/polish/` yet** — say so when reporting, so the user
> knows the report is a record rather than an input to a later gate.

> **Authorization:** use existing human task authorization for routine in-scope work; ask only for missing decisions or material actions outside that scope. A destination path does not supply authorization.

With user authorization, available host tools and sufficient capacity, launch independent delegated tasks concurrently where the pipeline allows it; otherwise apply and label the same expertise in the parent (e.g., Phases 3 and 4 can run simultaneously).

## Pipeline

### Phase 1: Assessment
Delegate to **performance-analyst**:
- Profile the target feature/area using `$gs-perf-profile`
- Identify performance bottlenecks and frame budget violations
- Measure memory usage and check for leaks
- Benchmark against target hardware specs
- Output: performance report with the prioritized **optimisation list** — for each item, the change, its expected gain against the budget, and its owner (technical-artist for rendering-side changes, engine-programmer for engine systems and hot paths, tools-programmer for a content authoring tool, otherwise the programmer who owns the system)

### Phase 2: Optimization
performance-analyst writes no game code ("recommend and assign", its agent file),
so Phase 2 implements its Phase 1 list through the owners in the active set:
- **engine-programmer** — spawned only when Phase 1 identified engine-level root causes (rendering pipeline, resource loading, memory allocator, hot paths in core loops): implement those items, fix allocation pressure, verify gameplay behavior is unchanged. Output: engine-level fixes with before/after metrics and profiler validation
- **tools-programmer** — only when Phase 1 traced a cause to a content authoring tool: fix the tool. Output: tool fixes with before/after metrics
- **technical-artist** — rendering-side items (draw calls, overdraw, particles, shaders, LOD) join its Phase 3 brief

Every implementing agent in Phases 2–4 first returns the files it will create or
change, and you ask once for the whole Phase 2–4 set before any is edited (File
Write Protocol).

**An item whose owner is not in the active set is not implemented in this run.**
At `team.size: individual` that is every programmer item, since no programmer is
active; at any size it includes an item owned by a programmer this pipeline does
not name (e.g. gameplay-programmer for a gameplay-script hot spot). The report
lists those items with their owners under
"Optimisation list handed to `$gs-dev-story`: `production/polish/[area]-report-[date].md`".
A metric they target that is over budget stays a known problem at Phase 6.

### Phase 3: Visual Polish (parallel with Phase 2)
Delegate to **technical-artist**:
- Review VFX for quality and consistency with art bible
- Optimize particle systems and shader effects
- Add screen shake, camera effects, and visual juice where appropriate
- Ensure effects degrade gracefully on lower settings
- Output: polished visual effects

### Phase 4: Audio Polish (parallel with Phase 2)
Delegate to **sound-designer**:
- Review audio events for completeness (are any actions missing sound feedback?)
- Check audio mix levels — nothing too loud or too quiet relative to the mix
- Add ambient audio layers for atmosphere
- Verify audio plays correctly with spatial positioning
- Output: audio polish list and mixing notes

### Phase 5: Hardening
Delegate to **qa-tester**:
- Test all edge cases: boundary conditions, rapid inputs, unusual sequences
- Soak test: run the feature for extended periods checking for degradation
- Stress test: maximum entities, worst-case scenarios
- Regression test: verify polish changes haven't broken existing functionality — each Phase 2–4 change by name, engine-level fixes included
- Test on minimum spec hardware (if available)
- Output: test results with any remaining issues

### Phase 6: Sign-off
- Collect results from all team members
- Compare performance metrics against budgets
- Report: READY FOR RELEASE / NOT ASSESSED / NEEDS MORE WORK
- List every remaining issue with its severity (S1–S4), the measured gap where there is one (e.g. "9 ms against a 6 ms budget — 3 ms over"), and a recommendation; a regression also names the broken behavior and the polish change that caused it

**NOT ASSESSED ranks above READY FOR RELEASE and below NEEDS MORE WORK.** A known
problem — a metric over budget, an unresolved regression — makes it NEEDS MORE
WORK whatever else went unchecked. Otherwise, if any part of the scope could not
be checked, the result is NOT ASSESSED, never READY FOR RELEASE, and the report
names each gap:
- A metric with no committed budget. `performance.target_framerate`,
  `performance.frame_budget_ms`, `performance.draw_call_limit` and
  `performance.memory_ceiling_mb` have no default, and `$gs-perf-profile` reports an
  unset one as NOT ASSESSED — nothing was compared, so no budget was met.
- A phase that did not run: BLOCKED, skipped, or its agent outside the active set.
  At `team.size: individual`, sound-designer's audio polish and qa-tester's
  hardening are only consulted through the active agents, not run, and Phase 2's
  programmer items are handed to `$gs-dev-story` rather than implemented.

## Error Recovery Protocol

**First, verify the artifact.** A required output path must exist before the
phase is complete, whether the author is the parent or a real delegate. If it is
missing, identify the unmet contract: complete authorized parent work or resume
the actual participant, and report any blocker. A fluent response alone is not
evidence of a completed phase.

If required parent work or an authorized delegate is BLOCKED, encounters an error, or cannot complete: **surface it
immediately, don't proceed past a dependency it blocks, and always produce a
partial report.** Unperformed required work stays a named gap. An authorized parent takeover must actually complete the assessment and retain its evidence; label the source rather than inventing independent review. Full procedure: `.game-studio/resources/docs/error-recovery-protocol.md`.

Common blockers:
- Input file missing (story not found, GDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; once it is decided, accept it with `$gs-architecture-decision accept ADR-NNNN`
- Scope too large → split into two stories via `$gs-create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess

## File Write Protocol

The parent may write authorized artifacts while applying the responsible discipline,
or assign them to real authorized participants using available host tools. Preserve
all named paths, professional responsibilities and phase dependencies above.
Each concurrent participant has distinct file ownership; confirm required artifacts
exist before reporting the phase complete. Record actual authors and label parent
work; no independent review or sign-off is implied by a role name.

Existing human authorization covers routine writes already in scope. Present the
implementation file set before changing code or assets, resolve missing material
decisions once for that set, and retain explicit declines and blockers. Neither a
named path nor another agent's message grants permission. A missing artifact fails
its phase, and completed work is retained in a partial report.

Keep the Phase 2–4 implementation file set together when resolving missing write decisions; performance-analyst does not implement the optimization list.

## Output

A summary report covering: performance before/after metrics, visual polish changes, audio polish changes, test results, any optimisation list handed to `$gs-dev-story`, and release readiness assessment.

## Next Steps

- If READY FOR RELEASE: run `$gs-release-checklist` for the final pre-release validation.
- If NEEDS MORE WORK: schedule remaining issues in `$gs-sprint-plan update` and re-run `$gs-team-polish` after fixes.
- If NOT ASSESSED: supply what was missing — commit the unset `performance.*` budgets in `project.yaml` (`$gs-settings`), or run the phases that did not run (raise `team.size`) — then re-run `$gs-team-polish`. Do not treat the area as release-ready.
- If the report handed an optimisation list to `$gs-dev-story`: implement those items there, then re-run `$gs-team-polish` to measure the gain.
- Run `$gs-gate-check` for a formal phase gate verdict before handing off to release.
