# Codex compatibility contract

This is the runtime adapter for the preserved Claude-Code-Game-Studios design workflows. Read the project's AGENTS.md and existing context entry first. The human's instructions and established project agreements take priority over upstream conventions.

## Resolve sources and context

Read codex/context.json if it exists. Its optional framework_source_root is relative to the project root, defaulting to the project root itself. Resolve original .claude/docs, .claude/skills and .claude/agents paths against that source root. They are reference material, not executable Codex configuration.

An optional project_context_file identifies the consuming project's integration contract; an optional context_entry identifies its existing workbench or handoff navigation. Read those when configured. Otherwise use the project's actual navigation and current design artifacts. Do not assume a particular language, workspace path, PRD layout, genre, engine or installed product-design skill.

## Standalone entry and existing projects

No external requirements-design skill is required. Native start, help, onboard and adopt cover entry, navigation, recovery and design adoption. A previously created workbench is useful persisted context, not a mandatory runtime dependency.

When existing context already answers a source onboarding question, reuse that answer even if an engine is not configured. Do not rerun the new-user questionnaire merely because the upstream returning-user heuristic expects engine metadata. Audit only the requested design scope; engine selection and developer adoption remain handoffs.

Read professional artifacts from the consuming project, not from the source/template snapshot. File presence is not proof of completion: examine draft status and actual rule content before claiming readiness. Preserved templates, empty registries and mock artifacts never satisfy production gates.

## Preserve the studio design framework

Keep upstream phases, design categories, specialist responsibilities, templates, dependencies and meaningful readiness checks. Concepts, pillars, loops, the systems index, GDDs, narrative, art, UX, balance and reviews use the original design/ structure unless the consuming project explicitly maps an equivalent location.

Use one authoritative owner for each game rule. A workbench can index professional artifacts and maintain discussion, progress and decisions; it should not duplicate their complete rules. The entity registry is a cross-document index with source pointers, populated only from real approved facts. Do not invent registry entries or game content to fill templates.

## Interpret original instructions in Codex

Original frontmatter, model labels, allowed-tools lists, inline shell injections and Claude call examples are not Codex instructions. Read the selected source body as a design procedure and apply these replacements:

| Original feature | Codex behavior |
| --- | --- |
| Read, Glob, Grep, Write, Edit | Use actually available file tools; rg for searches when available |
| AskUserQuestion | Use the available question tool or conversation; ask for missing design decisions, not repeated authorization for ordinary work already requested |
| Agent and named specialists | Use actual delegation tools and optional ccgs-* role profiles only when delegation is authorized; otherwise perform explicitly labelled single-session review |
| Task*, log_decision, session-state | Use the project's existing task/progress/decision records; distinguish assistant choices from human-approved rules |
| CLAUDE.md and @file imports | Read AGENTS.md and explicitly load only the relevant mapped reference files |
| /design-command | Use $ccgs-design-command; commands absent from the native manifest are unsupported handoffs, not working Codex skills |
| yaml-helper and dynamic configuration | Read current project.yaml and existing project.local.yaml, then apply the preserved config-resolution and workflow-modes semantics |
| review receipts, structure-check scripts | Inspect actual content, file references and hashes with available tools; state whether the check was manual or scripted |

Do not execute original inline commands, hooks or scripts as part of this adapter. No Claude permission rules, status line, persistent-memory configuration, model routing, or global Codex settings are imported. Do not claim equivalent automation just because a reference file was preserved.

## Configuration and review depth

Resolve the current explicit invocation overrides, project-local/project configuration, per-system overrides and rigor expansion according to the preserved config-resolution.md and workflow-modes.md. Do not pin derived knobs or create unrequested local configuration. For an unconfigured project the source defaults to minimal/solo; standard derives standard/lean, and full derives full/full. Read only the relevant shared sections, not the entire effects-map.

At standard, a system GDD needs overview, detailed rules, edge cases, dependencies and acceptance criteria; formulas are required whenever numeric rules are defined. Full uses all eight source sections. A concept draft can contain explicit unknowns and is reviewed for its stage, not falsely certified as ready for implementation.

Design review, formula checks, technical feasibility and playtest evidence are separate claims. Missing documents/data/results mean NOT ASSESSED for the affected scope. A zero-match scan over absent data does not establish health. List actual inputs, findings, gaps, participants and limits.

## Delegation and boundaries

Retain specialist roles without starting every role or promising 49 simultaneous agents. Honor current permissions, concurrency limits and tool schemas. Named roles are optional profiles; if the current dispatcher cannot load a profile directly, an authorized child can read that profile and source role explicitly. Do not change global settings to force this.

For coordination skills, apply only the assigned design phases. Implementation, asset production, profiling, builds and release steps remain handoffs until a corresponding Codex development adapter exists and the task authorizes them. Do not spawn nested reviewers or write another participant's files without an explicit responsibility assignment.

Prototype plans are plans until run. playtest-report can produce a report structure or analyze actual notes; it cannot fabricate observations. quick-design can use the project's design-change record when development stories are maintained elsewhere. content-audit and technical change propagation require real implementation/ADR inputs to assess those portions.

Persist professional design outputs and update the existing context handoff after substantive progress. Saving a candidate is not human approval. Ordinary updates do not imply commit, push, publication, asset uploads, NAS operations or deletion.

## Provenance and scope

codex/manifest.json lists the native design skills, optional role profiles and preserved source hashes. Original LICENSE remains applicable. This release adapts the design layer; original developer skills, hooks, engine setup and build/release workflows are not advertised as Codex-ready.
