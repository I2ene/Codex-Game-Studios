# Upstream engine command observations

These are historical examples from upstream 1.1.2, not execution evidence for
this release or a consumer. Verify current official engine documentation and
the actual pinned project. Convert reviewed commands to argv lists. Shell strings
are not accepted by the native runner.

**`commands` block** — engine-default shell commands, simple-string form:

| Engine | `build` | `test` | `run` | `smoke` |
|--------|---------|--------|-------|---------|
| Godot | `godot --headless --export-debug '<PRESET>'` **(ASK — do not default)** | `godot --headless -s -d --remote-debug tcp://127.0.0.1:0 res://addons/gdUnit4/bin/GdUnitCmdTool.gd -a res://tests --ignoreHeadlessMode` | `godot --path . --windowed --resolution 1280x720` | `godot --headless --quit-after 5` |
| Unity | `"<Unity editor>" -batchmode -quit -projectPath . -buildTarget <TARGET> -build<PLATFORM>Player Builds/<Target>/<Game>.exe` **(ASK — do not default)** | `"<Unity editor>" -batchmode -runTests -projectPath . -testPlatform EditMode -testResults test-results/editmode.xml` | `Builds/<Target>/<Game>.exe -screen-width 1280 -screen-height 720 -screen-fullscreen 0` | `"<Unity editor>" -batchmode -quit -projectPath . -logFile -` |

> **What each exit code proves — every row verified on the pinned engines.**
> Godot `test` exits 0 when all pass, 100 on a failure, 101 when all pass but
> nodes leaked (a warning, not a failure), 105 when a test script does not
> parse, and 103 / 104 when gdUnit4 cannot run at all (headless refused, Godot
> older than 4.3). Keep `--remote-debug tcp://127.0.0.1:0`: without it a script
> error opens Godot's interactive debugger and the run waits at a `debug>`
> prompt forever instead of exiting. Run `godot --headless --path . --import`
> before it on a fresh clone: with no `.godot/` class cache,
> `GdUnitCmdTool.gd` did not load and the run exits 1 having run nothing. Unity `test`
> exits 0 / 2, and a results file with `testcasecount="0"` means no test was
> compiled — not a pass. It runs Edit Mode only: Play Mode tests under
> `Assets/Tests/PlayMode/` need a second run into their own results file
> (`-testPlatform PlayMode -testResults test-results/playmode.xml`), which
> `$gs-smoke-check` makes whenever that folder holds tests and CI runs as its own
> step. Unity `smoke` exits 1 on a compile error, 0 when clean.
> **Godot `smoke` exits 0 even on a parse error** — it is a boot check: read its
> output for `SCRIPT ERROR`. It also needs `run/main_scene` set: without one it
> prints `Can't run project: no main scene defined` and never exits, so run it
> under a timeout. Unity `smoke` compiles only the editor-side assemblies; an
> error that exists only in a player build (an `Editor/` script without its own
> assembly) shows up in `build`, not here. The real Godot parse check is
> `godot --headless --path . --import`, then
> `godot --headless --path . -s <project-provided Godot parse adapter> -- res://<file>.gd …`
> (exit 1 when a script does not load). `--check-only` is not one: it fails
> valid code that names an autoload. `<Unity editor>` is the **editor**
> executable's full path, quoted. Never write bare `Unity`: on `PATH` that name
> may be Unity's separate CLI, which rejects `-batchmode` with exit 2 — the same
> code as a failed test.

> **`commands.run` is the one the run-and-observe step depends on.** It must
> launch the **game**, windowed, at a fixed resolution — never the editor, and
> never with a headless / batch / null-RHI flag, which exist to skip rendering.
> `$gs-dev-story` Phase 6 step 4 appends the per-engine capture flags to it
> (`.game-studio/resources/docs/run-and-observe.md`). `smoke` is Unity's parse check, `test`
> feeds `$gs-smoke-check`; `build` is the one row you must ask for.

> Native commands are argv lists, not shell strings. Inspect each argument;
> preserve paths as single array entries. Never insert timeout/shell operators.

> **Also write `engine.path` if the editor is not on `PATH`.** Agents and
> `$gs-smoke-check` read it to find the editor, but a command is run as written —
> `engine.path` is never spliced into `commands.*` at run time, which is why the
> full path goes into the commands above — and on Windows and macOS none of
> the three engines installs onto `PATH` by default (on macOS the editor is inside an app
> bundle, e.g. `/Applications/Godot.app/Contents/MacOS/Godot`). Ask for or probe the
> install location and record it — the editor executable for Godot and Unity,
> the engine folder (`<UE root>`) for Unreal:
>
> ```yaml
> engine:
>   path: "C:/Program Files/Epic Games/UE_5.7"   # omit if the editor is on PATH
> ```
>
> **This is not cosmetic.** Without it, an agent reports *"no editor on this
> machine"* and ships C++ it never compiled — on a machine where that engine WAS
> installed. Nothing in the project told it where to look, so absence of a path read
> as absence of an engine.

