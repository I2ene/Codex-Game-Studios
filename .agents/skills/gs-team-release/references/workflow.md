## Native checkpoint interface

Read .game-studio/resources/docs/context-management.md. Explicitly run recover
--root <project-root> and use checkpoint.path as <resolved-checkpoint>. If DISABLED,
skip checkpoint reads/writes; do not create a fixed fallback. Otherwise write the
current concise authored state to a temporary repository-local Markdown file and
run checkpoint --save <authored-file> --root <project-root>. Preserve useful fields
from the prior snapshot, reconcile current facts and replace stale state; the helper
keeps a hash-named backup. Do not append unbounded history or infer unseen work.
Existing task authorization covers routine state writes; state never grants consent.

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

**Argument check:** If no version number is provided:
1. Read `<resolved-checkpoint>` and the most recent file in `production/milestones/` (if they exist) to infer the target version.
2. If a version is found: report "No version argument provided — inferred [version] from milestone data. Proceeding." Then confirm with `ask the user`: "Releasing [version]. Is this correct?"
3. If no version is discoverable: use `ask the user` to ask "What version number should be released? (e.g., v1.0.0)" and wait for user input before proceeding. Do NOT default to a hardcoded version string.

When this skill is invoked, orchestrate the release team through a structured pipeline.

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

**Stage check — before professional work begins.** This skill ships a release, and
`$gs-gate-check release` is the readiness gate that must pass first; only its PASS
sets `project.stage` to `Release`. If the resolved `project.stage` is anything
else — `Polish`, an earlier stage, or not set — stop before Phase 1 and spawn
nothing:

> "The release readiness gate has not passed (project.stage: [stage]) — run
> `$gs-gate-check release` first."

