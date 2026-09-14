# A3 Evidence Context Translation Layer Semantic Expectation Matrix v1

| case | external Evidence fixture | permitted primitive type | fixture vocabulary only | prohibited semantic escalation |
| --- | --- | --- | --- | --- |
| OCR | `text_candidate:出口` | `semantic_candidate` | `exit_related_candidate` | “这里存在出口” Fact; “用户应该向右走” Decision |
| Vision | `object_candidate:person` | `entity_candidate` | `human_candidate` | `confirmed_person`; identity inference; provider identity as Entity |
| Spatial | `location_reference` | `spatial_candidate` | `location_related_candidate` | navigation decision; route action; Field/State update |
| Audio | `speaker_candidate` | `semantic_candidate` | `speaker_related_candidate` | identity confirmation; relationship judgment |
| Provenance Trace | trace-required Evidence reference | `temporal_candidate` | `trace_preserving_candidate` | hidden source; missing source ref; semantic conclusion |

Fixture vocabulary labels express permitted candidate intent for regression comparison. The controlled Skeleton does not generate these labels, infer a world meaning, or promote any label to Fact.
