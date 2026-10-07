# Evaluation scenarios: gs-level-designer

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-level-designer.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output format
**Scenario:** The user has agreed the outline for "The Flooded Tunnels": a low-intensity exploration opening, two mid-intensity encounters with visible escape routes, a tension-building narrow passage with environmental hazards, and a high-intensity final encounter room followed by a release/reward area. The user asks level-designer to draft the level document.
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.
**Checklist:**
- [ ] The document has all nine Level Document Standard sections: Level Name and Theme, Estimated Play Time, Layout Diagram, Critical Path, Optional Paths, Encounter List, Pacing Chart, Narrative Beats, Music/Audio Cues
- [ ] The Pacing Chart follows the outline's intensity curve — low opening, mid encounters, rising passage, high final encounter, release — with its rest points marked
- [ ] The Encounter List gives type, difficulty, and position for each encounter
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.

---

### Case 2: Out-of-domain request — redirects or escalates
**Scenario:** A team member asks level-designer to write the behavior tree code for an enemy patrol AI that navigates the level layout.
**Domain checks:** Agent declines to write AI behavior code — implementation is outside its role — and instead specifies the patrol from a level design perspective, as input for ai-programmer.
**Checklist:**
- [ ] Does not write or specify code for AI behavior logic
- [ ] States that behavior-tree code is implementation work outside its role, rather than taking it on
- [ ] Explicitly names `ai-programmer` (or `gameplay-programmer`, which its file names for engine implementation) as who implements it
- [ ] Specifies the desired patrol in level design terms (e.g., route through named chokepoints and sight lines, pressure zones, spawn timing) for the programmer to implement

---

### Case 3: Review findings — specific, verdict left to the review skill
**Scenario:** `$gs-design-review` in full mode spawns level-designer as the adversarial specialist for the level document of "The Ancient Forge." The spawn prompt reads: "Your job is NOT to validate this design — your job is to find problems. Be specific and critical." Section 3 of the level introduces a dramatically harder elite enemy with new attack patterns, with no earlier moment that introduces it, no environmental readability cues (no visible cover or safe zones), and no checkpoint nearby.
**Domain checks:** Returns specific findings locating the problem in section 3: the difficulty spike, the missing readability cues, and the missing checkpoint, each with a concrete spatial fix offered as an option. It returns findings, not a verdict — `$gs-design-review` issues the verdict.
**Checklist:**
- [ ] Identifies section 3 specifically as the location of the issue
- [ ] Identifies the three specific problems: difficulty spike without an introduction, missing readability cues, missing nearby checkpoint
- [ ] Provides actionable spatial revision options (e.g., introduce the elite in isolation first, add a visible safe zone or cover, place a checkpoint before the arena)
- [ ] Returns findings to the review, not its own APPROVED / NEEDS REVISION stamp

---

### Case 4: Conflict escalation — correct parent
**Scenario:** game-designer wants higher encounter density throughout the level (more enemies in each room) to increase combat challenge. level-designer believes this density undermines the pacing arc by eliminating rest periods and making the level feel relentless without reward.
**Domain checks:** level-designer states the pacing concern in pacing-chart terms (removing rest points flattens the tension-release rhythm), acknowledges game-designer's challenge goal, lays out the options, and escalates to creative-director for a design arbiter ruling on whether challenge density or pacing rhythm takes precedence for this level.
**Checklist:**
- [ ] States the specific pacing impact: denser rooms remove the rest points, flattening the intensity curve into constant high intensity
- [ ] Escalates to `creative-director` as the design arbiter
- [ ] Does not unilaterally override game-designer's challenge density request
- [ ] Presents the choice as options (e.g., keep density, keep rest points, add density with dedicated rest rooms) with a recommendation, leaving the ruling to the arbiter

---

### Case 5: Context pass — uses provided context
**Scenario:** The request includes game-feel notes: "exploration sections should feel vast and lonely," "combat sections should feel urgent and claustrophobic," and "reward rooms should feel safe and visually distinct." A new level layout is submitted for the agent's assessment. Its exploration section is a narrow, winding corridor, and its reward room uses the same lighting and layout as the combat arena before it.
**Domain checks:** Assessment evaluates each section type (exploration, combat, reward) against its feel target, using the exact vocabulary from the notes, and flags the two sections that conflict with their targets.
**Checklist:**
- [ ] References all three feel targets from the provided context by their exact vocabulary
- [ ] Evaluates each relevant section of the submitted layout against its corresponding feel target
- [ ] Flags the narrow exploration corridor as conflicting with "vast and lonely," and the reward room as not "visually distinct" from the arena
- [ ] Does not generate generic pacing advice — all feedback is tied to the provided feel targets
