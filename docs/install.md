# Install Codex Game Studios 2.0.0

Requires Python 3.11+ and PyYAML 6.x. Review the release, install requirements.txt
in a local virtual environment, then invoke the distribution entry point with that
interpreter. The framework repository and consumer target must be separate directories.

```text
python -m venv .venv
<venv-python> -m pip install -r requirements.txt
<venv-python> tools/studio.py install --target <absolute-project-root> --dry-run
<venv-python> tools/studio.py install --target <absolute-project-root>
```

On Windows the venv interpreter is .venv/Scripts/python.exe; on POSIX it is
.venv/bin/python. No activation is needed. Installation creates only namespaced
skills/roles, .game-studio resources/runtime, an ownership ledger and one bounded
AGENTS.md block. An absent project.yaml receives a minimal engine-neutral seed.
The consumer runtime needs the same dependencies; use a consumer-owned environment
or an explicitly chosen existing interpreter. Installer never installs dependencies.

Existing project.yaml/local.yaml, Codex config/hooks, AGENTS.override.md, user skill
names, game source, assets, records and instruction text outside the managed block
are preserved. A root AGENTS.override.md takes precedence over AGENTS.md; the installer
reports it. Integrate the framework routing into that file deliberately if desired.
Nested overrides follow native precedence. No global settings or permissions change.

Release hashes detect incomplete/edited distribution payloads. They are integrity
metadata, not a signature proving publisher identity. Review/trust the downloaded
source before running any installer. Installation rejects links/reparse paths,
unsafe paths, source/target overlap and corrupt ownership state. All collisions are
preflighted; an exactly identical existing file can be adopted. Unowned differences
and edited managed files fail without overwriting. Dry run does not create the target.

Open Codex in the consumer and invoke $gs-start, $gs-help or a relevant skill. Native
discovery may refresh automatically; restart if the host hasn't refreshed. Check
docs/migration/platform-evidence.md for the tested host and unassessed boundaries.

Optional hooks: generate and review definitions; register only through normal native
configuration/trust mechanisms. Do not bypass trust or replace an existing hooks file.
See docs/integration.md for context and command adapters.
