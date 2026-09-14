# Luna Evaluation — Basic Navigation Loop Vision Strengthening DryRun v1

对应 phase：`Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001`

## 运行命令

```bash
python3 tools/evaluation/midplatform/run_basic_navigation_loop_vision_strengthening_dryrun_v1.py
python3 tools/evaluation/midplatform/verify_basic_navigation_loop_vision_strengthening_dryrun_v1.py
```

runner 默认输出目录：

- `_eval_out/basic_navigation_loop_vision_strengthening_dryrun_v1_smoke_v0/`

## 必须输入

- `_eval_out/visual_ocr_map_task_feedback_dryrun_v1_smoke_v0/`
- `_eval_out/selective_tracking_adapter_policy_v1_smoke_v0/`
- `_eval_out/world_observation_and_entity_feature_policy_v1_smoke_v0/`
- `_eval_out/task_aware_visual_focus_policy_v1_smoke_v0/`
- `_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0/`
- `_eval_out/basic_navigation_guidance_loop_stabilization_test_v1_smoke_v0/`
- `_eval_out/safety_task_arbitration_policy_v1_smoke_v0/`
- `_eval_out/minimal_runtime_integration_closure_v1_smoke_v0/`
- `_eval_out/ocr_mainline_final_closure_v1_smoke_v0/`

如存在，也加载：

- `_eval_out/basic_navigation_guidance_loop_dryrun_v1_smoke_v0/`
- `_eval_out/navigation_guidance_speech_adapter_v1_smoke_v0/`
- `_eval_out/voice_interruption_governance_dryrun_v1_smoke_v0/`
- `_eval_out/voice_command_ownership_gate_policy_v1_smoke_v0/`
- `_eval_out/minimal_runtime_integration_text_only_output_post_trial_review_v1_smoke_v0/`

可选输入不存在时必须标记 `optional_missing`，不得失败，不得伪造能力。

## 必须输出

- `summary.json`
- `input_root_matrix.json`
- `navigation_vision_strengthening_dryrun_case_schema.json`
- `navigation_feedback_intake_candidate_schema.json`
- `vision_aware_navigation_guidance_candidate_schema.json`
- `navigation_safety_arbitration_bridge_candidate_schema.json`
- `navigation_output_candidate_dryrun_schema.json`
- `navigation_vision_strengthening_boundary_decision_schema.json`
- `navigation_loop_vision_strengthening_scenario_matrix.json`
- `navigation_loop_vision_strengthening_dryrun_results.json`
- `navigation_loop_vision_strengthening_boundary_matrix.json`
- `governance_debt_register.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## Verifier Pass Requirements

至少检查 220 项，baseline requirement = 180。

硬性检查：

- required input loaded 全为 `true`
- 6 个核心 schema 全部定义
- `scenario_matrix_generated=true`
- `scenario_count>=12`
- 12 个指定场景全部存在
- `dryrun_results_generated=true`
- `guidance_candidate_count>=12`
- `output_candidate_count>=12`
- `safety_priority_cases_generated=true`
- `task_guidance_cases_generated=true`
- `active_view_adjustment_cases_generated=true`
- `ocr_later_needed_cases_generated=true`
- `tracking_later_needed_cases_generated=true`
- `map_visual_conflict_cases_generated=true`
- `crossing_uncertain_cases_generated=true`

候选边界：

- `feedback_candidates_require_arbitration=true`
- `speech_allowed_false_until_gate=true`
- `action_allowed_false=true`
- `navigation_action_allowed=false`
- `fact_status_not_fact=true`
- `ocrrequest_submission_allowed=false`
- `ocr_provider_allowed=false`
- `tracking_runtime_allowed=false`
- `crossing_action_instruction_allowed=false`
- `crowd_flow_follow_action_allowed=false`
- `fixed_poi_commit_allowed=false`
- `identity_fact_allowed=false`

`WorldModel / Memory / Library` 边界：

- `entity_resolution_deferred=true`
- `fact_admission_deferred=true`
- `memory_consolidation_deferred=true`
- `library_experience_governance_deferred=true`
- `worldmodel_write_allowed=false`
- `memory_write_allowed=false`
- `library_write_allowed=false`
- `handoff_candidate_not_fact=true`
- `placeholder_not_runtime=true`

runtime / write / speech / action 边界：

- `dryrun_only=true`
- `no_runtime_executed=true`
- `no_new_runtime_enabled=true`
- `camera_invoked=false`
- `map_api_invoked=false`
- `ocr_provider_invoked=false`
- `ocrrequest_submitted=false`
- `tracking_runtime_invoked=false`
- `optical_flow_runtime_invoked=false`
- `supervision_imported=false`
- `supervision_invoked=false`
- `bytetrack_imported=false`
- `bytetrack_invoked=false`
- `ocsort_imported=false`
- `ocsort_invoked=false`
- `safety_task_arbitration_runtime_invoked=false`
- `speech_gate_invoked=false`
- `vop_invoked=false`
- `tts_invoked=false`
- `user_heard_assumed=false`
- `task_state_committed_now=false`
- `navigation_action_triggered=false`
- `route_modified=false`
- `scene_delta_generated=false`
- `world_model_written=false`
- `memory_written=false`
- `library_written=false`
- `fact_written=false`
- `entity_resolution_runtime_invoked=false`
- `fact_admission_runtime_invoked=false`
- `memory_consolidation_invoked=false`
- `library_experience_commit_invoked=false`
- `boundary_ok=true`
- `violations=[]`

governance debt：

- `governance_debt_register_generated=true`
- `future_midplatform_function_governance_required=true`
- `no_duplicate_governance_module_allowed=true`

## Ready / No-Go

通过时：

- `verdict=GO`
- `final_decision=BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Basic-Navigation-Loop-Vision-Strengthening-Post-DryRun-Review-v1-001`

未通过时：

- 不得把本阶段表述为 runtime-ready
- 不得跳过 `Post-DryRun Review`
