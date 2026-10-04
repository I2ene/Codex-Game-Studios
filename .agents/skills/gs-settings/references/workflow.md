# Inspect or edit framework settings

Run config with explicit --root to inspect effective values, provenance and notes.
For an authorized edit use `settings --root <project-root> [--local] dotted.key=value`;
--dry-run renders the proposed result without writing. YAML values may need shell
quoting. Local-only whitelist and enum validation are documented in config-resolution.md.
Serialize only after reviewing the intended change; comments are not retained by this
helper, so use a normal targeted file edit when preserving comments matters.

Keep rigor separate from explicit knob overrides. Explain which value will change,
its current source and affected workflow. Unknown specialist preferences belong in
project.yaml only when the project explicitly defines them. Do not write Codex model,
permission, global configuration, hooks or trust settings. Legacy mirrors are warnings,
not automatic reconciliation. Current user authorization governs any edit.
