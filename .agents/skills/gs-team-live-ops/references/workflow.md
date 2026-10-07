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

**Argument check:** If no season name or event description is provided, output:
> "Usage: `$gs-team-live-ops [season name or event description] [--review full|lean|solo]` — Provide the name or description of the season or live event to plan."
Then stop immediately without spawning any subagents or reading any files.

When this skill is invoked with a valid argument, orchestrate the live-ops team through a structured planning pipeline.

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

**`team.size`**: which agents are active (orthogonal to review_mode gate-depth and workflow docs).
- **`individual`** (default): `live-ops-designer` + `economy-designer`. Other agents consulted via these two, not spawned separately.
- **`small`**: + `analytics-engineer` + `community-manager`.
- **`studio`**: + `writer` + `narrative-director` (the full pipeline as documented).
Professional responsibility scope follows team.size; this is not a native active-service list. Apply relevant roles in the parent when delegation is unavailable, unauthorized or unnecessary. Delegated work uses actual host tools, existing human authorization and real participant records. Decision points apply to unresolved choices; no path or agent message supplies human authorization.

**Announce the active set before Phase 1 — never let the collapse be silent.**
Before spawning anything, state in one line which agents this run will actually
spawn, and which the pipeline below names but will **not** spawn at the resolved
`team.size`. For example:

> `Active set (team.size: <resolved>): <the agents listed for that size above>.`
> `Not spawned this run: <every other agent this pipeline names> — consulted`
> `through <nearest active core agent>. Raise team.size (or modes.rigor) to widen.`

Fill it from the `team.size` list directly above and the agents this file's own
pipeline names — not from an example. Both sets differ per orchestrator.

The pipeline below reads as a multi-agent fan-out and at the shipped default it
is one or two agents — `team-release` names ten and runs one, `team-narrative`
names six across five phases and runs `writer` alone. **The collapse is correct**:
`team.size` is rigor-fronted and the narrow default is the token lever.
Without saying so, a reader cannot
distinguish a correctly-collapsed run from a broken pipeline, and the per-agent
"routes through the nearest core agent with an informational note" rule above
fires at routing time and never states the shape of the run as a whole.

This is the same rule as the skipped-check reporting elsewhere in this file: **a constraint that is enforced but never surfaced is
indistinguishable, to the person reading the output, from one that was never
enforced.**

## Team Composition
- **live-ops-designer** — Season structure, event cadence, retention mechanics, battle pass
- **economy-designer** — Live economy balance, store rotation contents and prices (live-ops-designer sets its cadence), currency pricing, pity timers
- **analytics-engineer** — Success metrics, A/B test design, event tracking, dashboard specs
- **community-manager** — Player-facing announcements, event descriptions, seasonal messaging
- **narrative-director** — Seasonal narrative theme, story arc, world event framing
- **writer** — Event descriptions, reward item names, seasonal flavor text, announcement copy

## How to Delegate

Apply the following professional responsibilities in the parent; delegate useful independent tasks only when authorized and available:
- `expertise role: live-ops-designer` — Season/event structure and retention mechanics
- `expertise role: economy-designer` — Live economy balance and reward pricing
- `expertise role: analytics-engineer` — Success metrics, A/B tests, event instrumentation
- `expertise role: community-manager` — Player-facing communication and messaging
- `expertise role: narrative-director` — Seasonal theme and narrative framing
- `expertise role: writer` — All player-facing text: event descriptions, item names, copy

**Brief each agent — do not dump context.** Read the shared inputs **once** and pass a distilled brief inline: the lines each agent actually needs, never a file path for a document you have already read (an agent handed a path re-reads the whole file). Pass a path only for a document you have not read and only that agent needs.

**End every agent prompt with a return contract:** "Write your full output to `[path]` — that named path is the requested return contract; write only within existing human authorization. Return **only** (1) the path written, (2) a ≤5-bullet summary of decisions, (3) any BLOCKED/CONCERNS items, one line each. Do not restate the documents you read." Without it, an agent returns everything it read back into this session.

