# Code and test root resolution

Use explicit project code_root/test_root when configured. Otherwise use the chosen
engine layout: Godot src/ and tests/; Unity Assets/ and Assets/Tests/; Unreal Source/
and the project module's Private/Tests/ (ask for the module if ambiguous). An engine
neutral/custom layout is permitted when the project supplies paths and command adapters.
An unresolved root is unknown, never evidence that the project has no code/tests.
Paths must stay in the project. Do not install or choose an engine from reference files.
