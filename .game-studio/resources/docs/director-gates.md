# Native gate execution

Review modes select professional responsibilities. A role review may be performed
by the parent; label it accordingly. Independent sign-off requires a real authorized
participant. No gate causes mandatory delegation. User authorization and the native
permission system govern actions.

# Director Gates — Shared Review Pattern

Index of all director and lead review gates. Skills reference gate IDs from this
index instead of embedding prompts inline — eliminating drift when prompts need
updating. Each gate's full definition (Trigger, Context to pass, Prompt, Verdicts)
lives in its own file under `.game-studio/resources/docs/director-gates/`, named after the gate
ID in lowercase.

**Scope**: All 7 production stages (Concept → Release), all 3 Tier 1 directors,
all key Tier 2 leads. Any skill, team orchestrator, or workflow may invoke these gates.

The actual reviewer reads the gate definition and relevant context. When the parent
applies the role, read its definition here. When useful delegation is authorized and
available, pass the file path plus a bounded context brief and require the actual
participant to read it. Label parent work and independent work separately; a panel
definition never implies that multiple participants ran or independently signed off.

---

## Gate Index

Agent by prefix: `CD-` creative-director · `TD-` technical-director ·
`PR-` producer · `AD-` art-director · `LP-` lead-programmer · `QL-` qa-lead ·
`ND-` narrative-director. Definition files below are in
`.game-studio/resources/docs/director-gates/`; each header names the professional reviewer; all inherit session settings.

| Gate ID | Purpose | Definition file |
|---------|---------|-----------------|
| CD-PILLARS | Pillar stress test after pillars are defined | cd-pillars.md |
| CD-GDD-ALIGN | GDD pillar alignment after a system GDD is authored | cd-gdd-align.md |
| CD-SYSTEMS | Systems decomposition vision check after `$gs-map-systems` | cd-systems.md |
| CD-NARRATIVE | Narrative consistency of story/lore documents | cd-narrative.md |
| CD-PLAYTEST | Player experience validation of playtest reports | cd-playtest.md |
| CD-PHASE-GATE | Creative readiness at phase transition | cd-phase-gate.md |
| TD-SYSTEM-BOUNDARY | System boundary review before GDD authoring | td-system-boundary.md |
| TD-FEASIBILITY | Technical feasibility of early concept risks | td-feasibility.md |
| TD-ARCHITECTURE | Master architecture document sign-off | td-architecture.md |
| TD-ADR | Individual ADR review before Accepted | td-adr.md |
| TD-ENGINE-RISK | Engine version risk for post-cutoff APIs | td-engine-risk.md |
| TD-PHASE-GATE | Technical readiness at phase transition | td-phase-gate.md |
| TD-MANIFEST | Control manifest review before it is written | td-manifest.md |
| TD-CHANGE-IMPACT | Design-change impact assessment review | td-change-impact.md |
| PR-SCOPE | Scope and timeline validation | pr-scope.md |
| PR-SPRINT | Sprint plan feasibility review | pr-sprint.md |
| PR-MILESTONE | Milestone risk assessment | pr-milestone.md |
| PR-EPIC | Epic structure feasibility before story breakdown | pr-epic.md |
| PR-PHASE-GATE | Production readiness at phase transition | pr-phase-gate.md |
| AD-CONCEPT-VISUAL | Visual identity anchor after pillars lock | ad-concept-visual.md |
| AD-ART-BIBLE | Art bible sign-off before asset production | ad-art-bible.md |
| AD-PHASE-GATE | Visual readiness at phase transition | ad-phase-gate.md |
| LP-FEASIBILITY | Implementation feasibility of the architecture | lp-feasibility.md |
| LP-CODE-REVIEW | Code review of an implemented story | lp-code-review.md |
| QL-STORY-READY | Acceptance-criteria testability before sprint | ql-story-ready.md |
| QL-TEST-COVERAGE | Test coverage review for one story before it closes (`$gs-story-done`) | ql-test-coverage.md |
| ND-CONSISTENCY | Narrative consistency of writer deliverables | nd-consistency.md |
| AD-VISUAL | Visual consistency of art/tech-art decisions | ad-visual.md |

---

## Review Modes

Review intensity controls whether gates run.

