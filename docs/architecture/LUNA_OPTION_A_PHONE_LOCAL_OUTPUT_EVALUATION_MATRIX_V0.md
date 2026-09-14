# LUNA — Option A Phone Local Output Evaluation Matrix v0 (Phase-OutputEval-001)

## Inputs
- FusionEval root:
  - `logs/fusion_eval_option_a_phone_local_001_<timestamp>/`

## Evaluation outputs (per run)
- `logs/output_eval_option_a_phone_local_001_<timestamp>/output_evaluation_summary.json`
- `logs/output_eval_option_a_phone_local_001_<timestamp>/per_sample_output_results.json`
- `logs/output_eval_option_a_phone_local_001_<timestamp>/output_trace.jsonl`
- `logs/output_eval_option_a_phone_local_001_<timestamp>/evaluation_notes.md`

## Per-sample output candidate matrix (expected schema)
Legend:
- ✅ present / valid
- ❌ missing / violated

| sample_id | navigation_output_candidate | schema valid | output_type present | priority valid | timing valid | suppression present | allows_execute_now=false | real_tts_invoked=false | candidate_only |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| phone_local_001_clear_path | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| phone_local_002_minor_obstacle | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| phone_local_003_narrow_path | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## Safety boundary (must be zero)
| sample_id | forbidden_output_semantic_count | direct_execute_leakage_count | release_retry_reopen_leakage_count | default_on_leakage_count | side_effects_expansion_count |
|---|---:|---:|---:|---:|---:|
| phone_local_001_clear_path | 0 | 0 | 0 | 0 | 0 |
| phone_local_002_minor_obstacle | 0 | 0 | 0 | 0 | 0 |
| phone_local_003_narrow_path | 0 | 0 | 0 | 0 | 0 |

## Notes
- v0 allows `output_runtime_mode=baseline_or_mock_downstream`; must not claim real output policy validation.
- v0 does not emit real TTS; only evaluates candidate outputs.

