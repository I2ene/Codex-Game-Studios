# Contributing to Codex Game Studios

Contribute framework fixes, professional workflow improvements and documentation.
Keep consumer games and private records in separate repositories. Preserve MIT,
Donchitos attribution, domain contracts and mode-dependent gates. Original Claude
sources remain audited history; native changes belong in .agents, .codex/agents and
.game-studio. Do not regenerate reviewed content blindly.

Skills use .agents/skills/gs-name/SKILL.md with name/description metadata and complete
referenced procedures. Roles use .codex/agents/gs-name.toml with name, description and
developer_instructions. Omit model, effort and permission pins. Preserve the current
user's authorization; do not add per-file prompts for actions already in scope.
Delegation is optional, useful and authorized; record actual participants/results.

Use Python 3.11+ and requirements.txt in a local environment. Run targeted tests for
changed behavior and tools/validate.py for native content. Rebuild integrity hashes
after payload edits with tools/build_release.py; installation rejects altered releases.

```text
python tools/validate.py
python tools/build_release.py
python -m unittest discover -s tests -v
python tools/integration_sample.py
```

Optionally run tools/integration_sample.py --native-discovery with Codex CLI present
for actual installed discovery without model calls/trust changes. Native hook delivery
and custom-role launch need separate evidence. Format checks/fixture packaging do not
prove game balance, performance, engine builds or certification.

PRs describe the concrete problem, final behavior, actual validation and limitations.
Update migration coverage and affected indexes. Prefer Conventional Commits. Keep
global settings, hook trust, consumer files and main merging outside automatic effects.
