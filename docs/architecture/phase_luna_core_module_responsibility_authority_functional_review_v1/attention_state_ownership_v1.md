# Attention State Ownership v1

| State | Classification | Owner/meaning |
|---|---|---|
| attention_candidate_id | candidate identity | Attention allocation candidate |
| focus target/object/region refs | reference/candidate | source refs plus Attention candidate |
| focus/relevance score | local derived candidate | Attention scoring, not semantic Truth |
| priority | candidate | Attention within Brain policy |
| urgency | candidate/reference | source/policy-derived candidate |
| modality preference | candidate | Attention; Capability remains external |
| budget candidate | candidate | Brain ceilings plus Attention allocation |
| persistence/decay | local derived/mechanical candidate | Attention policy |
| source Need ref | reference-only | A |
| Task/Context refs | reference-only | Task/Context |
| Role/Perspective refs | reference-only | Role/Perspective boundary |
| Brain policy ref | reference-only | Brain/resource governance |
| source versions | reference-only | source owners |
| trace/provenance | candidate lineage | Attention allocation |
| actual resource commitment | external | Brain/Capability/Observation execution |

No Attention payload should be treated as authoritative semantic state. An
allocation candidate may be accepted by a later governance/execution boundary,
but this review does not create that runtime authority.