**Global config**: `modes.review_mode` in `project.yaml` — one word: `full`,
`lean`, or `solo`. Legacy fallback: `production/review-mode.txt` (single line,
same values); `project.yaml` wins when both are present. `$gs-start` never writes
it: left unset, it follows `modes.rigor` (`minimal` → `solo`, `standard` →
`lean`, `full` → `full`). Set it explicitly only with
`$gs-settings modes.review_mode=<value>`.

**Per-run override**: any gate-using skill accepts `--review [full|lean|solo]`,
overriding the global config for that run only.

| Mode | What runs |
|------|-----------|
| `full` | All gates active — every workflow step reviewed |
| `lean` | PHASE-GATEs only (`$gs-gate-check`) — per-skill gates skipped. The `rigor: standard` value |
| `solo` | No director gates anywhere (game jams, prototypes, max speed). **Default** — the `rigor: minimal` value |

**One exception:** `$gs-team-narrative` runs ND-CONSISTENCY in every review mode
whenever narrative-director is on the team — it is that pipeline's only
narrative consistency check, not an optional review.

---

## Invocation Pattern (copy into any skill)

**MANDATORY: apply the review mode before every gate spawn.**

Run the explicit native config command and retain modes.review_mode.
Use config-resolution.md for precedence and provenance.

An inline `--review [mode]` argument, if the skill accepts one, overrides the
resolved value for that run.

Apply the resolved mode:
- `solo` → **skip all gates**. Note: `[GATE-ID] skipped — Solo mode`
- `lean` → **skip unless this is a PHASE-GATE** (CD-PHASE-GATE, TD-PHASE-GATE, PR-PHASE-GATE, AD-PHASE-GATE). Note: `[GATE-ID] skipped — Lean mode`
- `full` → spawn as normal

> **PHASE-GATE panel width is a second, independent axis.** `review_mode` decides
> whether the four PHASE-GATEs run at all; `modes.workflow` decides how many of
> them run — `minimal` → PR only, `standard` → TD + PR, `full` → all four. The
> rule and its rationale live in `$gs-gate-check` Section 4b, the only skill that
> spawns PHASE-GATEs. Every other gate in this index is single-director and
> unaffected. Width never softens a verdict: the escalation rule below applies
> unchanged to whoever ran.

```
# Apply mode check, then:
Spawn `[agent-name]` via native delegation when authorized:
- Gate: [GATE-ID] — delegation brief instructs the agent to read
  `.game-studio/resources/docs/director-gates/[gate-id].md` FIRST (the actual reviewer reads it; parent reads it when applying the role locally)
- Context: [fields under that gate's **Context to pass**]
- Await the verdict before proceeding.
```

For parallel spawning (multiple directors at one gate point): apply the mode
check per gate, then spawn all surviving agents simultaneously — issue all native delegation when authorized
calls before waiting for any result; collect all verdicts before proceeding.

---

## Standard Verdict Format

