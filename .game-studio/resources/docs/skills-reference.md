# Native skill catalog

78 discoverable entries provide 75 canonical workflows and three compatibility
aliases. Invoke `$gs-<name>` in Codex or describe the task. Roles supply expertise;
actual tool availability and user authorization govern delegation.

The default new-game route is prototype → play/change → Grow → feature sittings →
selected cuts. Studio mode retains the complete seven-phase professional lifecycle.
Use next-step to route existing work, project-settings for effective configuration
and write-changelog for version history.

| Entry | Purpose |
| --- | --- |
| [`$gs-adopt`](../../../.agents/skills/gs-adopt/SKILL.md) | Brownfield audit — do existing artifacts actually work? Numbered migration plan. Unlike $gs-project-stage-detect, checks compliance not existence. |
| [`$gs-architecture-decision`](../../../.agents/skills/gs-architecture-decision/SKILL.md) | Create an ADR documenting a technical decision: context, alternatives considered, consequences. |
| [`$gs-architecture-review`](../../../.agents/skills/gs-architecture-review/SKILL.md) | Traceability matrix mapping GDD requirements to ADRs. Finds gaps, cross-ADR conflicts, engine compatibility. PASS/CONCERNS/NOT ASSESSED/FAIL. |
| [`$gs-art-bible`](../../../.agents/skills/gs-art-bible/SKILL.md) | Author the Art Bible — visual identity gating asset production. Run before $gs-map-systems. |
| [`$gs-asset-audit`](../../../.agents/skills/gs-asset-audit/SKILL.md) | Audit assets against naming conventions, file size budgets, format standards. Finds orphaned assets, missing references. |
| [`$gs-asset-spec`](../../../.agents/skills/gs-asset-spec/SKILL.md) | Per-asset visual specs plus AI generation prompts from GDDs and character profiles. After the art bible. |
| [`$gs-balance-check`](../../../.agents/skills/gs-balance-check/SKILL.md) | Find balance outliers, broken progressions, degenerate strategies, economy imbalances in formulas and data. 'Check game balance'. |
| [`$gs-brainstorm`](../../../.agents/skills/gs-brainstorm/SKILL.md) | Guided concept ideation using professional studio techniques, player psychology, creative exploration. |
| [`$gs-bug-report`](../../../.agents/skills/gs-bug-report/SKILL.md) | Structured bug report from a description, or analyze code for potential bugs. Reproduction steps, severity. |
| [`$gs-bug-triage`](../../../.agents/skills/gs-bug-triage/SKILL.md) | Re-evaluate open bugs — priority vs severity, assign to sprints, surface systemic trends. Run when the count grows. |
| [`$gs-changelog`](../../../.agents/skills/gs-changelog/SKILL.md) | Compatibility alias. Use when the user invokes $gs-changelog; forwards the original request to $gs-write-changelog. |
| [`$gs-code-review`](../../../.agents/skills/gs-code-review/SKILL.md) | Architectural review of written code: coding standards, SOLID, testability, performance. |
| [`$gs-consistency-check`](../../../.agents/skills/gs-consistency-check/SKILL.md) | Scan GDDs against the entity registry for cross-document conflicts. Grep-first approach targets conflicting sections, different stats. |
| [`$gs-content-audit`](../../../.agents/skills/gs-content-audit/SKILL.md) | Audit GDD content counts against what's implemented — planned vs built. |
| [`$gs-create-architecture`](../../../.agents/skills/gs-create-architecture/SKILL.md) | Author the architecture blueprint before code is written. Validates decisions against the pinned engine, flags knowledge gaps. |
| [`$gs-create-control-manifest`](../../../.agents/skills/gs-create-control-manifest/SKILL.md) | Flat must-do/never-do rules sheet per system and layer, extracted from Accepted ADRs. ADRs explain why; this is actionable. |
| [`$gs-create-epics`](../../../.agents/skills/gs-create-epics/SKILL.md) | Turn GDDs plus architecture into epics — one per architectural module, with untraced requirements. Then $gs-create-stories [epic-slug]. |
| [`$gs-create-stories`](../../../.agents/skills/gs-create-stories/SKILL.md) | Break one epic into implementable stories embedding TR-ID, ADR guidance, acceptance criteria. Reads the control manifest. After $gs-create-epics. |
| [`$gs-cut`](../../../.agents/skills/gs-cut/SKILL.md) | Use when asked what to cut, how to finish or ship a game from its brief, or for a polish list. |
| [`$gs-day-one-patch`](../../../.agents/skills/gs-day-one-patch/SKILL.md) | Day-one launch patch — focused fix for known issues found after gold master. Mini-sprint with QA gate and rollback. |
| [`$gs-design-review`](../../../.agents/skills/gs-design-review/SKILL.md) | Reviews one design document for completeness, internal consistency, implementability, and design standards. Before handing to programmers. |
| [`$gs-design-system`](../../../.agents/skills/gs-design-system/SKILL.md) | Section-by-section GDD authoring for one system — walks through each required section, cross-references dependencies. |
| [`$gs-dev-story`](../../../.agents/skills/gs-dev-story/SKILL.md) | Implement a story: ADR guidelines, right programmer agent, code plus test. Then $gs-story-done ($gs-story-readiness before, $gs-code-review after, at standard/full). |
| [`$gs-estimate`](../../../.agents/skills/gs-estimate/SKILL.md) | Estimate task effort from complexity, dependencies, velocity, risk. Structured estimate with confidence levels. |
| [`$gs-gate-check`](../../../.agents/skills/gs-gate-check/SKILL.md) | Ready to advance between development stages? PASS/CONCERNS/NOT ASSESSED/FAIL with blockers and required artifacts. 'Can we move to production?' |
| [`$gs-help`](../../../.agents/skills/gs-help/SKILL.md) | Compatibility alias. Use when the user invokes $gs-help; forwards the original request to $gs-next-step. |
| [`$gs-hotfix`](../../../.agents/skills/gs-hotfix/SKILL.md) | Emergency fix bypassing normal sprint process — hotfix branch, approvals tracked, backport verified, full audit trail. |
| [`$gs-launch-checklist`](../../../.agents/skills/gs-launch-checklist/SKILL.md) | Launch readiness across every department: code, content, store, marketing, community, infrastructure, legal, go/no-go sign-offs. |
| [`$gs-localize`](../../../.agents/skills/gs-localize/SKILL.md) | Localization pipeline — find hardcoded strings, extract string tables, cultural review, VO, RTL, enforce string freeze. |
| [`$gs-map-systems`](../../../.agents/skills/gs-map-systems/SKILL.md) | Decompose a concept into individual systems, map dependencies, prioritize design order, create the systems index. |
| [`$gs-milestone-review`](../../../.agents/skills/gs-milestone-review/SKILL.md) | Milestone progress review — completeness, quality metrics, risk, go/no-go recommendation. At checkpoints or before a deadline. |
| [`$gs-next-step`](../../../.agents/skills/gs-next-step/SKILL.md) | Use when asked what to do next in a game project, or when the user is stuck. |
| [`$gs-onboard`](../../../.agents/skills/gs-onboard/SKILL.md) | Onboarding doc for a new contributor or agent — project state, conventions, priorities relevant to the specified role. |
| [`$gs-patch-notes`](../../../.agents/skills/gs-patch-notes/SKILL.md) | Player-facing patch notes from git history and changelogs. Translates developer language into player communication. |
| [`$gs-perf-profile`](../../../.agents/skills/gs-perf-profile/SKILL.md) | Performance profiling — find bottlenecks, measure against budgets, produce ranked optimization recommendations. |
| [`$gs-playtest-report`](../../../.agents/skills/gs-playtest-report/SKILL.md) | Structured playtest report template, or turn existing playtest notes into structured feedback. |
| [`$gs-project-settings`](../../../.agents/skills/gs-project-settings/SKILL.md) | Use when checking or changing effective project settings and their sources. |
| [`$gs-project-stage-detect`](../../../.agents/skills/gs-project-stage-detect/SKILL.md) | Analyze project state, detect stage, identify gaps, recommend next steps. 'Where are we in development?' |
| [`$gs-propagate-design-change`](../../../.agents/skills/gs-propagate-design-change/SKILL.md) | A GDD changed — scan ADRs and the traceability index for now-stale architectural decisions. Impact report, guides resolution. |
| [`$gs-prototype`](../../../.agents/skills/gs-prototype/SKILL.md) | Use to build, import, change or grow a playable browser one-shot, or test one design hypothesis with an engine, paper prototype or spike before production. |
| [`$gs-qa-plan`](../../../.agents/skills/gs-qa-plan/SKILL.md) | QA test plan for a sprint — classifies stories by Logic/Integration/Visual/UI, covers automated tests, manual cases, smoke scope. |
| [`$gs-quick-design`](../../../.agents/skills/gs-quick-design/SKILL.md) | Lightweight spec for small changes — tuning adjustments, minor mechanics. Embeds directly into stories; skips full GDD. |
| [`$gs-regression-suite`](../../../.agents/skills/gs-regression-suite/SKILL.md) | Map test coverage to GDD critical paths, find fixed bugs lacking regression tests, flag drift from new features. |
| [`$gs-release-checklist`](../../../.agents/skills/gs-release-checklist/SKILL.md) | Pre-release checklist — build verification, certification requirements, store metadata, launch readiness. |
| [`$gs-retrospective`](../../../.agents/skills/gs-retrospective/SKILL.md) | Sprint or milestone retrospective from completed work, velocity, blockers. Actionable insights for the next iteration. |
| [`$gs-reverse-document`](../../../.agents/skills/gs-reverse-document/SKILL.md) | Writes missing design or architecture docs, or a game's brief, from code. Use when code or prototypes have no docs. |
| [`$gs-review-all-gdds`](../../../.agents/skills/gs-review-all-gdds/SKILL.md) | Holistic cross-GDD review — contradictions between systems, dominant strategies, economic imbalance, cognitive overload, pillar drift. |
| [`$gs-scope-check`](../../../.agents/skills/gs-scope-check/SKILL.md) | Scope creep check — current scope versus the original plan. Flags additions, quantifies bloat, recommends cuts. 'Any scope creep?' Finishing a game from its brief is $gs-cut's. |
| [`$gs-security-audit`](../../../.agents/skills/gs-security-audit/SKILL.md) | Security audit — save tampering, cheat vectors, network exploits, data exposure, input validation. Before public or multiplayer release. |
| [`$gs-settings`](../../../.agents/skills/gs-settings/SKILL.md) | Compatibility alias. Use when the user invokes $gs-settings; forwards the original request to $gs-project-settings. |
| [`$gs-setup-engine`](../../../.agents/skills/gs-setup-engine/SKILL.md) | Sets up and pins the engine version: web for a new project unless Godot, Unity or Unreal is named. Use to choose or upgrade it. |
| [`$gs-skill-improve`](../../../.agents/skills/gs-skill-improve/SKILL.md) | Improve a skill via a test-fix-retest loop — static checks, targeted fixes, keep or revert on score change. |
| [`$gs-skill-test`](../../../.agents/skills/gs-skill-test/SKILL.md) | Validate skill files for structural compliance and behavioral correctness. Four modes: static linter, spec, category rubric, audit. |
| [`$gs-smoke-check`](../../../.agents/skills/gs-smoke-check/SKILL.md) | Critical-path smoke gate before QA hand-off — runs the automated suite. A failed check means the build is not QA-ready. |
| [`$gs-soak-test`](../../../.agents/skills/gs-soak-test/SKILL.md) | Soak test protocol for extended play — what to observe and log for slow leaks, fatigue, late-appearing edge cases. |
| [`$gs-sprint-plan`](../../../.agents/skills/gs-sprint-plan/SKILL.md) | New or updated sprint plan from the current milestone, completed work, and available capacity. |
| [`$gs-sprint-status`](../../../.agents/skills/gs-sprint-status/SKILL.md) | Fast, concise sprint snapshot — burndown and emerging risks for situational awareness. 'How is the sprint going?' |
| [`$gs-start`](../../../.agents/skills/gs-start/SKILL.md) | Guides a first-time user through onboarding and picks the right workflow. Use when the user is new, just cloned or installed the studio, has no idea or engine yet, asks where to begin, or wants to bring in an existing game. A request for a game itself ('make me a game where...') is $gs-prototype's. |
| [`$gs-story-done`](../../../.agents/skills/gs-story-done/SKILL.md) | End-of-story completion review — verifies each acceptance criterion, checks GDD/ADR deviations, prompts code review, updates status. |
| [`$gs-story-readiness`](../../../.agents/skills/gs-story-readiness/SKILL.md) | Is a story implementation-ready? Checks clear acceptance criteria, open questions, ADR refs. READY/NEEDS WORK/BLOCKED/NOT ASSESSED. |
| [`$gs-team-audio`](../../../.agents/skills/gs-team-audio/SKILL.md) | Orchestrate the audio team — audio-director, sound-designer, technical-artist, gameplay-programmer — direction through implementation. |
| [`$gs-team-combat`](../../../.agents/skills/gs-team-combat/SKILL.md) | Orchestrate the combat team — game-designer, gameplay-programmer, ai-programmer, technical-artist, sound-designer, qa-tester — design through implement and validate. |
| [`$gs-team-level`](../../../.agents/skills/gs-team-level/SKILL.md) | Orchestrate the level team — level-designer, narrative-director, world-builder, art-director, systems-designer, qa-tester — for complete area creation. |
| [`$gs-team-live-ops`](../../../.agents/skills/gs-team-live-ops/SKILL.md) | Orchestrate the live-ops team — live-ops-designer, economy-designer, analytics-engineer, community-manager, writer — for a season or live event. |
| [`$gs-team-narrative`](../../../.agents/skills/gs-team-narrative/SKILL.md) | Orchestrate the narrative team — narrative-director, writer, world-builder, level-designer — for story, world lore, narrative-driven levels. |
| [`$gs-team-polish`](../../../.agents/skills/gs-team-polish/SKILL.md) | Orchestrate the polish team — performance-analyst, technical-artist, sound-designer, qa-tester — to optimize and harden a feature or area. |
| [`$gs-team-qa`](../../../.agents/skills/gs-team-qa/SKILL.md) | Orchestrate the QA team through a full testing cycle — qa-lead strategy and test plan, qa-tester case writing, execution, sign-off. |
| [`$gs-team-release`](../../../.agents/skills/gs-team-release/SKILL.md) | Orchestrate the release team — release-manager, qa-lead, devops-engineer, producer — to execute a release from candidate to deployment. |
| [`$gs-team-ui`](../../../.agents/skills/gs-team-ui/SKILL.md) | Orchestrate the UI team through the UX pipeline — authoring, visual design, implementation, review, polish. Uses $gs-ux-design, $gs-ux-review, studio templates. |
| [`$gs-tech-debt`](../../../.agents/skills/gs-tech-debt/SKILL.md) | Track, categorize and prioritize technical debt across the codebase — scans for debt indicators, maintains a register. |
| [`$gs-test-evidence-review`](../../../.agents/skills/gs-test-evidence-review/SKILL.md) | Quality review of test files and evidence — goes beyond existence, evaluates assertion coverage. ADEQUATE/INCOMPLETE/MISSING/NOT ASSESSED per story. |
| [`$gs-test-flakiness`](../../../.agents/skills/gs-test-flakiness/SKILL.md) | Find flaky tests from CI logs — aggregates pass rates, spots intermittent failures, recommends quarantine. After multiple runs. |
| [`$gs-test-helpers`](../../../.agents/skills/gs-test-helpers/SKILL.md) | Generate engine-specific test helper libraries — assertion utilities, factory functions, mocks in the engine's test folder. Reduces boilerplate. |
| [`$gs-test-setup`](../../../.agents/skills/gs-test-setup/SKILL.md) | Sets up the test framework and CI: tests/ directory, engine runner, GitHub Actions workflow. Use once, before the first sprint. |
| [`$gs-ux-design`](../../../.agents/skills/gs-ux-design/SKILL.md) | Section-by-section UX spec authoring for a screen, flow or HUD. Reads the player journey to provide context; also project-wide accessibility. |
| [`$gs-ux-review`](../../../.agents/skills/gs-ux-review/SKILL.md) | Validate a UX spec, HUD design or pattern library — accessibility, GDD alignment, readiness. APPROVED / NOT ASSESSED / NEEDS REVISION / MAJOR REVISION NEEDED. |
| [`$gs-vertical-slice`](../../../.agents/skills/gs-vertical-slice/SKILL.md) | Pre-production validation — end-to-end build to confirm the full loop is achievable before committing to Production. After GDDs, architecture, UX specs. |
| [`$gs-write-changelog`](../../../.agents/skills/gs-write-changelog/SKILL.md) | Use when a release or sprint needs an internal or player-facing changelog. |

The old help/settings/changelog names print one rename notice and carry original
arguments to next-step/project-settings/write-changelog exactly once. Their shared
canonical evaluation guidance is not counted as duplicate model execution.
