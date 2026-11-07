# $gs-setup-engine — Sections 8 and 8.5: Verify and Read Back

> Part of `$gs-setup-engine`. `.agents/skills/gs-setup-engine/references/workflow.md` names when to read this file; the settings it
> resolved and the rules under its later headings still apply here.


## 8. Verify project reference routing

Confirm engine.name/version and engine.reference_root identify actual project
records. Read them explicitly; there are no @ imports in native instructions.

## 8.5 Read Back What You Just Wrote

This section exists because prose did not hold. Section 5.5.1's rendering/physics
table already carries an emphatic, source-cited warning naming the two mistakes
most often made here -- and it is still entirely possible to make **both** of
them anyway, writing `Forward+` and `Jolt` for a 2D browser game. Section 3's
`Installed at pin time` row is just as easy to drop silently, because a missing
row leaves no trace.

Neither is fixed by adding more instructions. They are fixed by verifying the
files after writing them:

```bash
python .game-studio/runtime/studio.py coherence --root <project-root>
```

Consume observations/counts JSON. Local comparisons cover project VERSION and
recorded installed pin, engine project version/settings, Godot rendering/2D physics,
configured runner script paths and export presets. Every DIFFERS needs reconciliation
before setup is called coherent. Every NOT ASSESSED needs its reason in the report.
The default command never probes a binary. Inspect commands.engine_probe first; run
coherence --probe only within authorization and retain actual exit/output. An absent
probe or engine project file cannot establish agreement or a working engine build.

The script emits observations and never a verdict, per the convention in
AGENTS.md. The judgement is yours and the user's.

---
