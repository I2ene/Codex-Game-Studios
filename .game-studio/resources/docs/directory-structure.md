# Consumer project layout

Framework files: .agents/skills/gs-*, .codex/agents/gs-*, .game-studio/runtime and
.game-studio/resources. AGENTS.md contains one bounded framework block alongside
user instructions. .codex/config.toml and hook registration remain user-managed.

Professional defaults: design/gdd (concept, pillars, system docs), design/art,
design/narrative, design/balance, design/ux and design/registry; docs/architecture
(master architecture, ADRs, control manifest, TR registry); production/epics,
production/sprints, production/milestones, production/releases and optional
production/session-state. Templates live in .game-studio/resources/docs/templates.
These directories are created when applicable workflows produce artifacts, not
pre-filled with fake project decisions. Adapt paths to an existing project's layout.

Code/test roots: see code-root-resolution.md. Assets belong to the consumer's engine
layout. Engine reference examples are packaged under .game-studio/resources/engine-reference;
record current project engine verification separately, preserving packaged references
for safe upgrades. Project metadata lives in project.yaml; local whitelisted settings
and optional recovery interface are personal data and should be ignored by project Git.