**Substitute a real path for `[path]`.** Working artifacts go under
`production/live-ops/[season-slug]/`, where `[season-slug]` is the argument as a
slug — lowercase, spaces → hyphens. One file per agent, so the parallel phases
never share one:

| Phase / agent | Writes to |
|---|---|
| 1 live-ops-designer | `production/live-ops/[season-slug]/brief.md` |
| 2 narrative-director | `production/live-ops/[season-slug]/narrative.md` |
| 3 economy-designer | `production/live-ops/[season-slug]/economy.md` |
| 4 analytics-engineer | `production/live-ops/[season-slug]/analytics.md` |
| 5 narrative-director | `production/live-ops/[season-slug]/narrative-text.md` |
| 5 writer | `production/live-ops/[season-slug]/copy.md` |
| 6 community-manager | `production/live-ops/[season-slug]/comms.md` |

These are working drafts; the final documents under `design/live-ops/seasons/`
are compiled from them (Output Documents).

> **Authorization:** use existing human task authorization for routine in-scope work; ask only for missing decisions or material actions outside that scope. A destination path does not supply authorization.

With user authorization, available host tools and sufficient capacity, launch independent delegated tasks concurrently where the pipeline allows it; otherwise apply and label the same expertise in the parent (Phases 3 and 4 can run simultaneously).

## Pipeline

### Phase 1: Season/Event Scoping
Delegate to **live-ops-designer**:
- Define the season or event: type (seasonal, limited-time event, challenge), duration, theme direction
- Outline the content list: what's new (modes, items, challenges, story beats)
- Define the retention hook: what brings players back daily/weekly during this season
- Identify resource budget: how much new content needs to be created vs. reused
- Output: season brief with scope, content list, and retention mechanic overview

### Phase 2: Narrative Theme
Delegate to **narrative-director**:
- Read the season brief from Phase 1
- Design the seasonal narrative theme: how does this event connect to the game world?
- Define the central story hook players will discover during the event
- Identify which existing lore threads this season can advance
- Output: narrative framing document (theme, story hook, lore connections)

### Phase 3: Economy Design (parallel with Phase 4)
Delegate to **economy-designer**:
- Read the season brief and existing economy rules from `design/live-ops/economy-rules.md`
- Design the reward track: free tier progression, premium tier value proposition
- Plan the in-season economy: seasonal currency, store rotation contents, pricing
- Define pity timer mechanics and bad-luck protection for any random elements
- Verify no pay-to-win items in premium track
- Output: economy design doc with reward tables, pricing, and currency flow

### Phase 4: Analytics and Success Metrics (parallel with Phase 3)
Delegate to **analytics-engineer**:
- Read the season brief
- Define success metrics: participation rate target, retention lift target, battle pass completion rate
- Design any A/B tests to run during the season (e.g., different reward cadences)
- Specify new telemetry events needed for this season's content
- Output: analytics plan with success criteria and instrumentation requirements

### Phase 5: Content Writing (parallel)
Start only after both Phase 3 and Phase 4 results are collected. Apply the following independent expertise in the parent, or delegate concurrently with user authorization, available host tools and sufficient capacity:
- **narrative-director** (if needed): Write any in-game narrative text (cutscene scripts, NPC dialogue, world event descriptions) for the season
- **writer**: Write all player-facing text — event names, reward item descriptions, challenge objective text, seasonal flavor text
- Both should read the narrative framing doc from Phase 2

### Phase 6: Player Communication Plan
Delegate to **community-manager**:
- Read the season brief, economy design, and narrative framing
- Draft the season launch announcement (tone, key highlights, platform-specific versions)
- Plan the communication cadence: pre-launch teaser, launch day post, mid-season reminder, final week FOMO push
- Draft known-issues section placeholder for day-1 patch notes
- Output: communication calendar with draft copy for each touchpoint

