# Evaluation scenarios: gs-audio-director

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-audio-director.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output format
**Scenario:** The user has approved the direction for the game's "Exploration" music layer: a generative ambient system of layered stems that shift with environmental density, in a sparse, organic, slightly melancholic palette, meant to reinforce the pillar "lived-in world." The user asks audio-director to draft the audio asset specification for this layer.
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.
**Checklist:**
- [ ] Every asset name follows `[category]_[context]_[name]_[variant].[ext]` (e.g., `mus_explore_forest_calm_loop.ogg`)
- [ ] Specifies format, sample rate, loudness target (LUFS), and file-size budget for the music assets
- [ ] Rationale ties the density-driven stem layering to the "lived-in world" pillar
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.

---

### Case 2: Out-of-domain request — redirects or escalates
**Scenario:** A developer asks audio-director to evaluate whether the UI flow for the audio settings menu (the sequence of screens and options) is intuitive and well-organized.
**Domain checks:** Agent does not rule on screen flow or menu organization — that is UX, not audio. It limits its answer to the audio requirements the menu must expose, derived from its own mix strategy, and leaves flow and layout to ux-designer.
**Checklist:**
- [ ] Does not make any binding decision about UI flow, screen sequence, or information architecture
- [ ] States that flow and layout are outside the audio domain rather than evaluating them
- [ ] Explicitly names `ux-designer` as the owner of the menu's flow and layout (its file defers UX decisions to ux-designer)
- [ ] Limits its contribution to audio requirements taken from its mix strategy (e.g., one slider per bus in its volume hierarchy — master, music, SFX, dialogue)

---

### Case 3: Review findings — specific, verdict left to the review skill
**Scenario:** `$gs-design-review` in full mode spawns audio-director as the adversarial specialist for a boss-encounter GDD that contains music triggers. The spawn prompt reads: "Your job is NOT to validate this design — your job is to find problems. Be specific and critical." The GDD's final-boss cue is an upbeat, major-key orchestral piece with fast tempo; the game pillars and narrative context for the encounter specify "dread, inevitability, and tragic sacrifice."
**Domain checks:** Returns specific findings: the cue's major key, fast tempo, and upbeat register contradict the emotional targets, with revision directions offered as options. It returns findings, not a verdict — the review's verdict is produced by `$gs-design-review`.
**Checklist:**
- [ ] Identifies the specific musical characteristics that conflict (major key, fast tempo, upbeat register)
- [ ] Names the emotional targets the cue contradicts (dread, inevitability, tragic sacrifice), treating them as the encounter's emotional mapping
- [ ] Provides actionable revision directions (e.g., minor mode, slower tempo, thinner ensemble) as options with a recommendation
- [ ] Returns findings to the review, not its own APPROVED / NEEDS REVISION stamp

---

### Case 4: Conflict escalation — correct parent
**Scenario:** sound-designer proposes implementing audio occlusion using real-time raycast-based physics queries. technical-artist argues this is too expensive and proposes a zone-based trigger system instead. Both agree the occlusion effect is desirable; the conflict is purely about implementation approach.
**Domain checks:** audio-director defines the desired audio behavior (what occlusion should sound like and when it should activate) as the requirement either approach must meet, then defers the raycast-vs-zone choice to `lead-programmer` — the agent its file names for audio system implementation — or to `technical-director` for a technical conflict. It does not pick the implementation, and does not hand the decision to either party in the dispute.
**Checklist:**
- [ ] Defines the desired audio behavior clearly (what the player hears, when occlusion engages, how strongly it attenuates)
- [ ] Defers the implementation approach (raycast vs. zone-trigger) to `lead-programmer` or `technical-director` — not to sound-designer or technical-artist, who are the disputants
- [ ] Does not unilaterally choose the technical implementation method
- [ ] States the audio behavior as the requirement either implementation must satisfy, so the technical decision can be checked against it

---

### Case 5: Context pass — uses provided context
**Scenario:** The request includes the game's three pillars: "emergent stories," "meaningful sacrifice," and "lived-in world." An ambient environmental audio spec is submitted: one static loop per biome, with no layer that responds to player actions or world events.
**Domain checks:** Assessment evaluates the ambient spec against all three pillars by name. It flags that static loops do not support "emergent stories" because nothing in the audio responds to game state, and points to adaptive audio as the gap.
**Checklist:**
- [ ] References all three provided pillars by name in the assessment
- [ ] Evaluates the audio spec's contribution to each pillar explicitly
- [ ] Flags "emergent stories" as unsupported because the loops do not respond to game state, naming adaptive audio (state-driven layers or transitions) as the missing piece
- [ ] Does not generate generic audio direction advice — all feedback is tied to the provided pillar vocabulary
