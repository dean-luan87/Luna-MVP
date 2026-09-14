# Luna Evaluation — Controlled Frame Input Post-DryRun Review v1

对应 phase：`Phase-Controlled-Frame-Input-Post-DryRun-Review-v1-001`

## 运行命令

```bash
python3 tools/evaluation/vision/run_controlled_frame_input_post_dryrun_review_v1.py
python3 tools/evaluation/vision/verify_controlled_frame_input_post_dryrun_review_v1.py
```

runner 默认输出目录：

- `_eval_out/controlled_frame_input_post_dryrun_review_v1_smoke_v0/`

## 必须输入

- `_eval_out/controlled_frame_input_dryrun_v1_smoke_v0/`
- `_eval_out/controlled_frame_input_planning_v1_smoke_v0/`
- `_eval_out/map_location_readonly_context_policy_v1_smoke_v0/`
- `_eval_out/post_vision_strengthening_roadmap_decision_v1_smoke_v0/`
- `_eval_out/basic_navigation_loop_vision_strengthening_closure_v1_smoke_v0/`
- `_eval_out/task_aware_visual_focus_policy_v1_smoke_v0/`
- `_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0/`
- `_eval_out/minimal_runtime_integration_closure_v1_smoke_v0/`
- `_eval_out/ocr_mainline_final_closure_v1_smoke_v0/`

如存在，也加载：

- Vision Frame Trace / Stream Registry 相关输出
- Vision Frame Input Governance 相关输出
- Vision ROI Proposal Stub 相关输出
- System Health / Hardware Profile 相关输出
- Simulation Lab profile 相关输出

可选 root 不存在时必须标记 `optional_missing`，不得失败，不得伪造能力。

## 必须输出

- `summary.json`
- `input_root_matrix.json`
- `controlled_frame_dryrun_input_root_review.json`
- `controlled_frame_scenario_coverage_review.json`
- `frame_intake_gate_review.json`
- `frame_quality_gate_review.json`
- `frame_privacy_tagging_review.json`
- `frame_stc_freshness_review.json`
- `frame_downstream_handoff_review.json`
- `dual_device_placeholder_review.json`
- `runtime_write_action_speech_boundary_review.json`
- `controlled_frame_input_closure_readiness_decision.json`
- `governance_debt_review.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## Verifier Pass Requirements

至少检查 180 项，baseline requirement = 140。

输入检查：

- `controlled_frame_input_dryrun_input_loaded=true`
- `controlled_frame_input_planning_input_loaded=true`
- `map_location_readonly_context_input_loaded=true`
- `post_vision_strengthening_roadmap_decision_input_loaded=true`
- `vision_strengthening_closure_input_loaded=true`
- `task_aware_visual_focus_input_loaded=true`
- `midplatform_perception_orchestration_input_loaded=true`
- `minimal_runtime_integration_closure_loaded=true`
- `ocr_final_closure_loaded=true`

review 产物检查：

- `input_root_review_generated=true`
- `scenario_coverage_review_generated=true`
- `frame_intake_gate_review_generated=true`
- `frame_quality_gate_review_generated=true`
- `frame_privacy_tagging_review_generated=true`
- `frame_stc_freshness_review_generated=true`
- `frame_downstream_handoff_review_generated=true`
- `dual_device_placeholder_review_generated=true`
- `runtime_write_action_speech_boundary_review_generated=true`
- `closure_readiness_decision_generated=true`
- `governance_debt_review_generated=true`

覆盖检查：

- `reviewed_scenario_count>=14`
- `accepted_candidate_count>=5`
- `rejected_candidate_count>=6`
- `restricted_candidate_count>=1`
- `stale_archive_only_candidate_count>=1`
- `source_chain_required_verified=true`
- `timestamp_required_verified=true`
- `privacy_tags_required_verified=true`
- `live_camera_blocked_verified=true`
- `device_camera_blocked_verified=true`
- `external_stream_blocked_verified=true`

handoff 边界检查：

- `frame_to_ocr_requires_visual_focus=true`
- `frame_to_tracking_requires_visual_focus=true`
- `frame_to_world_observation_requires_policy=true`
- `frame_to_navigation_action_allowed=false`
- `frame_to_speech_output_allowed=false`
- `frame_to_worldmodel_write_allowed=false`
- `frame_to_memory_write_allowed=false`
- `frame_to_fact_write_allowed=false`

dual-device placeholder 检查：

- `dual_device_redundant_perception_placeholder_loaded=true`
- `dual_device_runtime_allowed=false`
- `dual_model_runtime_allowed=false`
- `failover_runtime_allowed=false`
- `automatic_hardware_switch_allowed=false`
- `multi_input_fusion_runtime_allowed=false`
- `hardware_stage_deferred=true`

runtime / write / action / speech 检查：

- `no_runtime_boundary_pass=true`
- `no_write_boundary_pass=true`
- `no_action_boundary_pass=true`
- `no_speech_boundary_pass=true`
- `no_runtime_executed=true`
- `no_new_runtime_enabled=true`
- `frame_content_loaded=false`
- `actual_image_read=false`
- `camera_invoked=false`
- `camera_opened=false`
- `video_capture_invoked=false`
- `visual_model_invoked=false`
- `map_api_invoked=false`
- `gaode_api_invoked=false`
- `gps_runtime_invoked=false`
- `ocr_provider_invoked=false`
- `ocrrequest_submitted=false`
- `tracking_runtime_invoked=false`
- `optical_flow_runtime_invoked=false`
- `supervision_invoked=false`
- `bytetrack_invoked=false`
- `ocsort_invoked=false`
- `dual_device_runtime_invoked=false`
- `dual_model_runtime_invoked=false`
- `failover_runtime_invoked=false`
- `multi_input_fusion_runtime_invoked=false`
- `speech_gate_invoked=false`
- `vop_invoked=false`
- `tts_invoked=false`
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

governance debt 检查：

- `governance_debt_review_generated=true`
- `future_midplatform_function_governance_required=true`
- `no_duplicate_governance_module_allowed=true`

readiness 检查：

- `final_decision=CONTROLLED_FRAME_INPUT_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`
- `recommended_next_phase=Phase-Controlled-Frame-Input-Closure-v1-001`
