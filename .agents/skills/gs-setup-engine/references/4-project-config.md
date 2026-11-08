# Engine setup — Phase 4: Record project facts

## 4. Record engine and language facts

Record engine.name, engine.version and engine.language in project.yaml, preserving
existing settings. Godot language choices: GDScript, C# or Both; read the language
configuration reference when applicable. Unreal choices: C++ primary with Blueprint
prototyping, or Blueprint primary with C++ where needed. Unity uses C#.
Use the actual consumer's requirements and installed toolchain, not template defaults.
Do not write AGENTS.md technology-stack/import blocks or modify packaged role files.
