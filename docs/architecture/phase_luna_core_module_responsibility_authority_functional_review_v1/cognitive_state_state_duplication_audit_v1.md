# Cognitive State Duplication Audit

| Data | Classification | Recommendation |
|---|---|---|
| Current World object | REF_ONLY / DERIVED_SUMMARY | preserve candidate ref/version, no mutable copy |
| Context object | REF_ONLY | preserve Context owner and version |
| Field object | REF_ONLY | use read-only Field refs |
| Attention candidates | DERIVED_SUMMARY | assemble candidates, do not rank |
| Semantic relations | REF_ONLY / DERIVED_SUMMARY | keep Semantic Module-owned |
| Hypothesis candidates | DERIVED_CANDIDATE | no active-hypothesis mutation |
| Need/Sufficiency/Reconsideration | REF_ONLY | A-owned decisions only |
| source versions | DERIVED_ALIGNMENT | State Formation may own alignment record |
| trace/provenance | DERIVED_LINEAGE | preserve source lineage |

Main risk is treating candidate snapshot fields as authoritative duplicated state. Future forms should prefer refs plus version maps and explicit derived status.
