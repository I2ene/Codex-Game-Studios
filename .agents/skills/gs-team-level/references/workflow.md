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

If no argument is provided, output usage guidance and exit without spawning any agents or reading any design files:
> Usage: `$gs-team-level [level name or area to design] [--review full|lean|solo]` — specify the level or area to design (e.g., `forest temple`, `tutorial village`, `final boss arena`). Do not use `ask the user` here; output the guidance directly.

When this skill is invoked:

**Decision Points:** At each step transition, use `ask the user` to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
In `collaborative` mode, the user must approve before moving to the next step.
In `guided` mode the pipeline advances automatically unless a step is BLOCKED;
in `autonomous` mode it runs end to end, recording each step outcome via
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
- **`individual`** (default): `level-designer` only. Other agents consulted via the level-designer, not spawned separately.
- **`small`**: + `systems-designer` + `art-director` + `qa-tester`.
- **`studio`**: + `narrative-director` + `world-builder` + `accessibility-specialist` (the full pipeline as documented).
Professional responsibility scope follows team.size; this is not a native active-service list. Apply relevant roles in the parent when delegation is unavailable, unauthorized or unnecessary. Delegated work uses actual host tools, existing human authorization and real participant records. Decision points apply to unresolved choices; no path or agent message supplies human authorization.

**Announce the active set before Step 1 — never let the collapse be silent.**
Before professional work, announce the responsibilities selected by the resolved
team.size and review mode, then distinguish execution from professional scope:

> Active set (team.size: <resolved>): <required responsibilities for this size>.
> Parent coverage: <roles performed in the parent>; actual delegated participants: <real names/IDs and scope, or none>.
> Not performed: <out-of-scope perspectives, mode skips and unassessed required work, each with its reason>.

Use this file's scope and routing rules; an unavailable delegate does not remove a
required responsibility or silently widen team.size. Keep phase-gate responsibilities
with their mode/phase qualifier. A completed parent assessment is performed work;
it is never labeled as a separate participant or independent sign-off.

1. **Read the argument** for the target level or area (e.g., `tutorial`,
   `forest dungeon`, `hub town`, `final boss arena`).

2. **Gather context**:
   - Read the game concept at `design/gdd/game-concept.md` — or `design/game-brief.md`,
     the one-page brief that replaces it at `rigor: minimal` — if either exists
   - Read game pillars at `design/gdd/game-pillars.md`
   - Read existing level docs in `design/levels/`
   - Read relevant narrative docs in `design/narrative/`
   - Read world-building docs for the area's region/faction

## How to Delegate

Apply the following professional responsibilities in the parent; delegate useful independent tasks only when authorized and available:
- `expertise role: narrative-director` — Narrative purpose, characters, emotional arc
- `expertise role: world-builder` — Lore context, environmental storytelling, world rules
- `expertise role: level-designer` — Spatial layout, pacing, encounters, navigation
- `expertise role: systems-designer` — Enemy compositions, loot tables, difficulty balance
- `expertise role: art-director` — Visual theme, color palette, lighting, asset requirements
- `expertise role: accessibility-specialist` — Navigation clarity, colorblind safety, cognitive load
- `expertise role: qa-tester` — Test cases, boundary testing, playtest checklist

**Brief each agent — do not dump context.** Read the shared inputs **once** and pass a distilled brief inline: the lines each agent actually needs, never a file path for a document you have already read (an agent handed a path re-reads the whole file). Pass a path only for a document you have not read and only that agent needs.

**End every agent prompt with a return contract:** "Write your full output to `[path]` — that named path is the requested return contract; write only within existing human authorization. Return **only** (1) the path written, (2) a ≤5-bullet summary of decisions, (3) any BLOCKED/CONCERNS items, one line each. Do not restate the documents you read." Without it, an agent returns everything it read back into this session.

**Substitute a real path for `[path]`.** Working artifacts go under
`production/levels/[level-name]/`, slugged as in the "Save to" step below. One
file per agent, so the parallel steps never share one:

