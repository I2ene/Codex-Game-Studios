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
> Usage: `$gs-team-audio [feature or area to design audio for] [--review full|lean|solo]` — specify the feature or area to design audio for (e.g., `combat`, `main menu`, `forest biome`, `boss encounter`). Do not use `ask the user` here; output the guidance directly.

When this skill is invoked with an argument, orchestrate the audio team through a structured pipeline.

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
- **`individual`** (default): `sound-designer` only. Other agents consulted via the sound-designer, not spawned separately.
- **`small`**: + `audio-director` + `technical-artist` + `gameplay-programmer`.
- **`studio`**: + `accessibility-specialist` + the primary engine specialist (the full pipeline as documented).
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

1. **Read the argument** for the target feature or area (e.g., `combat`,
   `main menu`, `forest biome`, `boss encounter`).

2. **Gather context**:
   - Read relevant design docs in `design/gdd/` for the feature
   - Read the sound bible at `design/audio/sound-bible.md` if it exists. If only
     `design/gdd/sound-bible.md` exists (where earlier versions put it), read that
     and recommend moving it to `design/audio/` — in `design/gdd/` the GDD checks
     count every file as a system GDD. If neither exists,
     say so in one line — "No sound bible at `design/audio/sound-bible.md`; audio
     direction starts from the GDDs alone" — so the gap is visible in the output.
     Carry the gap forward: say so in the audio-director's Step 1 brief, and
     recommend creating a sound bible in Next Steps.
   - Read existing audio asset lists in `assets/audio/`
   - Read any existing sound design docs for this area

## How to Delegate

Apply the following professional responsibilities in the parent; delegate useful independent tasks only when authorized and available:
- `expertise role: audio-director` — Sonic identity, emotional tone, audio palette
- `expertise role: sound-designer` — SFX specifications, audio events, mixing groups
- `expertise role: accessibility-specialist` — Visual fallbacks and subtitles for critical audio, auditory sensitivity
- `expertise role: technical-artist` — Audio middleware, bus structure, memory budgets
- `expertise role: [primary engine specialist]` — Validate audio integration patterns for the engine
- `expertise role: gameplay-programmer` — Audio manager, gameplay triggers, adaptive music

**Brief each agent — do not dump context.** Read the shared inputs **once** and pass a distilled brief inline: the lines each agent actually needs, never a file path for a document you have already read (an agent handed a path re-reads the whole file). Pass a path only for a document you have not read and only that agent needs.

**End every agent prompt with a return contract:** "Write your full output to `[path]` — that named path is the requested return contract; write only within existing human authorization. Return **only** (1) the path written, (2) a ≤5-bullet summary of decisions, (3) any BLOCKED/CONCERNS items, one line each. Do not restate the documents you read." Without it, an agent returns everything it read back into this session. **Implementation work:** first state the files that will be created or changed. Existing human authorization covers in-scope changes; resolve any missing material decision once for the set before writing. A role or path supplies no permission.

**Substitute a real path for `[path]`.** Working artifacts go under
`production/audio/[feature]/`, where `[feature]` is the argument as a slug —
lowercase, spaces → hyphens (`boss encounter` → `boss-encounter`), the same slug
the "Save to" step uses. One file per agent, so parallel steps never share one:

| Step / agent | Writes to |
|---|---|
| 1 audio-director | `production/audio/[feature]/direction.md` |
| 2 sound-designer | `production/audio/[feature]/sfx-spec.md` |
| 2 accessibility-specialist | `production/audio/[feature]/accessibility.md` |
| 3 technical-artist | `production/audio/[feature]/integration-plan.md` |
| 3 engine specialist | `production/audio/[feature]/engine-notes.md` |
| 4 gameplay-programmer | the code root and the engine's test root — the files in the implementation set (File Write Protocol), subject to existing human authorization |

These are working drafts; the durable record is the audio design document you
compile from them.

> **Authorization:** use existing human task authorization for routine in-scope work; ask only for missing decisions or material actions outside that scope. A destination path does not supply authorization.

3. **Orchestrate the audio team** in sequence:

### Step 1: Audio Direction (audio-director)
Apply the `audio-director` expertise in the parent, or delegate to an authorized participant to:
- Define the sonic identity for this feature/area
- Specify the emotional tone and audio palette
- Set music direction (adaptive layers, stems, transitions)
- Define audio priorities and mix targets
- Establish any adaptive audio rules (combat intensity, exploration, tension)

