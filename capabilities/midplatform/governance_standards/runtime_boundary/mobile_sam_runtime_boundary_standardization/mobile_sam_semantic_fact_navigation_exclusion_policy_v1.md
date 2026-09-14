# MobileSAM Semantic / Fact / Navigation / Speech Exclusion Policy V1

## Status (all false, not granted now)

- `semantic_layer_ready`  
- `fact_write_ready`  
- `navigation_action_speech_ready`

## Rules

| Layer | Requirement |
|-------|-------------|
| Semantic | Separate governance; mask ≠ semantic object |
| Fact | Fact admission required; mask must not become fact |
| Navigation | Navigation action gate required |
| Speech | Speech gate required |

## MobileSAM Candidate Mask

- `candidate_mask_must_not_become_fact`  
- `candidate_mask_must_not_trigger_navigation`  
- `candidate_mask_must_not_trigger_speech`  
- `candidate_mask_must_not_update_world_model_without_admission`

## Real Image Trial Note

Object category names in prompts (road sign, building, etc.) are **test descriptions only**. MobileSAM does not produce semantic labels; category judgment requires separate evidence chain.