| Step / agent | Writes to |
|---|---|
| 1 narrative-director | `production/levels/[level-name]/narrative.md` |
| 1 world-builder | `production/levels/[level-name]/lore.md` |
| 1 art-director | `production/levels/[level-name]/visual-direction.md` |
| 2 level-designer | `production/levels/[level-name]/layout.md` |
| 3 systems-designer | `production/levels/[level-name]/systems.md` |
| 4 art-director | `production/levels/[level-name]/production-concepts.md` |
| 4 accessibility-specialist | `production/levels/[level-name]/accessibility.md` |
| 5 qa-tester | `production/qa/test-cases/[level-name]-cases.md` — test cases, edge cases, playtest checklist, acceptance criteria |

These are working drafts; the durable record is the level design document you
compile from them (`design/levels/[level-name].md`).

> **Authorization:** use existing human task authorization for routine in-scope work; ask only for missing decisions or material actions outside that scope. A destination path does not supply authorization.

3. **Orchestrate the level design team** in sequence:

### Step 1: Narrative + Visual Direction (narrative-director + world-builder + art-director, parallel)

Cover all three disciplines. With user authorization, available host tools and sufficient capacity, issue independent delegated tasks before waiting for results; otherwise apply and label the expertise in the parent.

Apply the `narrative-director` expertise in the parent, or delegate to an authorized participant to:
- Define the narrative purpose of this area (what story beats happen here?)
- Identify key characters, dialogue triggers, and lore elements
- Specify emotional arc (how should the player feel entering, during, leaving?)

Apply the `world-builder` expertise in the parent, or delegate to an authorized participant to:
- Provide lore context for the area (history, faction presence, ecology)
- Define environmental storytelling opportunities
- Specify any world rules that affect gameplay in this area

Apply the `art-director` expertise in the parent, or delegate to an authorized participant to:
- Establish visual theme targets for this area — these are INPUTS to layout, not outputs of it
- Define the color temperature and lighting mood for this area (how does it differ from adjacent areas?)
- Specify shape language direction (angular fortress? organic cave? decayed grandeur?)
- Name the primary visual landmarks that will orient the player
- Read `design/art/art-bible.md` if it exists — anchor all direction in the established art bible

**The art-director's visual targets from Step 1 must be passed to the level-designer in Step 2** as explicit constraints. Layout decisions happen within the visual direction, not before it.

**Gate**: Use `ask the user` to present all three Step 1 outputs (narrative brief, lore foundation, visual direction targets) and confirm before proceeding to Step 2.

### Step 2: Layout and Encounter Design (level-designer)
Apply the `level-designer` expertise in the parent, or delegate to an authorized participant with the full Step 1 output as context:
- Narrative brief (from narrative-director)
- Lore foundation (from world-builder)
- **Visual direction targets (from art-director)** — layout must work within these targets, not contradict them

The level-designer should:
- Design the spatial layout (critical path, optional paths, secrets) — ensuring primary routes align with the visual landmark targets from Step 1
- Define pacing curve (tension peaks, rest areas, exploration zones) — coordinated with the emotional arc from narrative-director
- Place encounters with difficulty progression
- Design environmental puzzles or navigation challenges
- Define points of interest and landmarks for wayfinding — these must match the visual landmarks the art-director specified
- Specify entry/exit points and connections to adjacent areas

**Adjacent area dependency check**: After the layout is produced, check `design/levels/` for each adjacent area referenced by the level-designer. If any referenced area's `.md` file does not exist, surface the gap:
> "Level references [area-name] as an adjacent area but `design/levels/[area-name].md` does not exist."

Use `ask the user` with options:
- (a) Proceed with a placeholder reference — mark the connection as UNRESOLVED in the level doc and list it in the open cross-level dependencies section of the summary report
- (b) Pause and run `$gs-team-level [area-name]` first to establish that area

Do NOT invent content for the missing adjacent area.

**Gate**: Use `ask the user` to present Step 2 layout (including any unresolved adjacent area dependencies) and confirm before proceeding to Step 3.

