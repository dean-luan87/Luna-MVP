# Cognitive Provider Adaptive Control Boundary v1

## Candidate payload

`provider_adaptive_control_candidate` contains:

- `attention_adjustment_candidate`
- `capability_refinement_candidate`
- `information_state_candidate`
- `no_text_means_absent=false`
- `attention_allocation_changed=false`
- `provider_invocation_requested=false`

## Authority separation

| Concern | Owner | V1 adaptive-control role |
|---|---|---|
| Cognitive purpose and goal | Brain | Unchanged. |
| Signal quality interpretation | Neural Governance | Creates bounded quality and adaptation candidates. |
| Actual attention allocation | Attention Controller | Not invoked in this phase. |
| Capability resolution / provider selection | Middleware | Not invoked by the candidate. |
| Provider execution | Provider Adapter | Only the original fixed-fixture OCR execution. |
| Truth / Reality / state mutation | No component in this phase | Prohibited. |

## Negative rule

`empty OCR output → no text exists` is forbidden. The only permitted conclusion is `information_insufficient_candidate`, with the unknown retained for future cognitive handling.
