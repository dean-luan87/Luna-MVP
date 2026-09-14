# Cognitive Concept Layer Validation Matrix v1

| Area | Evidence | Required result | Failure level |
| --- | --- | --- | --- |
| Concept schema | Serialized candidate fields | All required fields populated | blocker |
| Type mapping | Six fixed case identifiers/types | Pattern, Situation, Relationship, Risk, Context, Goal match | blocker |
| Primitive integrity | Non-empty `primitive:` references | Concept has Primitive lineage | blocker |
| Context integrity | Non-empty `context:` references | Context lineage retained | blocker |
| Provenance closure | Concept, Primitive, Translation, source/Evidence, capability, trace | Full ordered reference chain | blocker |
| Candidate lifecycle | candidate-only / not-fact / no authority fields | No promotion authority | blocker |
| Language boundary | Design-only flag | No encoding or reverse generation | blocker |
| Negative guards | Eight guard results | All true | blocker |
| Determinism | Canonical run1/run2 output | `comparison_equal=true` | blocker |
