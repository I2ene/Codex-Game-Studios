# Evaluation scenarios: gs-patch-notes

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-patch-notes/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Changelog filtered to player-facing entries

**Fixture:**
- `docs/CHANGELOG.md` has a `v0.4.0` entry with 5 items:
  - "Add dual-wield melee system" (player-facing)
  - "Fix crash on level transition" (player-facing)
  - "Add enemy patrol AI" (player-facing)
  - "Refactor input handler to use event bus" (internal only)
  - "Update dependency: Godot 4.6" (internal only)
- Git history since the previous tag holds the Game commits behind those items
- No tone guide and no patch-notes template exist

**Input:** `$gs-patch-notes v0.4.0`

**Domain checks:**
- [ ] The authorized write produces both `docs/patch-notes/v0.4.0.md` and `production/releases/v0.4.0/patch-notes.md`, with the same approved notes.
- [ ] Only the 3 player-facing items appear in the notes; the 2 internal items are listed separately as excluded, for review
- [ ] Entries are written in plain language without internal task IDs or system names
- [ ] Notes use the built-in Detailed style (Highlights, New Content, … Known Issues) — the default when no `--style` is given and no template exists
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is COMPLETE after the write

---

### Case 2: No Changelog File — Falls back to git history

**Fixture:**
- Neither `production/releases/v0.4.0/changelog.md` nor `docs/CHANGELOG.md` exists
- Tag `v0.3.0` exists; the range `v0.3.0..HEAD` holds 6 Game commits and 2
  Framework / maintenance commits (one touching a hook, one touching CI)

**Input:** `$gs-patch-notes v0.4.0`

**Domain checks:**
- [ ] Skill does not crash and does not stop with BLOCKED while git history is available
- [ ] Skill falls back to `git log` from the previous tag (`v0.3.0`) to HEAD
- [ ] Output states how many of how many commits were used
- [ ] The 2 framework / maintenance commits do not appear in the patch notes
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 3: Tone Guidance from Design Folder — Incorporated into output

**Fixture:**
- `docs/CHANGELOG.md` has a `v0.4.0` entry with player-facing items; git history
  holds the matching Game commits
- `design/community/tone-guide.md` exists with guidance: "upbeat, encouraging tone; avoid passive voice"
- `docs/PATCH-NOTES-STYLE.md` does not exist and
  `.game-studio/resources/docs/technical-preferences.md` has no tone, voice or style fields
- No patch-notes template exists

**Input:** `$gs-patch-notes v0.4.0`

**Domain checks:**
- [ ] Skill checks the tone sources in Phase 2b, including `design/community/tone-guide.md`
- [ ] The tone guide's instructions are applied in place of the built-in default tone
- [ ] Entries use active voice ("Fixed a crash when…", "You can now…"), not passive ("A crash was fixed")
- [ ] Tone guidance changes wording only — the output structure is still the Detailed style

---

### Case 4: Patch Note Template Exists — Used instead of the built-in styles

**Fixture:**
- `.game-studio/resources/docs/templates/patch-notes-template.md` exists with a header block,
  the sections `## New`, `## Fixed` and `## Known Issues`, and a footer
- `docs/CHANGELOG.md` has a `v0.4.0` entry with one new feature and one bug fix,
  both player-facing; git history holds the matching Game commits

**Input:** `$gs-patch-notes v0.4.0 --style full`

**Domain checks:**
- [ ] Skill globs both template locations before generating
- [ ] The template's structure replaces the built-in style — no "Developer Commentary" section from the Full style despite `--style full`
- [ ] The new feature is placed under `## New` and the fix under `## Fixed`
- [ ] The template's header and footer are preserved in the output
- [ ] Use the linked native procedure and explicit runtime command; retired host execution is not required.

---

### Case 5: Gate Compliance — No gate; community-manager is separate

**Fixture:**
- `docs/CHANGELOG.md` has a `v0.4.0` entry with player-facing items; git history
  holds the matching Game commits
- `project.yaml` sets `modes.review_mode: full`

**Input:** `$gs-patch-notes v0.4.0`

**Domain checks:**
- [ ] No director gate is invoked regardless of review mode
- [ ] Output suggests (but does not require) a community-manager tone review before posting
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is COMPLETE

---

### Case 6: Provenance Stop — Zero Game commits

**Fixture:**
- `git log --oneline -20` shows 20 commits, all touching the framework or
  tooling — subjects such as "fix: session-start hook timeout", "docs: skill
  catalog", "ci: cache the test runner" — and none names a game system in
  `design/` or the code root
- Neither `production/releases/v0.4.0/changelog.md` nor `docs/CHANGELOG.md` exists

**Input:** `$gs-patch-notes v0.4.0`

**Domain checks:**
- [ ] No patch notes is generated or written on this provenance/no-history stop.
- [ ] Output names the classification result — 0 of 20 commits are Game commits
- [ ] Output contains the "does not appear to belong to" stop, not notes written from framework commits (no "Fixed an issue where …" line from a hook fix)
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is BLOCKED, not COMPLETE

---

### Case 7: No Changelog Data — No changelog and no git history

**Fixture:**
- Neither `production/releases/v0.4.0/changelog.md` nor `docs/CHANGELOG.md` exists
- The project directory is not a git repository, so `git log` returns nothing

**Input:** `$gs-patch-notes v0.4.0`

**Domain checks:**
- [ ] No patch notes is generated or written on this provenance/no-history stop.
- [ ] The "does not appear to belong to" provenance stop is NOT shown — an empty history is not a wrong history
- [ ] Output contains "No changelog data found for v0.4.0" and recommends `$gs-changelog v0.4.0`
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is BLOCKED
