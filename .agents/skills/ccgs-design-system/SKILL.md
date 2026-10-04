---
name: ccgs-design-system
description: Use when authoring or revising detailed rules and a GDD for one game system.
license: MIT; upstream MIT license preserved in the configured source root.
---

# CCGS design-system for Codex

Preserve the original specialist workflow; adapt runtime and context through the compatibility contract.

1. Restore the project's AGENTS.md, existing context navigation, current state and decisions.
2. Read [Codex compatibility](../../../codex/compatibility.md), optional codex/context.json and its configured project_context_file. Resolve the source root and current project configuration.
3. Read .claude/skills/design-system/SKILL.md under that source root. Use its professional design phases and relevant templates, while replacing provider-specific frontmatter, inline commands, paths and calls as specified in the compatibility contract. Load only the references needed for this task.
4. Keep the upstream artifact structure and readiness checks for the current phase. State missing inputs and unsupported developer portions explicitly; preserve candidates, confirmed decisions and unverified assumptions as different states.
5. Write design artifacts to the project's professional design area and update its existing context handoff. Report actual checks and participants. Do not import source scripts, hooks, global settings or automatic Git operations.

Original /design-system corresponds to $ccgs-design-system. Other native design entries are listed in [the design adapter guide](../../../codex/README.md). Unsupported development commands remain handoff items.
