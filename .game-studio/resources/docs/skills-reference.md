# Installed skill catalog

| Skill | Scope |
|---|---|
| $gs-adopt | Brownfield audit — do existing artifacts actually work? Numbered migration plan. Unlike $gs-project-stage-detect, checks compliance not existence. |
| $gs-architecture-decision | Create an ADR documenting a technical decision: context, alternatives considered, consequences. |
| $gs-architecture-review | Traceability matrix mapping GDD requirements to ADRs. Finds gaps, cross-ADR conflicts, engine compatibility. PASS/CONCERNS/NOT ASSESSED/FAIL. |
| $gs-art-bible | Author the Art Bible — visual identity gating asset production. Run before $gs-map-systems. |
| $gs-asset-audit | Audit assets against naming conventions, file size budgets, format standards. Finds orphaned assets, missing references. |
| $gs-asset-spec | Per-asset visual specs plus AI generation prompts from GDDs and character profiles. After the art bible. |
| $gs-balance-check | Find balance outliers, broken progressions, degenerate strategies, economy imbalances in formulas and data. 'Check game balance'. |
| $gs-brainstorm | Guided concept ideation using professional studio techniques, player psychology, creative exploration. |
| $gs-bug-report | Structured bug report from a description, or analyze code for potential bugs. Reproduction steps, severity. |
| $gs-bug-triage | Re-evaluate open bugs — priority vs severity, assign to sprints, surface systemic trends. Run when the count grows. |
| $gs-changelog | Auto-generate a changelog from git commits and sprint data. Internal and player-facing versions. |
| $gs-code-review | Architectural code review — coding standards, SOLID, testability, performance concerns. |
| $gs-consistency-check | Scan GDDs against the entity registry for cross-document conflicts. Grep-first approach targets conflicting sections, different stats. |
| $gs-content-audit | Audit GDD content counts against what's implemented — planned vs built. |
| $gs-create-architecture | Author the architecture blueprint before code is written. Validates decisions against the pinned engine, flags knowledge gaps. |
| $gs-create-control-manifest | Flat must-do/never-do rules sheet per system and layer, extracted from Accepted ADRs. ADRs explain why; this is actionable. |
| $gs-create-epics | Turn GDDs plus architecture into epics — one per architectural module, with untraced requirements. Then $gs-create-stories [epic-slug]. |
| $gs-create-stories | Break one epic into implementable stories embedding TR-ID, ADR guidance, acceptance criteria. Reads the control manifest. After $gs-create-epics. |
| $gs-day-one-patch | Day-one launch patch — focused fix for known issues found after gold master. Mini-sprint with QA gate and rollback. |
| $gs-design-review | Reviews one design document for completeness, internal consistency, implementability, and design standards. Before handing to programmers. |
| $gs-design-system | Section-by-section GDD authoring for one system — walks through each required section, cross-references dependencies. |
| $gs-dev-story | Implement a story: ADR guidelines, right programmer agent, code plus test. Then $gs-story-done ($gs-story-readiness before, $gs-code-review after, at standard/full). |
| $gs-estimate | Estimate task effort from complexity, dependencies, velocity, risk. Structured estimate with confidence levels. |
| $gs-gate-check | Ready to advance between development phases? PASS/CONCERNS/NOT ASSESSED/FAIL with blockers and required artifacts. 'Can we move to production?' |
| $gs-help | What should I do next? Use when stuck or you don't know what to do. |
| $gs-hotfix | Emergency fix bypassing normal sprint process — hotfix branch, approvals tracked, backport verified, full audit trail. |
| $gs-launch-checklist | Launch readiness across every department: code, content, store, marketing, community, infrastructure, legal, go/no-go sign-offs. |
| $gs-localize | Localization pipeline — find hardcoded strings, extract string tables, cultural review, VO, RTL, enforce string freeze. |
| $gs-map-systems | Decompose a concept into individual systems, map dependencies, prioritize design order, create the systems index. |
| $gs-milestone-review | Milestone progress review — completeness, quality metrics, risk, go/no-go recommendation. At checkpoints or before a deadline. |
| $gs-onboard | Onboarding doc for a new contributor or agent — project state, conventions, priorities relevant to the specified role. |
| $gs-patch-notes | Player-facing patch notes from git history and changelogs. Translates developer language into player communication. |
| $gs-perf-profile | Performance profiling — find bottlenecks, measure against budgets, produce ranked optimization recommendations. |
| $gs-playtest-report | Structured playtest report template, or turn existing playtest notes into structured feedback. |
| $gs-project-stage-detect | Analyze project state, detect stage, identify gaps, recommend next steps. 'Where are we in development?' |
| $gs-propagate-design-change | A GDD changed — scan ADRs and the traceability index for now-stale architectural decisions. Impact report, guides resolution. |
| $gs-prototype | Concept prototype before GDDs — throwaway HTML, Engine or Paper build, PROCEED/PIVOT/KILL/NOT ASSESSED. After $gs-brainstorm and $gs-setup-engine. |
| $gs-qa-plan | QA test plan for a sprint — classifies stories by Logic/Integration/Visual/UI, covers automated tests, manual cases, smoke scope. |
| $gs-quick-design | Lightweight spec for small changes — tuning adjustments, minor mechanics. Embeds directly into stories; skips full GDD. |
| $gs-regression-suite | Map test coverage to GDD critical paths, find fixed bugs lacking regression tests, flag drift from new features. |
| $gs-release-checklist | Pre-release checklist — build verification, certification requirements, store metadata, launch readiness. |
| $gs-retrospective | Sprint or milestone retrospective from completed work, velocity, blockers. Actionable insights for the next iteration. |
| $gs-reverse-document | Generate missing design or architecture docs from existing implementation — works backwards from code and prototypes. |
| $gs-review-all-gdds | Holistic cross-GDD review — contradictions between systems, dominant strategies, economic imbalance, cognitive overload, pillar drift. |
| $gs-scope-check | Scope creep check — current scope versus the original plan. Flags additions, quantifies bloat, recommends cuts. 'Any scope creep?' |
| $gs-security-audit | Security audit — save tampering, cheat vectors, network exploits, data exposure, input validation. Before public or multiplayer release. |
| $gs-settings | View or change project config — effective merged values, or set locally in project.local.yaml. |
| $gs-setup-engine | Configure engine and version. Pins it in AGENTS.md; WebSearch fills reference docs when the version is beyond LLM training data. |
| $gs-skill-improve | Improve a skill via a test-fix-retest loop — static checks, targeted fixes, keep or revert on score change. |
| $gs-skill-test | Validate skill files for structural compliance and behavioral correctness. Four modes: static linter, spec, category rubric, audit. |
| $gs-smoke-check | Critical-path smoke gate before QA hand-off — runs the automated suite. A failed check means the build is not QA-ready. |
| $gs-soak-test | Soak test protocol for extended play — what to observe and log for slow leaks, fatigue, late-appearing edge cases. |
| $gs-sprint-plan | New or updated sprint plan from the current milestone, completed work, and available capacity. |
| $gs-sprint-status | Fast, concise sprint snapshot — burndown and emerging risks for situational awareness. 'How is the sprint going?' |
| $gs-start | First-time onboarding — asks where you are, then guides you to the right workflow. |
| $gs-story-done | End-of-story completion review — verifies each acceptance criterion, checks GDD/ADR deviations, prompts code review, updates status. |
| $gs-story-readiness | Is a story implementation-ready? Checks clear acceptance criteria, open questions, ADR refs. READY/NEEDS WORK/BLOCKED/NOT ASSESSED. |
| $gs-team-audio | Orchestrate the audio team — audio-director, sound-designer, technical-artist, gameplay-programmer — direction through implementation. |
| $gs-team-combat | Orchestrate the combat team — game-designer, gameplay-programmer, ai-programmer, technical-artist, sound-designer, qa-tester — design through implement and validate. |
| $gs-team-level | Orchestrate the level team — level-designer, narrative-director, world-builder, art-director, systems-designer, qa-tester — for complete area creation. |
| $gs-team-live-ops | Orchestrate the live-ops team — live-ops-designer, economy-designer, analytics-engineer, community-manager, writer — for a season or live event. |
| $gs-team-narrative | Orchestrate the narrative team — narrative-director, writer, world-builder, level-designer — for story, world lore, narrative-driven levels. |
| $gs-team-polish | Orchestrate the polish team — performance-analyst, technical-artist, sound-designer, qa-tester — to optimize and harden a feature or area. |
| $gs-team-qa | Orchestrate the QA team through a full testing cycle — qa-lead strategy and test plan, qa-tester case writing, execution, sign-off. |
| $gs-team-release | Orchestrate the release team — release-manager, qa-lead, devops-engineer, producer — to execute a release from candidate to deployment. |
| $gs-team-ui | Orchestrate the UI team through the UX pipeline — authoring, visual design, implementation, review, polish. Uses $gs-ux-design, $gs-ux-review, studio templates. |
| $gs-tech-debt | Track, categorize and prioritize technical debt across the codebase — scans for debt indicators, maintains a register. |
| $gs-test-evidence-review | Quality review of test files and evidence — goes beyond existence, evaluates assertion coverage. ADEQUATE/INCOMPLETE/MISSING/NOT ASSESSED per story. |
| $gs-test-flakiness | Find flaky tests from CI logs — aggregates pass rates, spots intermittent failures, recommends quarantine. After multiple runs. |
| $gs-test-helpers | Generate engine-specific test helper libraries — assertion utilities, factory functions, mocks in the engine's test folder. Reduces boilerplate. |
| $gs-test-setup | Scaffold the test framework and CI — tests/ directory, engine test runner, GitHub Actions workflow. Once, before the first sprint. |
| $gs-ux-design | Section-by-section UX spec authoring for a screen, flow or HUD. Reads the player journey to provide context; also project-wide accessibility. |
| $gs-ux-review | Validate a UX spec, HUD design or pattern library — accessibility, GDD alignment, readiness. APPROVED / NOT ASSESSED / NEEDS REVISION / MAJOR REVISION NEEDED. |
| $gs-vertical-slice | Pre-production validation — end-to-end build to confirm the full loop is achievable before committing to Production. After GDDs, architecture, UX specs. |
