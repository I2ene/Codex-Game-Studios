# Platform evidence — 2026-10-05

Official pages fetched during the audit (the older developers URLs redirect to Learn):

| Capability | Primary source | Verified boundary |
|---|---|---|
| Repository skills | https://learn.chatgpt.com/docs/build-skills | .agents/skills; SKILL.md name/description; explicit/implicit selection |
| Project instructions | https://learn.chatgpt.com/docs/agent-configuration/agents-md | AGENTS.override.md precedes AGENTS.md; nested guidance; no @ import mechanism used |
| Native roles | https://learn.chatgpt.com/docs/agent-configuration/subagents | standalone .codex/agents TOML; name, description, developer_instructions; omitted settings inherit |
| Command hooks | https://learn.chatgpt.com/docs/hooks | native events, JSON stdin/stdout, cwd execution, commandWindows, exact-definition trust |
| Claude conversion | https://developers.openai.com/plugins/guides/submit-claude-plugin | convert commands/procedures; remove Claude-only settings; command hooks need runtime/trust |

Actual local runtime: Codex CLI 0.160.0; Python 3.12.14; PyYAML 6.0.3.
The CLI generated its own protocol schema. Read-only initialize, skills/list and
hooks/list calls succeeded. All 74 gs-* skills were discovered without framework
errors. No model inference, permission override, global configuration change or
hook-trust bypass was used. Role files passed TOML/required-field validation;
custom-role loading/launch is NOT ASSESSED. Hook handlers were invoked directly with
event fixtures; trusted runtime callback delivery is NOT ASSESSED.

The platform is evolving. Recheck source pages and capability evidence when changing
native interfaces. Upstream engine version examples and historical execution notes
are professional reference material, not fresh engine evidence for this release.
