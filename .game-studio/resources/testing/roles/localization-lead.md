# Evaluation scenarios: gs-localization-lead

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-localization-lead.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — string extraction pipeline for a Unity project
**Input**: "Set up a string extraction pipeline for our Unity game. We need to get all localizable strings into a format translators can work with."
**Domain checks**:
- Lays out the workflow its String Extraction Workflow defines: strings enter through the localization API (never raw text), land in the base locale file with a context comment, extraction tooling collects new and modified strings, and they go to translators with context, screenshots, and character limits, then come back into the locale files
- Scopes extraction to player-facing text from code, UI, and content — "Ensure no hardcoded strings reach production"
- Specifies structured locale files (JSON, CSV, or a project-appropriate format), one file per language per system or feature area (the `locales/en/ui_menu.json` pattern)
- Uses hierarchical dot-notation keys that describe context (`menu.settings.audio.volume_label`) — not positional or index-based keys — each with a context comment giving where it appears, its character limit, and its variables
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.

---

### Case 2: Out-of-domain request — translate game dialogue
**Input**: "Translate the following English dialogue into French: 'Well met, traveler. The road ahead is treacherous.'"
**Domain checks**:
- Does not produce a French translation
- States that it owns the pipeline, quality standards and workflow, and that translation itself is done by human translators or approved vendors (its "Write actual translations" must-not line)
- Optionally notes what information a translator would need: context (who is speaking, to whom, game genre/tone), character limit constraints if any, glossary terms (e.g., if "traveler" has a game-specific translation)

---

### Case 3: Domain boundary — missing plural forms in Russian locale
**Input**: "Our Russian locale files only have a singular form for item quantity strings. Russian requires multiple plural forms (1 item, 2-4 items, 5+ items use different forms)."
**Domain checks**:
- Identifies this as a locale-specific plural form gap: CLDR/Unicode plural rules give Russian four categories — one, few, many and other (`other` covers fractional quantities, and ICU MessageFormat requires it in every plural message) — so a single string is insufficient
- Flags it as a localization quality bug, not a minor style issue — incorrect plural forms are grammatically wrong and visible to players
- Recommends the fix its Pluralization standard names: plural rules through ICU MessageFormat (or equivalent) with the language's plural categories, and flags to the translators that Russian strings need every plural form
- Treats it as a pipeline-wide fix — quantity strings in every supported locale move to ICU plural rules — not a Russian-only patch (Polish, Czech, and Arabic have the same problem)
- Does NOT suggest using a numeric threshold workaround as a substitute for proper plural rules

---

### Case 4: String key naming conflict between two systems
**Input**: "Our UI system uses keys like 'button_confirm' and 'button_cancel'. Our dialogue system uses 'confirm' and 'cancel' for the same concepts. Translators are confused about which to use."
**Domain checks**:
- Identifies the conflict: two systems use different key naming conventions for semantically identical strings, creating duplicate translation work and translator confusion
- Produces a naming convention resolution in its hierarchical dot-notation standard (e.g., `ui.button.confirm`, `ui.button.cancel`) — all systems use the same key for shared concepts
- Recommends that shared UI primitives (Confirm, Cancel, Back, OK) use a single canonical key in a shared namespace, referenced by both systems, and records the terms in the glossary
- Plans the key change so nothing breaks: every reference in both systems moves to the new key, no lookup is left pointing at a retired key (its Key naming convention rule, and Fallback chains: "never display raw keys to players"), existing translations carry over through translation memory, and the code change in both systems is coordinated with their owners before it is made
- Does NOT recommend maintaining two separate keys for the same concept

---

### Case 5: Context pass — pipeline accommodates RTL languages
**Input context**: Target locales include English (en), French (fr), German (de), Arabic (ar), and Hebrew (he).
**Input**: "Design the localization pipeline for this project."
**Domain checks**:
- Identifies Arabic and Hebrew as RTL languages — explicitly calls this out as a pipeline requirement
- Designs the pipeline to include its RTL requirements: mirrored UI layout, bidirectional text in the same string, numbers kept LTR inside RTL text, flipped directional UI, and testing with native RTL speakers — with RTL rendering coordinated with `ui-programmer`
- Does NOT design a pipeline that only accounts for LTR languages when RTL locales are specified
- Covers the Arabic/Hebrew font needs (RTL shaping, ligatures, contextual forms) and plural rules through ICU MessageFormat for every locale
- Includes all five locales: a fallback chain, and its Locale-Specific Testing Requirements (dates, numbers, currency, time, sorting, input, text rendering) applied to each language, not just the default (en)