### Step 2: Sound Design and Audio Accessibility (parallel)
Apply the `sound-designer` expertise in the parent, or delegate to an authorized participant to:
- Create detailed SFX specifications for every audio event
- Define sound categories (ambient, UI, gameplay, music, dialogue)
- Specify per-sound parameters (volume range, pitch variation, attenuation)
- Plan audio event list with trigger conditions
- Define mixing groups and ducking rules

Apply the `accessibility-specialist` expertise in the parent, or delegate to an authorized participant in parallel to:
- Identify which audio events carry critical gameplay information (damage received, enemy nearby, objective complete) and require visual alternatives for hearing-impaired players
- Specify subtitle requirements: which audio events need captions, what text format, on-screen duration
- Check that no gameplay state is communicated by audio alone (all must have a visual fallback)
- Review the audio event list for any that could cause issues for players with auditory sensitivities (high-frequency alerts, sudden loud events)
- Output: audio accessibility requirements list integrated into the audio event spec

A gameplay-critical audio event with no visual cue or subtitle is labelled
**BLOCKING** in the report, not advisory. Step 3 does not start until the user
resolves it or explicitly accepts it at the Step 2 decision point, which offers
the fix (a visual cue, subtitle or haptic fallback) and a stop; an accepted gap
is listed among the open questions in the summary.

### Step 3: Technical Implementation (parallel)
Apply the `technical-artist` expertise in the parent, or delegate to an authorized participant to:
- Design the audio middleware integration (Wwise/FMOD/native)
- Define audio bus structure and routing
- Specify memory budgets for audio assets per platform
- Plan streaming vs preloaded asset strategy
- Design any audio-reactive visual effects

Apply the **primary engine specialist** expertise in the parent, or delegate when authorized and supported by host tools and capacity (`<engine>-specialist` derived from `engine.name` — Godot→`godot-specialist`, Unity→`unity-specialist`, Unreal→`unreal-specialist`; fall back to the Primary line of `## Engine Specialists` in `docs/project-reference/technical-preferences.md`) to validate the integration approach:
- Is the proposed audio middleware integration idiomatic for the engine? (e.g., Godot's built-in AudioStreamPlayer vs FMOD, Unity's Audio Mixer vs Wwise, Unreal's MetaSounds vs FMOD)
- Any engine-specific audio node/component patterns that should be used?
- Known audio system changes in the pinned engine version that affect the integration plan?
- Output: engine audio integration notes to merge with the technical-artist's plan

If no engine is configured, skip the specialist spawn. **Record ``Engine validation: NOT ASSESSED — no engine configured (`engine.name` unset in `project.yaml`)`` in this run's output.** A skipped check that says nothing is indistinguishable from a check that passed; the reader cannot tell engine guidance was never sought.

### Step 4: Code Integration (gameplay-programmer)
Apply the `gameplay-programmer` expertise in the parent, or delegate to an authorized participant to:
- Implement audio manager system or review existing
- Wire up audio events to gameplay triggers
- Implement adaptive music system (if specified)
- Set up audio occlusion/reverb zones
- Write unit tests for audio event triggers

4. **Compile the audio design document** combining all team outputs.

5. **Save to** `design/audio/audio-[feature].md`. The parent compiles the
   completed step outputs. Use existing human authorization for the write; if a
   material decision is still missing, resolve it before writing. Working artifacts
   retain their named `production/audio/[feature]/` destinations. Create
   `design/audio/` when needed for the authorized document.

6. **Output a summary** with: audio event count, estimated asset count,
   implementation tasks, and any open questions between team members.

Verdict: **COMPLETE** — audio design document produced and team pipeline finished.

If the engine validation was skipped (no engine configured), the verdict says
so — never a plain COMPLETE:

Verdict: **COMPLETE — engine validation NOT ASSESSED ([reason])** — audio design document produced; the engine specialist never reviewed the integration plan.

If the pipeline stops because a dependency is unresolved (e.g., critical accessibility gap or missing GDD not resolved by the user):

Verdict: **BLOCKED** — [reason]

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

The parent compiles `design/audio/audio-[feature].md` from the completed step outputs.

## Next Steps

- Review the audio design doc with the audio-director before implementation begins.
- Use `$gs-dev-story` to implement the audio manager and event system once the design is approved.
- Run `$gs-asset-audit` after audio assets are created to verify naming and format compliance.
- If there was no sound bible, create one before the next audio pass: ask the
  `audio-director` agent to draft `design/audio/sound-bible.md` from
  `.game-studio/resources/docs/templates/sound-bible.md`, starting from this run's Step 1
  direction (it asks before writing under `design/`).

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
