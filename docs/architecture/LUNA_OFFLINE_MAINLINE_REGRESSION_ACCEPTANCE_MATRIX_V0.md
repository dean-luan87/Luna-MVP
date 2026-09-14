# LUNA Offline Mainline Regression Acceptance Matrix v0

## Phase

- Phase-EngineeringFlow-006 (Offline Mainline Regression Acceptance v0)

## Toolchain

- Runner: `tools/run_offline_mainline_regression_acceptance_v0.py`
- Verifier: `tools/verify_offline_mainline_regression_acceptance_v0.py`

## Regression objects

| Object | Normal | Fallback | Source |
|---|---:|---:|---|
| YOLO selected path | yolo_shadow × 3 | N/A | EF-005 comparison |
| Baseline/mock path | N/A | baseline_mock × 3 | EF-005 comparison |
| Five-stage chain completeness | 1.0 | 1.0 | EF-005 comparison + EF-004 summary |
| Schema validity | 1.0 | 1.0 | EF-004 summary |
| SceneContext gates presence | 1.0 | 1.0 | EF-004 stage_complete_rates.scene_context |
| Output no-real-TTS | 1.0 | 1.0 | EF-005 safety summary |
| No execute leakage | 1.0 | 1.0 | EF-005 safety summary |
| trace/replay/whitebox | present | present | EF-005 verifier |
| Observability integrity | all pass | all pass | EF-005 verifier |
| Evidence boundary | 1.0 | 1.0 | EF-005 evidence summary |

## Gate mapping (hard thresholds)

下列 gate **必须 pass**：

- chain_normal_complete_rate_1.0
- chain_fallback_complete_rate_1.0
- schema_all_stages_valid_1.0
- source_policy_normal_yolo_shadow_eq_3
- source_policy_fallback_baseline_mock_eq_3
- source_policy_fallback_count_eq_3
- scene_context_stage_complete_rate_1.0
- output_real_tts_invoked_false_rate_1.0
- output_allows_execute_now_false_rate_1.0
- observability_required_files_exist
- observability_verifier_all_pass
- observability_broken_refs_eq_0
- safety_*_eq_0（所有 safety leakage 计数项）
- evidence_*_eq_1.0（四项 rate）
- evidence_evidence_type_mutation_count_eq_0
- evidence_pending_closed_count_eq_0

