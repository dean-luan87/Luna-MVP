# LUNA — Option A Phone Local Perception Evaluation Matrix v0 (Phase-PerceptionEval-001)

## Inputs
- sample_matrix:
  - `logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`

## Evaluation outputs (per run)
- `logs/perception_eval_option_a_phone_local_001_<timestamp>/perception_evaluation_summary.json`
- `logs/perception_eval_option_a_phone_local_001_<timestamp>/per_sample_results.json`
- `logs/perception_eval_option_a_phone_local_001_<timestamp>/signal_trace.jsonl`
- `logs/perception_eval_option_a_phone_local_001_<timestamp>/evaluation_notes.md`

## Per-sample signal presence matrix (expected schema)
Legend:
- ✅ present (can be `not_available` where allowed)
- ❌ missing (not allowed)

| sample_id | object_stability_signal | ocr_navigation_signal | spatial_passability_signal | dynamic_event_signal | risk_field_signal |
|---|---:|---:|---:|---:|---:|
| phone_local_001_clear_path | ✅ | ✅ | ✅ | ✅ | ✅ |
| phone_local_002_minor_obstacle | ✅ | ✅ | ✅ | ✅ | ✅ |
| phone_local_003_narrow_path | ✅ | ✅ | ✅ | ✅ | ✅ |

## Safety & boundary matrix (must be zero leakage)
| sample_id | execute_leakage_count | default_on_leakage_count | side_effects_expansion_count | evidence_type_preserved | controlled_live_stream_false |
|---|---:|---:|---:|---:|---:|
| phone_local_001_clear_path | 0 | 0 | 0 | ✅ | ✅ |
| phone_local_002_minor_obstacle | 0 | 0 | 0 | ✅ | ✅ |
| phone_local_003_narrow_path | 0 | 0 | 0 | ✅ | ✅ |

## Notes
- v0 allows `perception_runtime_mode=baseline_or_mock`; this must be stated and must not claim real model capability.
- OCR may be `not_available` but must not fabricate OCR content.

