# Code and test root resolution

Resolve facts through native `config`/`observations`. Shared `engine.code_root`
and `engine.test_root` take priority over compatible shared top-level `code_root`
and `test_root`. Local overrides cannot change these team facts. Unset, null and
placeholders continue to engine defaults; an invalid explicit path never does.

The shared `.game-studio/resources/engines/engines.tsv` supplies Godot src/tests,
Unity Assets/Assets/Tests, Unreal Source/module Private/Tests and Web src/tests.
Unreal module ambiguity remains unresolved until supported by actual project data.
Preserve custom engines/layouts and explicit argv adapters. No engine is installed
or selected from example reference files.

Reject absolute/escaping paths, wrong case, nonexistent configured folders and
framework-only directories. Report NOT ASSESSED with the reason for unknown or
invalid roots, never a clean zero-file scan. A flat root `.` excludes `.agents`,
`.codex`, `.game-studio`, `.git`, production/design/docs/tests, tools, prototypes,
node_modules, vendor and generated build/dist trees from game code scans.

When scope remains ambiguous, show candidates and evidence. A whole-project
retrofit from a confirmed code root can produce a minimal game brief; a contained
subsystem produces a system brief. File counts are routing clues, not stage proof.
