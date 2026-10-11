# Contributing to Codex Game Studios

Contribute framework fixes, professional workflow improvements and documentation.
Keep consumer games and private records in separate repositories. Preserve
[MIT and source attribution](NOTICE.md), lifecycle coverage, domain contracts and
mode-dependent gates. Native content is authoritative; do not regenerate reviewed
files from historical host sources.

## Development setup

Use Python 3.11+ and a local environment with `requirements.txt`:

```text
python -m venv .venv
<venv-python> -m pip install -r requirements.txt
```

The interpreter is `.venv/Scripts/python.exe` on Windows or `.venv/bin/python` on
macOS/Linux. Work on a branch. Preserve user files and run targeted regression tests
for behavior changes. Use small non-private fixtures for installer/command failures.

## Content contracts

Skills live in `.agents/skills/gs-name/SKILL.md` with name/description metadata and
complete referenced procedures. Roles live in `.codex/agents/gs-name.toml` with name,
description and `developer_instructions`. Omit model, effort and permission pins.
Preserve actual human authorization, mode applicability, missing-evidence verdicts,
professional quality standards and real participant reporting.

Update affected skill/role indexes and the evaluation catalog with content changes.
Use [evaluation guidance](.game-studio/resources/testing/README.md) and reusable
[templates](.game-studio/resources/testing/templates/). Professional scenarios are
not a substitute for actual task execution. New native API claims need current
primary documentation and host evidence; distinguish unavailable capabilities.

## Validation and packaging

After reviewed payload edits, rebuild hashes, then run release checks:

```text
python tools/build_release.py
python tools/validate.py
python -m unittest discover -s tests -v
python tools/integration_sample.py
```

Use the chosen environment's Python for every command. The manifest must describe
all installed files and match `.game-studio/VERSION`. Update version/changelog for a
release. Test upgrade preservation and conflicts when changing managed content or
installation behavior. CI runs the same checks across three operating systems.
The sample prints results; it does not write evidence into the repository.

Optionally use `tools/integration_sample.py --native-discovery` with Codex CLI for
read-only installed discovery. Game builds, role launch and trusted hook delivery
need separate evidence. See [validation boundaries](docs/validation.md).

PRs explain the concrete problem, final behavior, compatibility, actual validation
and limitations. Use the PR description and review conversation for task plans,
review rounds and handoffs; keep lasting usage/maintenance knowledge in formal docs.
Do not include private paths, chat IDs or consumer adaptation histories. Prefer
Conventional Commits. No global settings, hook trust or automatic main merging.