Every gate returns one of its three verdicts — or NOT ASSESSED when it could not
judge. Skills must handle all four. The three judgement words are each gate's
own — its definition file's **Verdicts** line is the authority — and the rows
below are their meanings (TD-FEASIBILITY's VIABLE / CONCERNS / HIGH RISK,
PR-MILESTONE's ON TRACK / AT RISK / OFF TRACK). NOT ASSESSED is the same word at
every gate, so no Verdicts line lists it:

| Verdict | Meaning | Default action |
|---------|---------|----------------|
| **APPROVE / READY** | No issues. Proceed. | Continue the workflow |
| **CONCERNS [list]** | Issues present but not blocking. | Surface to user via `ask the user` — options: `Revise flagged items` / `Accept and proceed` / `Discuss further`. Revise flagged items: the specialist who drafted the section re-drafts it; the revision goes through the skill's normal approve-then-write step, and the header records `REVISED [date]`. |
| **REJECT / NOT READY [blockers]** | Blocking issues. Do not proceed. | Surface blockers to user. Do not write files or advance stage until resolved. |
| **NOT ASSESSED [what was missing]** | An input the gate names was missing or unreadable, so no judgement was made. | Name what was missing. Never treat it as APPROVE/READY: supply the input and re-run the gate, or record NOT ASSESSED and let the skill's own verdict reflect it. |

**Rank**: NOT ASSESSED sits below REJECT / NOT READY and CONCERNS, and above
APPROVE / READY — a known problem is more actionable than an unknown, and a gate
that could not look has approved nothing. A director that found a problem and
also lacked an input answers with the problem's word and names the missing
input in its rationale. An artifact the skill reports as absent is information,
not a missing input. At a phase gate,
a missing artifact the target phase requires is a finding (NOT READY or
CONCERNS); one `$gs-gate-check` passes as "not expected before [phase]" or "not
required at `workflow: [tier]`" is not a finding — a phase gate judges
readiness for the phase being entered, not a later one.

**Escalation rule**: When multiple directors are spawned in parallel, apply the
strictest verdict by that rank — one NOT READY overrides all READY verdicts, and
one NOT ASSESSED keeps the result from being READY.

---

## Recording Gate Outcomes

After a gate resolves, record the verdict in the relevant document's status header:

```markdown
> **[Director] Review ([GATE-ID])**: APPROVED [date] / CONCERNS (accepted) [date] / REVISED [date] / NOT ASSESSED [date] — [missing input]
```

For phase gates, record in `docs/architecture/architecture.md` or
`production/session-state/active.md` as appropriate.

---

## Parallel Gate Protocol

At checkpoints needing multiple directors (most common at `$gs-gate-check`):

```
Spawn in parallel (issue all native delegation when authorized calls before waiting for any result):
creative-director → CD-PHASE-GATE, technical-director → TD-PHASE-GATE,
producer → PR-PHASE-GATE, art-director → AD-PHASE-GATE

Collect every verdict from the directors that ran, then apply escalation rules:
- Any NOT READY / REJECT → overall verdict minimum FAIL
- Any CONCERNS → overall verdict minimum CONCERNS
- Any NOT ASSESSED (and no NOT READY / REJECT or CONCERNS) → overall verdict at best NOT ASSESSED
- All READY / APPROVE → eligible for PASS (still subject to artifact checks)
```

---

## Adding New Gates

1. Assign a gate ID: `[DIRECTOR-PREFIX]-[DESCRIPTIVE-SLUG]`. Prefixes: `CD-`
   `TD-` `PR-` `LP-` `QL-` `ND-` `AD-`; add new ones for new agents
   (`audio-director` → `AU-`, `ux-designer` → `UX-`)
2. Create `.game-studio/resources/docs/director-gates/[gate-id].md` (lowercase), starting with
   the standard "> Gate definition..." header note, with all five fields:
   Trigger, Context to pass, Prompt, Verdicts, special handling notes
3. Add its row to the Gate Index table above
4. Reference it in skills by ID only — never copy the prompt text into the skill

---

## Gate Coverage by Stage

| Stage | Required Gates | Optional Gates |
|-------|---------------|----------------|
| **Concept** | CD-PILLARS, AD-CONCEPT-VISUAL | TD-FEASIBILITY, PR-SCOPE |
| **Systems Design** | TD-SYSTEM-BOUNDARY, CD-SYSTEMS, PR-SCOPE, CD-GDD-ALIGN (per GDD) | ND-CONSISTENCY, AD-VISUAL, TD-CHANGE-IMPACT (on GDD revision) |
| **Technical Setup** | TD-ARCHITECTURE, TD-ADR (per ADR), TD-MANIFEST, LP-FEASIBILITY, AD-ART-BIBLE | TD-ENGINE-RISK |
| **Pre-Production** | PR-EPIC, QL-STORY-READY (per story), PR-SPRINT, the PHASE-GATE panel (via gate-check — PR at `minimal`, TD + PR at `standard`, all four at `full`) | CD-PLAYTEST |
| **Production** | LP-CODE-REVIEW (per story), QL-STORY-READY, PR-SPRINT (per sprint), QL-TEST-COVERAGE (per story, via `$gs-story-done`) | PR-MILESTONE, AD-VISUAL, TD-CHANGE-IMPACT (on GDD revision) |
| **Polish** | CD-PLAYTEST, PR-MILESTONE | AD-VISUAL |
| **Release** | The PHASE-GATE panel (via gate-check — PR at `minimal`, TD + PR at `standard`, all four at `full`) | — |
