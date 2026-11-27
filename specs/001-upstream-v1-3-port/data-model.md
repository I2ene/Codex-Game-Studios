# Port data model

## SourceMapping
- `SourceMapping.source_version`: fixed previous or target upstream commit; never inferred from filenames.
- `SourceMapping.disposition`: reuse, host adaptation, verified equivalent or host boundary.
- `SourceMapping.paths`: source before/after and native before/after; a retired source has an explicit replacement or unavailable boundary.
- `SourceMapping.verification`: actual test/contract reference with evidence level, not a claim all scenarios passed.

## EngineConfiguration
- `EngineConfiguration.name`: Web/Godot/Unity/Unreal or retained custom value; absent/unconfigured is distinct.
- `EngineConfiguration.roots`: nested shared `engine.code_root`/`engine.test_root` first, compatible top-level keys next, engine-table defaults last. Invalid explicit values do not fall back; '.' is project root with framework/generated directories excluded.
- `EngineConfiguration.commands`: explicit consumer argv retains precedence; table command text is a suggestion, not execution authority.
- `EngineConfiguration.goal`: upstream project goal choices with unset distinguished from guessed/saved values.

## BriefAndEvidence
- `BriefAndEvidence.features`: stable feature identity, built/unbuilt state and story references; legacy MVP remains readable.
- `BriefAndEvidence.provenance`: original user words retained; guessed/inferred/provisional fields explicit.
- `BriefAndEvidence.verdicts`: observed PASS/MISSING/BROKEN/NOT ASSESSED; human playtest limitations and sampled replay bounds explicit.
- `BriefAndEvidence.participants`: parent-thread authorship or actual delegated participants, never invented independent review.

## OwnedInstallation
- `OwnedInstallation.files`: hash-owned payload predicate excludes Spec Kit; edited managed files conflict before writes, unowned consumer files survive.
