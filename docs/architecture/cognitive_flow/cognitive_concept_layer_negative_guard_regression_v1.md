# Cognitive Concept Layer Negative Guard Regression v1

| Guard | Required serialized evidence |
| --- | --- |
| Concept is not Fact | `candidate_only=true`; `fact_status=not_fact`; no `fact_id` |
| Concept is not Decision | `decision_created=false`; no `decision_id` |
| Concept is not Action | `action_created=false`; no `action_id` |
| No Field State modification | `field_kernel_mutated=false`; `state_writeback=false` |
| No Memory write | `memory_updated=false`; no `memory_target` |
| No Learning admission | `learning_integrated=false` |
| No Language-to-Concept reverse path | `language_encoding_executed=false`; design-only Language interface |
| No provider taxonomy pollution | provider/model terms absent from `concept_type` |

The validator and verifier do not weaken a guard or hardcode a passing decision. A failed guard is a blocker.
