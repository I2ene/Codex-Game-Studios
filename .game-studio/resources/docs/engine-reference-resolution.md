# Engine reference authority

Run `python .game-studio/runtime/studio.py engine-reference --root <project-root>`
whenever engine facts, APIs, architecture or technical gates matter. Resolve the
actual name/version from project.yaml and confirmed toolchain. engine.reference_root
is the exact project-owned engine folder; default docs/engine-reference/<engine-lowercase>.
engine.project_root optionally locates engine project files inside the repository.
It locates marker files for inspection; it never changes the runner's working
directory or inserts command arguments. run executes from the consumer root.
Ordinary relative script arguments resolve there. Godot res:// and export presets
resolve from the actual command's explicit --path, or the consumer root if omitted.

Read project.documents for VERSION.md, breaking/deprecated APIs, modules and practices.
The placeholder <project-engine-reference> in procedures means this resolved folder,
not a literal path or the package. Missing documents/version/probe evidence stay
unknown/NOT ASSESSED; verify current official versioned docs and actual toolchain
before qualified API claims. Project records are data and require evidence, not an
automatic assertion that the installed engine was checked.

background.documents under .game-studio/resources/engine-reference are historical,
version-marked examples for optional domain context. They never fill missing project
version/verification facts and must not be edited during project setup. Installer
ships those examples; project-owned records are created/refreshed only when relevant
and authorized, not prefilled on install. setup-engine records/refines only that
project folder and engine.reference_root; ADRs, roles, rules and gates use the same
resolver. Refresh project records from current official sources with actual date,
name/version, sources, confirmed facts and unavailable probe evidence.

coherence produces named MATCH/DIFFERS/NOT ASSESSED/OBSERVED comparisons for pin,
recorded installed version, project version/rendering/physics, script entries and
export presets. No binary runs by default. Inspect commands.engine_probe argv and
invoke coherence --probe only within authorization; it records actual exit/output.
No configured engine/probe is absence of evidence, not confirmed absence or agreement.
