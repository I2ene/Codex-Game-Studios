# Codex Game Studios · design adapter

This fork adds 26 native Codex design skills and 13 optional design role profiles while preserving the original studio workflows, templates and role sources. The design layer can be used directly; it does not depend on a separate requirements-design skill or a specific PRD workbench.

## Enter the workflow

- $ccgs-start: start or resume game design.
- $ccgs-help: read-only guidance on the next step.
- $ccgs-onboard and $ccgs-adopt: recover a design area or adopt existing design artifacts.
- $rpg-game-design: optional routing across the specialist design skills.
- $ccgs-brainstorm → $ccgs-map-systems → $ccgs-design-system → $ccgs-design-review: concept, systems, detailed rules, and review.

Other native entries retain whole-GDD review, consistency, balance, scope, content evidence, quick changes, change propagation, playtest reports, art direction, asset specifications, UX design/review, and narrative/level/combat/UI/audio design coordination. The full native inventory is [manifest.json](manifest.json).

Read [compatibility.md](compatibility.md) for runtime mappings, stage-sensitive checks and scope boundaries. The original source procedures remain under .claude/ and are read as references, not installed Claude tool configuration. No source hook or script is executed by the adapter.

## Use in another project

Use Python 3.11+ for the installer and validator. From a checkout of this fork:

```sh
python codex/install_design.py --target /path/to/game-project --dry-run
python codex/install_design.py --target /path/to/game-project
python codex/validate_design.py --root /path/to/game-project
```

The installer copies native skills/profiles, the adapter contract and a bounded snapshot of their source references. It leaves existing AGENTS.md, project configuration and game artifacts unchanged. It refuses to overwrite existing destinations; upgrades require a reviewed plan instead of silently replacing local work.

Existing context navigation is optional:

```sh
python codex/install_design.py --target /path/to/game-project --context-entry docs/project-context.md --project-context-file docs/studio-integration.md
```

Those files must already exist. Installation records repository-relative paths in codex/context.json. Configure an existing handoff protocol there, or use the studio workflows directly. The adapter does not create or require a generic PRD structure. The default snapshot directory is .ccgs-source; --source-dirname can place it elsewhere inside the target project.

Run native skills with their $ccgs-* names. Codex discovers repository skills from .agents/skills; optional role TOML files live under .codex/agents. Roles inherit current model and permissions. Current dispatcher capabilities and explicit delegation authorization determine how they can be used; the number of definitions is not a concurrency promise.

## Preserved artifacts and configuration

Use the original design/ layout for concepts, the systems index, GDDs, the entity registry, narrative, art, UX, balance and reviews. Keep existing context records as handoff documents instead of duplicating game rules. project.yaml and an existing project.local.yaml retain the source rigor/configuration semantics.

The installer does not seed game content, copy session memory, set an engine, import permissions, enable hooks or change global Codex configuration. Sample contexts and fixture results are not production game evidence.

## Validation and current limits

```sh
python codex/validate_design.py
python -m unittest discover -s codex -p "test_*.py"
```

The validator checks preserved source hashes, native skill frontmatter shape/references, role TOML and context paths. The official skill-creator validator can also be run against each native SKILL.md. These checks do not prove that every professional workflow or role has been exercised in a live game project.

Unit tests run in the framework checkout. Consumer installation copies the installer and validator, not the framework test suite. Text source receipts normalize LF/CRLF line endings for portability; content changes still fail validation.

This release covers design and design portions of entry/adoption/coordination. Developer implementations, engine setup, hooks, technical automation, profiling, builds and releases remain unadapted. content-audit and technical change propagation require supplied code/ADR evidence; absent inputs remain NOT ASSESSED. Review and playtest claims name actual evidence and participants.

Original source version: b21fa0f7f289fc3e726cf36fb12b9bc1e7a51e4d. The upstream MIT LICENSE in the configured source root is preserved; [manifest.json](manifest.json) identifies the reference snapshot. Framework migration work belongs in this fork; game rules and project-specific context belong in consuming projects.
