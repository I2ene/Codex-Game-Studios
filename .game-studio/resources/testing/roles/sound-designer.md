# Evaluation scenarios: gs-sound-designer

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-sound-designer.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output
**Input:** "Create an SFX spec for a sword swing attack."
**Domain checks:**
- Produces a complete SFX spec sheet including:
  - Description, reference sounds, frequency character, and duration
  - Volume range and spatial properties
  - Variation plan: number of variants, pitch randomization range (e.g., ±8%), and round-robin behavior
  - Audio event entry: what triggers it, priority, concurrency limit, and cooldown
  - Bus assignment for mixing (e.g., the combat SFX bus)
- Event name follows the project audio naming convention if one is established (e.g., `sfx_combat_sword_swing`)
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.

---

### Case 2: Out-of-domain request — redirects correctly
**Input:** "Compose a looping ambient music track for the forest level."
**Domain checks:**
- Does NOT produce music composition direction or a music brief, and does not create the audio itself
- Explicitly states that music direction belongs to `audio-director`
- Redirects the request to `audio-director`
- Anything it offers in place of the track is from its own domain — e.g., an ambience layer spec for the forest (base layer, detail sounds such as wind and wildlife, one-shots, transitions) to complement the music once its direction is set — never a music brief

---

### Case 3: Dynamic parameter — falloff curve spec
**Input:** "The sword swing SFX needs distance falloff so it sounds different across the arena."
**Domain checks:**
- Documents the event's spatial properties for distance:
  - Parameter name (e.g., `distance` or `listener_distance`)
  - Falloff curve type (e.g., logarithmic, linear, custom)
  - Near/far distance thresholds with corresponding volume and high-frequency attenuation values
- Asks about behavior the request leaves unspecified (e.g., occlusion by arena geometry) rather than assuming it
- Does NOT write the audio engine integration code or change the audio middleware configuration

---

### Case 4: Naming convention conflict
**Input:** "Add a new SFX event called `SWORD_HIT_1` for the melee system." [Context includes the audio-director's naming convention: `[category]_[context]_[name]_[variant]`, e.g., `sfx_combat_sword_swing_01`.]
**Domain checks:**
- Identifies that `SWORD_HIT_1` deviates from the naming convention in context
- Does NOT silently register the non-conforming name
- Flags the deviation explicitly with a compliant alternative (e.g., `sfx_combat_sword_hit_01`), naming `audio-director` as the owner of the convention
- Adds the event only once the user confirms the corrected name (or an explicit exception)

---

### Case 5: Context pass — uses audio style guide
**Input:** Audio style guide provided in context specifying: "gritty, grounded, no reverb tails over 1.5s, reference: The Witcher 3 combat audio." Request: "Create SFX specs for the full melee combat suite."
**Domain checks:**
- References the "gritty, grounded" tone descriptor in the spec rationale
- Caps all reverb tail specifications at 1.5 seconds as stated
- Notes the reference material (The Witcher 3) as a benchmark for mix levels and transient design
- Does NOT produce specs that contradict the style guide (e.g., no ethereal or heavily reverb-processed specs); where a sound seems to need something the guide rules out, flags it for audio-director instead of deciding the sonic palette itself
