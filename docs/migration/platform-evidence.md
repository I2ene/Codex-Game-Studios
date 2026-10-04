# Platform reference sources

Historical primary-source references used for this adaptation. Recheck the applicable
current official documentation before changing a native interface:

| Capability | Primary source | Verified boundary |
|---|---|---|
| Repository skills | https://learn.chatgpt.com/docs/build-skills | .agents/skills; SKILL.md name/description; explicit/implicit selection |
| Project instructions | https://learn.chatgpt.com/docs/agent-configuration/agents-md | AGENTS.override.md precedes AGENTS.md; nested guidance; no @ import mechanism used |
| Native roles | https://learn.chatgpt.com/docs/agent-configuration/subagents | standalone .codex/agents TOML; name, description, developer_instructions; omitted settings inherit |
| Command hooks | https://learn.chatgpt.com/docs/hooks | native events, JSON stdin/stdout, cwd execution, commandWindows, exact-definition trust |
| Claude conversion | https://developers.openai.com/plugins/guides/submit-claude-plugin | convert commands/procedures; remove Claude-only settings; command hooks need runtime/trust |

Verify the current CLI, Python and PyYAML versions in the environment under review.
`tools/probe_codex.py --root <installed-consumer>` performs read-only discovery when
the CLI is available; `tools/integration_sample.py --native-discovery` runs that probe
inside a temporary consumer. Their output is an observation from that run, not an
installed capability grant. Custom-role loading/launch and trusted hook callback
delivery need separate actual host evidence; direct handler fixtures do not establish them.

The platform is evolving. Recheck source pages and capability evidence when changing
native interfaces. Upstream engine version examples and historical execution notes
are professional reference material, not fresh engine evidence for this release.