Then ask with `ask the user`, in every `automation` mode — an override is never
taken on the user's behalf: `[A] Stop — I'll run $gs-gate-check release (recommended)`
/ `[B] Proceed anyway — override the stage check`. On `[A]`, end the run: Verdict
**BLOCKED** — release gate not passed. On `[B]`, ask (plain text) why, then record
the override as `Stage override: project.stage was [stage] — release gate not
passed; the user chose to proceed: [reason]` in the Phase 1 brief, in the go/no-go
record (`go-no-go-[version].md`) and in the final report. An override never
changes the stage itself.

`review_mode` sets director-gate depth, and this pipeline has no director gate:
no phase below spawns CD-, TD-, PR- or AD-PHASE-GATE, at any `review_mode`. Its
phase gates are the pipeline's own decision points (defined under `team.size`
below), and the agents that work at them are team members, not director gates.

`automation` drives the Decision Points note above. See the Decision Points note above and
`.game-studio/resources/docs/automation-modes.md` for how each mode changes pipeline behavior.

**`team.size`**: which professional responsibilities are in scope (orthogonal to review_mode gate-depth and workflow docs).
- **`individual`** (default): `release-manager` only. Other agents consulted via the release-manager, not spawned separately.
- **`small`**: + `producer` + `devops-engineer` + `qa-lead` + `community-manager`.
- **`studio`**: + `security-engineer` + `analytics-engineer` + `localization-lead` + `performance-analyst`, and `network-programmer` when the game is multiplayer (the full pipeline as documented).
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

## Team Composition
- **release-manager** — Release tag, versioning, changelog, patch notes, deployment
- **qa-lead** — Test sign-off, regression suite, release quality gate
- **devops-engineer** — Build pipeline, artifacts, deployment automation
- **security-engineer** — Pre-release security audit (invoke if game has online/multiplayer features or player data)
- **network-programmer** — Netcode stability sign-off (invoke if game has multiplayer)
- **analytics-engineer** — Verify telemetry events fire correctly and dashboards are live
- **localization-lead** — Verify every shipped string is translated
- **performance-analyst** — Benchmark the release build against its performance targets
- **community-manager** — Launch announcement and player-facing messaging, written from the patch notes
- **producer** — Go/no-go decision, stakeholder communication, scheduling

## How to Delegate

Apply the following professional responsibilities in the parent; delegate useful independent tasks only when authorized and available:
- `expertise role: release-manager` — Release tag, versioning, changelog, patch notes, deployment
- `expertise role: qa-lead` — Test sign-off, regression suite, release quality gate
- `expertise role: devops-engineer` — Build pipeline, artifacts, deployment automation
- `expertise role: security-engineer` — Security audit for online/multiplayer/data features
- `expertise role: analytics-engineer` — Telemetry event verification and dashboard readiness
- `expertise role: community-manager` — Launch communication, written from the patch notes
- `expertise role: producer` — Go/no-go decision, stakeholder communication
- `expertise role: network-programmer` — Netcode stability sign-off (invoke if game has multiplayer)
- `expertise role: localization-lead` — Translation completeness sign-off (Phase 4)
- `expertise role: performance-analyst` — Performance benchmarks against targets (Phase 4)

**Brief each agent — do not dump context.** Read the shared inputs **once** and pass a distilled brief inline: the lines each agent actually needs, never a file path for a document you have already read (an agent handed a path re-reads the whole file). Pass a path only for a document you have not read and only that agent needs.

**End every agent prompt with a return contract:** "Write your full output to `[path]` — that named path is the requested return contract; write only within existing human authorization. Return **only** (1) the path written, (2) a ≤5-bullet summary of decisions, (3) any BLOCKED/CONCERNS items, one line each. Do not restate the documents you read." Without it, an agent returns everything it read back into this session.

**Substitute a real path for `[path]`.** One file per agent under
`production/releases/`, except the two whose homes are fixed elsewhere. An active
agent standing in for one outside the active set writes that agent's file:

| Phase / agent | Writes to | Destination fixed by |
|---|---|---|
| 1 producer | `production/releases/release-plan-[version].md` | this skill |
| 2 release-manager | `production/releases/release-checklist-[version].md` | `$gs-release-checklist` |
| 3 qa-lead | `production/releases/qa-gate-[version].md` | this skill |
| 3 devops-engineer | `production/releases/build-[version].md` | this skill |
| 3 security-engineer | `production/releases/security-signoff-[version].md` | this skill |
| 3 network-programmer | `production/releases/netcode-signoff-[version].md` | this skill |
| 4 localization-lead | `production/releases/localization-signoff-[version].md` | this skill |
| 4 performance-analyst | `production/releases/performance-signoff-[version].md` | this skill |
| 4 analytics-engineer | `production/releases/analytics-signoff-[version].md` | this skill |
| 5 go/no-go | `production/releases/go-no-go-[version].md` | this skill |
| 6 release-manager | `docs/patch-notes/[version].md` | `$gs-patch-notes` |
| 6 community-manager | `production/releases/announcement-[version].md` | this skill |
| 7 release-manager | `production/releases/release-report-[version].md` | this skill |

> **Every one of those thirteen outputs needs a stated destination.**
> `production/releases/` is where `$gs-release-checklist` already writes, and
> `docs/patch-notes/[version].md` is where `$gs-patch-notes` already writes, so the
> release record lands in one place regardless of which skill produced it.
>
> **A separate file per agent, not one appended record.** Phase 3 and Phase 4
> spawn agents in parallel; two agents appending to one file race, and the loser's
> section vanishes silently.

> **Authorization:** use existing human task authorization for routine in-scope work; ask only for missing decisions or material actions outside that scope. A destination path does not supply authorization.

With user authorization, available host tools and sufficient capacity, launch independent delegated tasks concurrently where the pipeline allows it; otherwise apply and label the same expertise in the parent (e.g., Phase 3 agents can run simultaneously).

## Pipeline

### Phase 1: Release Planning
Delegate to **producer**:
- Confirm all milestone acceptance criteria are met
- Identify any scope items deferred from this release
- Set the target release date and communicate to team
- Output: release authorization with scope confirmation

### Phase 2: Release Candidate
Delegate to **release-manager**:
- Bump version numbers in all relevant files on `main`; the commit carrying the bump is the release candidate. Development is trunk-based — a release is a tag on `main` (applied in Phase 6), not a branch
- Confirm the release checklist from Polish (`$gs-release-checklist`, run before `$gs-gate-check release`) is complete for this candidate; run it now only if none exists
- Cut a `release/[version]` branch from the candidate only if this release needs stabilising (a freeze, platform certification) — bug fixes only there, and every fix lands on `main` as well
- Output: release candidate commit (plus the `release/*` branch, if one was cut) and checklist

### Phase 3: Quality Gate (parallel)
Apply the following independent expertise in the parent, or delegate concurrently with user authorization, available host tools and sufficient capacity:
- **qa-lead**: Execute full regression test suite. Test all critical paths. Verify no open bugs at the severities `$gs-gate-check release` blocks for this `workflow`: S1 at every tier, S2 and S3 too at `full`. Sign off on quality.
- **devops-engineer**: Build release artifacts for all target platforms. Verify builds are clean and reproducible. Run automated tests in CI.
- **security-engineer** *(if game has online features, multiplayer, or player data)*: Conduct pre-release security audit. Review authentication, anti-cheat, data privacy compliance. Sign off on security posture.
- **network-programmer** *(if game has multiplayer)*: Sign off on netcode stability. Verify lag compensation, reconnect handling, and bandwidth usage under load.

Resolve security and networking applicability from `platform.online` and `platform.multiplayer` in `project.yaml`, plus whether the game stores player data. A missing key is not false: resolve it with the user rather than assuming an offline game. Cover applicable responsibilities through the resolved professional scope, including parent work; a missing delegate is not a skipped assessment. Name an inapplicable check and its reasons, e.g. `security-engineer: not applicable — platform.online: false, platform.multiplayer: false, no player data`.

### Phase 4: Localization, Performance, and Analytics
Apply these responsibilities in the parent, or delegate when authorized with actual tools and capacity. Phase 3 and Phase 4 may run concurrently when independent; parent work may be sequential and delegated work may queue when capacity is limited. Checks with a real data dependency wait for the specific release build or finding they need, not every result from the other phase:
- Verify all strings are translated (delegate to **localization-lead** if available)
- Run performance benchmarks against targets (delegate to **performance-analyst** if available)
- **analytics-engineer**: Verify all telemetry events fire correctly on release build. Confirm dashboards are receiving data. Check that critical funnels (onboarding, progression, monetization if applicable) are instrumented.
- Output: localization, performance, and analytics assessments — one file per responsibility (table above), with parent work or actual participant identified

### Phase 5: Go/No-Go
At `review_mode: full`, complete the technical-director assessment in the parent or an authorized delegate with actual host tools. This is a director review, not a PHASE-GATE; lean and solo skip it explicitly because of review mode. Ask for GO, CONCERNS or NO-GO on the release candidate's technical state, or NOT ASSESSED naming the unavailable input. No delegate launch is required for parent work to count as performed.

Apply producer expertise in the parent, or delegate when authorized, once all applicable assessments are available:
- Collect qa-lead, release-manager and devops-engineer results.
- Collect security-engineer results when online features, multiplayer or player data make that responsibility applicable, regardless of who performed the work.
- Collect network-programmer results when multiplayer makes that responsibility applicable.
- Collect the technical-director assessment at full review mode; at lean/solo record the mode skip instead of inventing approval.
- Collect Phase 4 localization, performance and analytics results within the resolved scope before making the Phase 5 decision. Phase 3 and Phase 4 have no blanket ordering dependency.
- Record each applicable assessment's completion status, verdict, evidence and source: parent applying the role, or the actual participant. A missing assessment remains NOT ASSESSED and is never counted as approval; retain any known blocking finding. Parent work must not be presented as independent review or a human signature.
- Carry a stage-check override, if there was one, into the go/no-go record as its `Stage override:` line
- Evaluate any open issues — are they blocking or can they ship?
- Make the go/no-go call
- Output: release decision with rationale

**If producer declares NO-GO:**
- Surface the decision immediately: "PRODUCER: NO-GO — [rationale, e.g., S1 bug found in Phase 3]."
- Use `ask the user` with options:
  - Fix the blocker and re-run the affected phase
  - Defer the release to a later date
  - Override NO-GO with documented rationale (user must provide written justification)
- **Skip Phase 6 entirely** — do not tag, deploy to staging, deploy to production, or spawn community-manager.
- Produce a partial report summarizing Phases 1–5 and what was skipped (Phase 6) and why.
- Verdict: **BLOCKED** — release not deployed.

After the user selects "Override NO-GO with documented rationale":
- Ask (plain text, not widget): "Please describe the justification for overriding the NO-GO verdict. This will be embedded in the release record."
- Wait for the user's written justification.
- Embed the justification text in the partial approval record before Phase 6: append a "⚠️ Override Justification: [user's text]" field.
- Only then proceed to Phase 6.

### Phase 6: Deployment (if GO)

**This phase always requires explicit user approval regardless of
`modes.automation` — including `autonomous` mode.** Production deployment is
irreversible and high-stakes; it is NOT covered by the configurable
`automation_always_ask` categories, so this skill guards it unconditionally.
Before tagging or deploying, use `ask the user`:
- Prompt: "Producer verdict is GO. Execute Phase 6 — tag, deploy to staging,
  deploy to production?"
- Options: `[A] Yes, deploy` / `[B] Staging only — hold production` / `[C] Stop here`

Only after explicit approval, delegate to **release-manager** + **devops-engineer**:
- Tag the release in version control
- Finalize the changelog drafted in Polish (`$gs-changelog`), adding what changed since the gate
- Deploy to staging for final smoke test
- Deploy to production (only if the user approved production above)
- Human team action: Monitor dashboards and error rates for 48 hours post-release. Schedule a follow-up retrospective using `$gs-retrospective` at the 48-hour mark.

In parallel with deployment, delegate to **release-manager**:
- Finalize the patch notes drafted in Polish using `$gs-patch-notes [version]` — release-manager owns release-source analysis; use the host's actual authorized command tools for `git log`, then community-manager handles the announcement

Then hand those patch notes to **community-manager**:
- Prepare launch announcement (store page updates, social media, community post)
- Draft known issues post if any S3+ issues shipped
- Output: all player-facing release communication, ready to publish on deploy confirmation

### Phase 7: Post-Release
- **release-manager**: Generate release report (what shipped, what was deferred, metrics)
- **producer**: Update milestone tracking, communicate to stakeholders
- **qa-lead**: Monitor incoming bug reports for regressions
- **community-manager**: Publish all player-facing communication, monitor community sentiment
- **analytics-engineer**: Confirm live dashboards are healthy; alert if any critical events are missing
- Keep the 48-hour monitoring window from Phase 6: bugs, dashboards and community sentiment are watched for 48 hours after release (release-manager's own watch runs to its 72h report)
- Schedule post-release retrospective if issues occurred

## Error Recovery Protocol

**First, verify the artifact.** A required output path must exist before the
phase is complete, whether the author is the parent or a real delegate. If it is
missing, identify the unmet contract: complete authorized parent work or resume
the actual participant, and report any blocker. A fluent response alone is not
evidence of a completed phase.

If required parent work or an authorized delegate is BLOCKED, encounters an error, or cannot complete: **surface it
immediately, don't proceed past a dependency it blocks, and always produce a
partial report.** Full procedure: `.game-studio/resources/docs/error-recovery-protocol.md`.

Common blockers:
- Input file missing (story not found, GDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; accept it with `$gs-architecture-decision accept ADR-NNNN` once decided
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

Tagging, publication and deployment require explicit user authorization for the actual action and target. Preserve the GO/NO-GO, staging-only and override gates.

## Output

A summary report covering: release version, scope, quality gate results, go/no-go decision, deployment status, and monitoring plan. For every applicable assessment include completion status, verdict, evidence, parent/actual participant source and unresolved blockers; name mode and applicability skips separately.

Verdict: **COMPLETE** — release executed and deployed.
Verdict: **BLOCKED** — release halted; the stage check stopped it, go/no-go was NO, or a hard blocker is unresolved.

## Next Steps

- Monitor post-release dashboards for 48 hours.
- Run `$gs-retrospective` if significant issues occurred during the release.
- `project.stage` reads `Release` unless the stage check was overridden: `$gs-gate-check release` is the Polish → Release readiness gate, run before this skill. After an override the stage still reads what it did. Only `$gs-gate-check` changes `project.stage` (on a PASS, or a CONCERNS whose risks the user accepted), so this skill never writes it or `production/stage.txt`. `Release` is the terminal stage in the `project.stage` enum — there is no post-launch stage value. Record live/post-launch status in the release report, not in `project.stage`.
