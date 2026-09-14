# Luna Evaluation — Basic Navigation Loop Vision Strengthening Post-DryRun Review v1

对应 phase：`Phase-Basic-Navigation-Loop-Vision-Strengthening-Post-DryRun-Review-v1-001`

## 运行命令

```bash
python3 tools/evaluation/midplatform/run_basic_navigation_loop_vision_strengthening_post_dryrun_review_v1.py
python3 tools/evaluation/midplatform/verify_basic_navigation_loop_vision_strengthening_post_dryrun_review_v1.py
```

runner 默认输出目录：

- `_eval_out/basic_navigation_loop_vision_strengthening_post_dryrun_review_v1_smoke_v0/`

## 必须输入

- `_eval_out/basic_navigation_loop_vision_strengthening_dryrun_v1_smoke_v0/`
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

- `basic_navigation_guidance_loop_dryrun_v1`
- `navigation_guidance_speech_adapter_v1`
- `voice_interruption_governance_dryrun_v1`
- `voice_command_ownership_gate_policy_v1`
- text-only output closure / post-trial review 相关产物

可选 root 不存在时必须标记 `optional_missing`，不得失败，不得伪造能力。

## 必须输出

- `summary.json`
- `input_root_matrix.json`
- `dryrun_input_root_review.json`
- `scenario_coverage_review.json`
- `guidance_candidate_review.json`
- `safety_arbitration_bridge_review.json`
- `text_only_dry_output_review.json`
- `high_risk_scenario_review.json`
- `worldmodel_memory_library_boundary_review.json`
- `runtime_write_action_speech_boundary_review.json`
- `governance_debt_review.json`
- `closure_readiness_decision.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## Verifier Pass Requirements

至少检查 180 项，baseline requirement = 140。

硬性检查：

- `dryrun_input_loaded=true`
- 所有 required upstream inputs loaded 为 `true`
- 10 份 review / decision 产物全部生成
- `reviewed_scenario_count>=12`
- `reviewed_guidance_candidate_count>=12`
- `reviewed_output_candidate_count>=12`
- `candidate_only_boundary_pass=true`
- `safety_priority_review_pass=true`
- `high_risk_conservative_handling_pass=true`
- `text_only_dry_output_boundary_pass=true`
- `worldmodel_memory_library_boundary_pass=true`
- `no_runtime_boundary_pass=true`
- `no_write_boundary_pass=true`
- `no_action_boundary_pass=true`
- `no_speech_boundary_pass=true`
- `governance_debt_recorded=true`
- `future_midplatform_function_governance_required=true`
- `no_duplicate_governance_module_allowed=true`

runtime / write / action / speech 边界：

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

ready / no-go：

- `final_decision=BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`
- `recommended_next_phase=Phase-Basic-Navigation-Loop-Vision-Strengthening-Closure-v1-001`

## 语义说明

本阶段 `GO` 仅表示：

- dry-run 闭环已经完成正式审查
- 可以进入本轮视角强化的 closure

不表示：

- 已开放真实 runtime
- 已允许真实导航 / OCR / tracking / map API / speech 输出