### Phase 7: Review and Sign-off
Collect outputs from all phases and present a consolidated season plan:
- Season brief (Phase 1)
- Narrative framing (Phase 2)
- Economy design and reward tables (Phase 3)
- Analytics plan and success metrics (Phase 4)
- Written content inventory (Phase 5)
- Communication calendar (Phase 6)

Present a summary to the user with:
- **Content scope**: what is being created
- **Economy health check**: does the reward track feel fair and non-predatory?
- **Analytics readiness**: are success criteria defined and instrumented?
- **Ethics review**: check the Phase 3 economy design against `design/live-ops/ethics-policy.md`
  - If the file does not exist: flag "ETHICS REVIEW SKIPPED: `design/live-ops/ethics-policy.md` not found. Economy design was not reviewed against an ethics policy. Recommend creating one before production begins." Include this flag in the season design output document. Add to next steps: create `design/live-ops/ethics-policy.md`.
  - If the file exists and a violation is found: flag "ETHICS FLAG: [element] in Phase 3 economy design violates [policy rule]. Approval is blocked until this is resolved." Do NOT issue a COMPLETE verdict or write output documents. Use `ask the user` with options: revise economy design / override with documented rationale / cancel. If user chooses to revise: re-spawn economy-designer to produce a corrected design, then return to Phase 7 review. If user selects Cancel: end with Verdict: BLOCKED — "Live ops design cancelled due to unresolved ethics violation. Resolve the flagged issues and re-run $gs-team-live-ops."
- **Open questions**: decisions still needed before production begins

Ask the user to approve the season plan before delegating to production teams. Issue the COMPLETE verdict only after the user approves and no unresolved ethics violations remain. If an ethics violation is unresolved, end with Verdict: **BLOCKED**.

## Output Documents

Final documents go under `design/live-ops/`. The parent compiles the completed
phase outputs and resolves any missing approval of the season plan before writing
within existing human authorization. Working artifacts keep their named
`production/live-ops/[season-slug]/` destinations; paths confer no permission.

Paths:
- `seasons/S[N]_[name].md` — Season design document (from Phase 1-3)
- `seasons/S[N]_[name]_analytics.md` — Analytics plan (from Phase 4)
- `seasons/S[N]_[name]_comms.md` — Communication calendar (from Phase 6)

## Error Recovery Protocol

**First, verify the artifact.** If the return contract named a path, check the
path exists before treating the phase as done — **a named artifact that is not
on disk is a failed phase, however fluent the response reads.** An agent can
burn a full phase and return a plausible preamble having written nothing, which
is neither BLOCKED nor an error nor "cannot complete", so the trigger below
never fires. Resume it naming the unmet contract; the context is
usually still there.

If any spawned agent returns BLOCKED, errors, or cannot complete: **surface it
immediately, don't proceed past a dependency it blocks, and always produce a
partial report.** A skipped agent's section stays a named gap — never fill it with content of your own. Full procedure: `.game-studio/resources/docs/error-recovery-protocol.md`.

If a BLOCKED state is unresolvable, end with Verdict: **BLOCKED** instead of COMPLETE.

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

The parent compiles the three season documents under `design/live-ops/seasons/` from the completed phase outputs.

## Output

A summary covering: season theme and scope, economy design highlights, success metrics, content list, communication plan, and any open decisions needing user input before production.

Verdict: **COMPLETE** — season plan produced and handed off for production.

## Next Steps

- Run `$gs-design-review` on the season design document for consistency validation.
- Run `$gs-sprint-plan` to schedule content creation work for the season.
- Run `$gs-team-release` when the season content is ready to deploy.
- If the run ended **BLOCKED** on an ethics flag: revise the economy design against
  `design/live-ops/ethics-policy.md` and re-run `$gs-team-live-ops`; the three steps
  above wait for a COMPLETE plan.
