# $gs-setup-engine — Section 12: Output Summary

> Part of `$gs-setup-engine`. `.agents/skills/gs-setup-engine/references/workflow.md` names when to read this file; the settings it
> resolved and the rules under its later headings still apply here.

## 12. Output Summary

Use Section 8's readback and Section 8.5's observations. Fill each field from what
was read, changed or verified on this run. Report unresolved discrepancies or missing
evidence with their reason.

```
Engine Setup Summary
=====================
Engine:          [configured name and version read back]
Language:        [configured language read back]
Knowledge Risk:  [LOW/MEDIUM/HIGH]
Reference Docs:  [resolved directory and actual outcome | NOT ASSESSED — reason]
AGENTS.md:       [actual outcome, normally unchanged]
Tech Prefs:      [created | updated | unchanged | skipped — reason]
project.yaml:    [created | updated | unchanged]
Agent Config:    [actual verification or skipped — reason]

Next Steps:
1. Review [resolved VERSION.md from project.documents, when present]
```

When VERSION.md is absent, identify the missing record and give the next verification step.

Then print **one** Next-Steps list: the main path, at every tier, in `$gs-next-step`'s
order (make a game, change it after you play it, grow it). Pick it by `$gs-next-step`'s
test: is there a game yet (`prototypes/*/index.html`, or 10 or more source files in
the code root)?

**No game yet:**
```
2. Make a game: run $gs-prototype and say the game in one line. On Web it is
   playable; on an engine it is a quick test build.
3. Play it, then ask for changes in plain words ("make the jump higher").
4. Not sure what comes next? $gs-next-step names the one next step.
```

**A game is here already:**
```
2. Play it, then ask for changes in plain words ("make the jump higher").
3. When it is worth keeping, $gs-next-step names the one next step to grow it.
```

At `standard` or `full`, add this line under the list:
```
Studio mode (design documents first): $gs-brainstorm, then $gs-map-systems and
$gs-design-system, then $gs-sprint-plan new.
```

---

Verdict: **COMPLETE** when the applicable setup work and readback agree. When they
do not, report **INCOMPLETE** and what remains. Report separately any check that
was **NOT ASSESSED**.