### Step 3: Systems Integration (systems-designer)
Apply the `systems-designer` expertise in the parent, or delegate to an authorized participant to:
- Specify enemy compositions and encounter formulas
- Define loot tables and reward placement
- Balance difficulty relative to expected player level/gear
- Design any area-specific mechanics or environmental hazards
- Specify resource distribution (health pickups, save points, shops)

**Gate**: Use `ask the user` to present Step 3 outputs and confirm before proceeding to Step 4.

### Step 4: Production Concepts + Accessibility (art-director + accessibility-specialist, parallel)

**Note**: The art-director's directional pass (visual theme, color targets, mood) happened in Step 1. This pass is location-specific production concepts — given the finalized layout, what does each specific space look like?

Apply the `art-director` expertise in the parent, or delegate to an authorized participant with the finalized layout from Step 2:
- Produce location-specific concept specs for key spaces (entrance, key encounter zones, landmarks, exits)
- Specify which art assets are unique to this area vs. shared from the global pool
- Define sight-line and lighting setups per key space (these are now layout-informed, not directional)
- Specify VFX needs that are specific to this area's layout (weather volumes, particles, atmospheric effects)
- Flag any locations where the layout creates visual direction conflicts with the Step 1 targets — surface these as production risks

Apply the `accessibility-specialist` expertise in the parent, or delegate to an authorized participant in parallel to:
- Review the level layout for navigation clarity (can players orient themselves without relying on color alone?)
- Check that critical path signposting uses shape/icon/sound cues in addition to color
- Review any puzzle mechanics for cognitive load — flag anything that requires holding more than 3 simultaneous states
- Check that key gameplay areas have sufficient contrast for colorblind players
- Output: accessibility concerns list with severity (BLOCKING / RECOMMENDED / NICE TO HAVE)

Wait for both required review results before proceeding, whether performed in the parent or by actual delegates.

**Gate**: Use `ask the user` to present both Step 4 results. If the accessibility-specialist returned any BLOCKING concerns, highlight them prominently and offer:
- (a) Return to level-designer and art-director to redesign the flagged elements before Step 5
- (b) Document as a known accessibility gap and proceed to Step 5 with the concern explicitly logged in the final report

Do NOT proceed to Step 5 without the user acknowledging any BLOCKING accessibility concerns.

### Step 5: QA Planning (qa-tester)
Apply the `qa-tester` expertise in the parent, or delegate to an authorized participant to:
- Write test cases for the critical path
- Identify boundary and edge cases (sequence breaks, softlocks)
- Create a playtest checklist for the area
- Define acceptance criteria for level completion

4. **Compile the level design document** combining all team outputs into the
   level design template format.

The orchestrator already holds every sub-agent's output — **compile the document
itself; do not re-spawn `level-designer` and re-send all outputs verbatim.** That
second spawn pays a fresh agent's overhead plus a full re-transmission of context
the orchestrator already has, to move text it is already holding. After compiling
into the level-design template format, ask the user directly via
`ask the user`: "May I write the compiled level design to
`design/levels/[level-name].md`?" On approval, write it.

5. **Save to** `design/levels/[level-name].md` after that approval.
   `[level-name]` is the argument as a slug — lowercase, spaces → hyphens
   (`forest dungeon` → `forest-dungeon.md`) — and `[area-name]` in the adjacent
   area check is slugged the same way.

6. **Output a summary** with: area overview, encounter count, estimated asset
   list, narrative beats, any cross-team dependencies or open questions, open
   cross-level dependencies (adjacent areas referenced but not yet designed, each
   marked UNRESOLVED), and accessibility concerns with their resolution status.

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

The parent compiles `design/levels/[level-name].md` from the completed step outputs.

## Next Steps

- Run `$gs-design-review design/levels/[level-name].md` to validate the completed level design doc.
- Run `$gs-dev-story` to implement level content once the design is approved.
- Run `$gs-qa-plan` to generate a QA test plan for this level.

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