For **Unreal**, UE build/test commands vary by version and project setup. Write
best-effort values and add a `# TODO` comment so the user knows to confirm them.
Substitute the engine's install folder for `<UE root>` (the value you record as
`engine.path`) — none of the editor binaries is on `PATH`. The commands embed
double quotes, so they take single-quoted scalars. Write the block for the
machine the project is developed on (`uname -s`: `Linux`, `Darwin` = macOS,
anything else = Windows). The Windows block was run on UE 5.7; the Linux and
macOS lines come from Epic's documentation, recorded with their sources in
`<project-engine-reference>/current-best-practices.md` ("Command Line").

Windows:

```yaml
commands:
  # TODO: confirm these for your UE version and project — adjust via $gs-settings
  build: '"<UE root>/Engine/Binaries/DotNET/AutomationTool/AutomationTool.exe" BuildCookRun -project="$(pwd -W 2>/dev/null || pwd)/<project>.uproject" -platform=Win64 -build -cook'
  test: '"<UE root>/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" "$(pwd -W 2>/dev/null || pwd)/<project>.uproject" -ExecCmds="Automation RunTests <project>.; Quit" -unattended -nullrhi -stdout -FullStdOutLogOutput'
  run: '"<UE root>/Engine/Binaries/Win64/UnrealEditor.exe" "$(pwd -W 2>/dev/null || pwd)/<project>.uproject" -game -windowed -ResX=1280 -ResY=720'
  smoke: '"<UE root>/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" "$(pwd -W 2>/dev/null || pwd)/<project>.uproject" -game -nullrhi -unattended -stdout -ExecCmds="Quit"'
```

Linux — the editor binary is `Engine/Binaries/Linux/UnrealEditor`, the build
scripts are shell scripts:

```yaml
commands:
  # TODO: confirm these for your UE version and project — adjust via $gs-settings
  build: '"<UE root>/Engine/Build/BatchFiles/RunUAT.sh" BuildCookRun -project="$(pwd -W 2>/dev/null || pwd)/<project>.uproject" -platform=Linux -build -cook'
  test: '"<UE root>/Engine/Binaries/Linux/UnrealEditor" "$(pwd -W 2>/dev/null || pwd)/<project>.uproject" -ExecCmds="Automation RunTests <project>.; Quit" -unattended -nullrhi -stdout -FullStdOutLogOutput'
  run: '"<UE root>/Engine/Binaries/Linux/UnrealEditor" "$(pwd -W 2>/dev/null || pwd)/<project>.uproject" -game -windowed -ResX=1280 -ResY=720'
  smoke: '"<UE root>/Engine/Binaries/Linux/UnrealEditor" "$(pwd -W 2>/dev/null || pwd)/<project>.uproject" -game -nullrhi -unattended -stdout -ExecCmds="Quit"'
```

macOS — only the build is sourced. Epic documents the `UnrealEditor.app`
bundle but no command-line editor inside it, so write `build` and leave the
other three as TODO lines rather than a guessed path; `$gs-smoke-check` reports
NOT ASSESSED for tests until the user sets `commands.test`:

```yaml
commands:
  # TODO: confirm this for your UE version and project — adjust via $gs-settings
  build: '"<UE root>/Engine/Build/BatchFiles/RunUAT.sh" BuildCookRun -project="$(pwd -W 2>/dev/null || pwd)/<project>.uproject" -platform=Mac -build -cook'
  # TODO: test, run and smoke — no documented command-line editor on macOS.
  # Set them via $gs-settings to the editor command you run for this project.
```

On Windows, `build` calls AutomationTool directly: from Git Bash, `RunUAT.bat` fails
(`'C:\Program' is not recognized`) whenever the project path has a space.
AutomationTool.exe runs on the machine's .NET 8 runtime; `RunUAT.bat` brings
its own SDK, so with no space in the path and no .NET 8 installed, use it.
`-build` builds the editor target too (verified on 5.7).

**Three details are load-bearing.** The project path is absolute: UE 5.7
does not find a relative `<project>.uproject` and exits 1 (`Project file not
found`) before anything runs. `$(pwd -W 2>/dev/null || pwd)` gives the `C:/…`
form in Git Bash and the plain path elsewhere, run from the project root;
`$PWD` alone fails when `MSYS_NO_PATHCONV` is set. `smoke` needs `-game`: without it
`UnrealEditor-Cmd` boots the *editor*, where a bare `Quit` console command only
ends a play-in-editor session — the process stays resident and the command
never returns; with `-game` the same line boots headless and exits in seconds.
`test` needs the `; Quit` inside the `Automation` string: the automation
runner handles that trailing `Quit` itself and exits the editor once the tests
finish, and without it the run also never returns. Its filter runs every test
whose full name *contains* `<project>.` — a substring match, not a prefix — so
name tests `<project>.[System].[Scenario]` as `qa-tester` does. If the
project's name is also an engine area — `Audio`, `Core`, `Input`, `Test`,
`System`, `Engine`, `Editor`, `AI`, `Math` — `<project>.` also runs hundreds
to thousands of the engine's own tests; give the tests a distinct root (say
`<project>Game.`) and put the same root in the filter. This form exits 255 on
a failing test AND on a filter that matches nothing (`No automation tests
matched`, verified on 5.7), so `$gs-smoke-check` reads the output, not the exit
code. `smoke` carries `-stdout` for the same reason: without it a failed boot
prints nothing. Do not swap in
`-TestExit="Automation Test Queue Empty"`: that form exits **0** on a failing
test unless its report JSON is parsed.
