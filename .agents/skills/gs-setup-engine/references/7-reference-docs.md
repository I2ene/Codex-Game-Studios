# $gs-setup-engine — Section 7: Populate Engine Reference Docs

> Part of `$gs-setup-engine`. `.agents/skills/gs-setup-engine/references/workflow.md` names when to read this file; the settings it
> resolved and the rules under its later headings still apply here.


## 7. Populate Engine Reference Docs

### First: does a reference set already exist for this engine?

Run engine-reference --root <project-root> and use project.root/documents. The
installer ships historical examples under .game-studio/resources only; it does not
populate project-owned reference records. Compare project.documents.VERSION.md
(if present) with the actual chosen engine/version. Missing project records remain
unknown; create them from current verified official sources and confirmed probes.
Preserve and update an existing project's records, including prior version spans.
Use engine.reference_root when configured; <project-engine-reference> below means
the resolved exact folder. Packaged examples never establish installed versions.

- **No directory, or no `VERSION.md`** → create, using the risk branch below.
- **Same version** → nothing to regenerate. Refresh `Last Docs Verified` only if you
  actually re-verified against the docs this run. Do not restamp a date you did
  not check. The one row still written is `Installed at pin time`, from
  Section 3 — its probe result is recorded whatever the outcome, after asking
  "May I record `Installed at pin time: [result]` in
  `<project-engine-reference>/VERSION.md`?" (it is a tracked file).
- **Directory pins an OLDER version than the one chosen** → **update, do not
  replace.** This is the common case. Show the changes below, then ask "May I
  update the `<project-engine-reference>/` files for [version]?" before editing.
  1. Edit `VERSION.md` in place: new **Engine Version**, new **Project Pinned**
     and **Last Docs Verified**, the `Installed at pin time` row from Section 3,
     and a new row in the post-cutoff timeline for each version added.
  2. **Append** to `breaking-changes.md`, `deprecated-apis.md` and
     `current-best-practices.md` under a heading naming the version span
     (`## 4.6 → 4.7`). Never truncate the older spans — a project migrating
     across two versions still needs the earlier one.
  3. Re-grade the older timeline rows if the cutoff moved past them.
- **Directory pins a NEWER version than the one chosen** → stop and ask. Someone
  pinned forward deliberately, or the version choice is wrong. Do not silently
  downgrade a curated reference.

### Sourcing rule for everything written in this section

**Never fill a gap from training data. Write the gap down instead.**

The whole purpose of these files is to be the thing agents consult *instead of*
their training data. A confidently wrong entry here is worse than no entry: it
produces work that looks verified and is not.

- Every claim must come from a page you fetched this run. Record the URL.
- If the official docs do not state something the template asks for — a release
  date, a subsystem's behaviour, web-export specifics — write
  **`NOT SOURCEABLE — <what>, not stated at <url>`** and move on.
- A `NOT SOURCEABLE` line is a successful outcome, not a failure to finish.
- Do not infer one fact from an adjacent one. "The migration guide lists no
  physics change" is not "the physics default is unchanged"; if you record the
  inference, label it as an inference and name what it rests on.

### If WITHIN training data (LOW RISK):

Ask: "May I create `<project-engine-reference>/VERSION.md`?" Wait for
confirmation, then create this minimal file:

```markdown
# [Engine] — Version Reference

| Field | Value |
|-------|-------|
| **Engine Version** | [version] |
| **Project Pinned** | [today's date] |
| **Installed at pin time** | [Section 3 result — the installed version, or NOT DETERMINED] |
| **LLM Knowledge Cutoff** | [the cutoff from the Section 6 coverage table] |
| **Risk Level** | LOW — version is within LLM training data |

## Note

This engine version is within the LLM's training data. Engine reference
docs are optional but can be added later if agents suggest incorrect APIs.

Run `$gs-setup-engine refresh` to populate full reference docs at any time.
```

Do NOT create breaking-changes.md, deprecated-apis.md, etc. — they would
add context cost with minimal value.

### If BEYOND training data (MEDIUM or HIGH RISK):

Create the full reference doc set by searching the web:

1. **Search for the official migration/upgrade guide**:
   - `"[engine] [old version] to [new version] migration guide"`
   - `"[engine] [version] breaking changes"`
   - `"[engine] [version] changelog"`
   - `"[engine] [version] deprecated API"`

2. **Fetch and extract** from official documentation:
   - Breaking changes between each version from the training cutoff to current
   - Deprecated APIs with replacements
   - New features and best practices

Ask: "May I create the engine reference docs under `<project-engine-reference>/`?"

Wait for confirmation before writing any files.

3. **Create the full reference directory**:
   ```
   <project-engine-reference>/
   ├── VERSION.md              # Version pin + knowledge gap analysis
   ├── breaking-changes.md     # Version-by-version breaking changes
   ├── deprecated-apis.md      # "Don't use X → Use Y" tables
   ├── current-best-practices.md  # New practices since training cutoff
   └── modules/                # Per-subsystem references (create as needed)
   ```

4. **Populate each file** using real data from the web searches, following
   the format established in existing reference docs. Every file must have
   a "Last verified: [date]" header.

5. **For module files**: Only create modules for subsystems where significant
   changes occurred. Don't create empty or minimal module files.

---
