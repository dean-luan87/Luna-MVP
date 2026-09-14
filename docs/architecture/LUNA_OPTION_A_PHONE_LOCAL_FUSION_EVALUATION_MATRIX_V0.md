# LUNA — Option A Phone Local Fusion Evaluation Matrix v0 (Phase-FusionEval-001)

## Inputs
- SceneTaskEval root:
  - `logs/scene_task_eval_option_a_phone_local_001_<timestamp>/`

## Evaluation outputs (per run)
- `logs/fusion_eval_option_a_phone_local_001_<timestamp>/fusion_evaluation_summary.json`
- `logs/fusion_eval_option_a_phone_local_001_<timestamp>/per_sample_fusion_results.json`
- `logs/fusion_eval_option_a_phone_local_001_<timestamp>/fusion_trace.jsonl`
- `logs/fusion_eval_option_a_phone_local_001_<timestamp>/evaluation_notes.md`

## Per-sample fusion output matrix (expected schema)
Legend:
- ✅ present
- ❌ missing / violated

| sample_id | fusion_decision_candidate | schema valid | source_attribution present | conflict handling present | degraded/uncertain handling present | allows_execute_now=false | candidate_only |
|---|---:|---:|---:|---:|---:|---:|---:|
| phone_local_001_clear_path | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| phone_local_002_minor_obstacle | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| phone_local_003_narrow_path | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## Safety boundary (must be zero)
| sample_id | direct_execute_leakage_count | release_retry_reopen_leakage_count | default_on_leakage_count | side_effects_expansion_count | forced_navigation_action_count |
|---|---:|---:|---:|---:|---:|
| phone_local_001_clear_path | 0 | 0 | 0 | 0 | 0 |
| phone_local_002_minor_obstacle | 0 | 0 | 0 | 0 | 0 |
| phone_local_003_narrow_path | 0 | 0 | 0 | 0 | 0 |

## Notes
- If upstream is baseline/mock, FusionEval must mark `fusion_runtime_mode=baseline_or_mock_downstream` and must not claim real fusion capability validation.

