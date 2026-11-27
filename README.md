# Codex Game Studios

A Codex native game production framework for new and existing game repositories.
Version **2.2.0** provides **78 repository skills**, **49 expertise roles**, and
professional procedures, contracts, templates and phase gates across the game lifecycle.
A Codex adaptation of Donchitos' MIT-licensed [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios);
based on upstream **1.3.0**. See [source attribution](NOTICE.md), [license](LICENSE),
and the [upstream compatibility map](docs/upstream-compatibility.md).

| Area | What it provides |
|---|---|
| First playable | Genre-informed brief, browser build/check, import, iteration, tuning, sharing, Grow and selected cuts |
| Design | Concepts and pillars, system GDDs, UX, art, audio, narrative, economy and balance |
| Development | Engine selection, architecture and ADRs, traceability, epics, stories, implementation and review |
| Quality | Readiness gates, QA, test evidence, accessibility, security, playtests and performance investigation |
| Delivery | Sprints, milestones, release and launch checklists, localization, hotfixes and live operations |
| Runtime | Ownership based installation, configuration, context recovery, artifact observations and review receipts |

## Install and start

Use a Codex host with repository skill support, Python **3.11+** and **PyYAML 6.x**.
Git is needed to clone and contribute. The optional upstream data helpers use Bash
and awk; Windows users can use Git for Windows Bash. A game engine and its build/test tools belong
to your game project; the framework does not install them.

Clone this repository separately from your game, then use a local Python environment:

```text
git clone https://github.com/I2ene/Codex-Game-Studios.git
cd Codex-Game-Studios
python -m venv .venv
<venv-python> -m pip install -r requirements.txt
<venv-python> tools/studio.py install --target <absolute-game-project-root> --dry-run
<venv-python> tools/studio.py install --target <absolute-game-project-root>
```

`<venv-python>` is `.venv/Scripts/python.exe` on Windows or `.venv/bin/python` on
macOS/Linux. Open Codex in the installed game repository and invoke `$gs-start` for
a new project, `$gs-adopt` for an existing one, or `$gs-next-step` for the next step.
Skills can also match natural language requests. See [installation](docs/install.md)
for preservation, dependencies and host discovery details.

## Use the lifecycle

For a new idea, say “make me a game” or invoke `$gs-prototype`. One genre-informed
round of questions leads to a brief with your original words, first minute,
challenge, features, Keep/Avoid and explicit guesses. Accept Build it to make a
browser playable. Scripted observations and viewed screenshots support each brief
verdict; missing evidence is named, and your play remains the real experience test.

After playing, ask for changes, tune values or share delivery files. Choose Grow
for a Web project and one-feature-at-a-time development, with sampled replay,
build/rule/smoke checks and authorized recovery points. `$gs-cut` proposes cuts
from the brief and built facts; you choose each cut. Import preserves the original
source. An existing engine keeps its engine and paper prototype routes. See the
[prototype entry](.agents/skills/gs-prototype/SKILL.md).

Browser creation/checks use Bash/awk and Chrome, Edge or Chromium. Web Grow needs
Node.js and downloads project dependencies when authorized. Missing browser access
or nonrepeatable replay remains NOT ASSESSED. Installation itself runs no game
commands and installs no game dependencies.

The professional design/development ladder is studio mode. The seven phases run from Concept through Release. Minimal, standard and full rigor
select the applicable artifacts and gates; all professional workflows remain available.
The minimal route uses a brief and ordered stories. Standard/full projects connect
GDDs to architecture, ADRs, traceable stories, implementation, review and test evidence.
See the [workflow guide](docs/workflow.md), [skill catalog](.game-studio/resources/docs/skills-reference.md)
and [role roster](.game-studio/resources/docs/agent-roster.md).

Configure `project.yaml`, project tool commands and optional context as described in
[project integration](docs/integration.md). Roles supply expertise; delegation uses
actual host tools and existing user authorization. Record real participants and
review results. Missing evidence remains **NOT ASSESSED**.

## Maintain and contribute

Installation preserves project configuration, instructions outside its managed block,
engine files, records and user skills. Upgrades check ownership and reject edited
managed files. It changes no global Codex configuration, model, permissions or hook trust.
Read [upgrading](UPGRADING.md), [contributing](CONTRIBUTING.md),
[security](SECURITY.md) and the [changelog](CHANGELOG.md).

Framework source lives in `.agents/skills`, `.codex/agents` and `.game-studio`.
[`docs/`](docs/README.md) describes usage and maintenance; `tools/`, `tests/` and
`fixtures/` contain release tooling and reproducible framework checks.

Format checks, executed helper fixtures and game quality evidence are different.
The test suite exercises framework behavior in temporary projects; it does not
establish game balance, visual quality, performance, engine builds or certification.
Trusted hook delivery, custom role launch and exhaustive inference evaluation of
all skills/roles need separate host evidence. Read the [validation boundaries](docs/validation.md).

Web, Godot, Unity and Unreal share one engine table; setup records the actual
project pin and reference data. Nested engine code/test roots take priority over
compatible legacy keys. The old `$gs-help`, `$gs-settings` and `$gs-changelog`
entries remain aliases for `$gs-next-step`, `$gs-project-settings` and
`$gs-write-changelog`.

Upstream reports a three-idea brief comparison and one six-story Grow example in
its [1.3.0 release](https://github.com/Donchitos/Claude-Code-Game-Studios/releases/tag/v1.3.0).
These are attributed upstream observations, not Codex validation. Spec Kit is
optional maintainer tooling and is excluded from consumer installation.
