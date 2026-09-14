# A3 Evidence Context Translation Layer Regression Matrix v1

| change surface | baseline invariant | required regression evidence | failure classification |
| --- | --- | --- | --- |
| Request/Object schema | required reference fields remain present and non-empty | Contract validation across five cases | blocker |
| Primitive type mapping | OCR/Vision/Spatial/Audio/Trace case mapping remains candidate-only | Semantic Expectation Matrix comparison | blocker |
| Candidate status | `translation_not_executed`, `candidate_only`, `not_fact` retained | candidate boundary check | blocker |
| Provenance/trace | candidate → request → Evidence → source capability remains complete | Provenance Closure Check | blocker |
| Permission flags | all no-execution/no-write flags remain fixed | Boundary flag comparison | blocker |
| Negative guards | all five guard IDs and failure conditions remain covered | Negative Guard Regression Check | blocker |
| Serializer | canonical JSON field ordering/normalization remains stable | deterministic rerun comparison | blocker |
| Runner | only fixed fixtures and Skeleton are used | Runner dependency review | blocker |
| Verifier | serialized-output only; no Runner/Skeleton call | verifier independence review | blocker |
| External binding | no real Evidence/model/Runtime binding is added | source and import boundary review | blocker |

Warnings may report a planned future real-Evidence binding, but it remains outside the validated baseline until a separately governed phase exists.
