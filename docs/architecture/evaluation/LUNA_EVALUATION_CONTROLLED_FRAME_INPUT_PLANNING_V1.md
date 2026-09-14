# Luna Evaluation — Controlled Frame Input Planning v1

对应 phase：`Phase-Controlled-Frame-Input-Planning-v1-001`

## 运行命令

```bash
python3 tools/evaluation/vision/run_controlled_frame_input_planning_v1.py
python3 tools/evaluation/vision/verify_controlled_frame_input_planning_v1.py
```

runner 默认输出目录：

- `_eval_out/controlled_frame_input_planning_v1_smoke_v0/`

## 必须输入

- `_eval_out/map_location_readonly_context_policy_v1_smoke_v0/`
- `_eval_out/post_vision_strengthening_roadmap_decision_v1_smoke_v0/`
- `_eval_out/basic_navigation_loop_vision_strengthening_closure_v1_smoke_v0/`
- `_eval_out/visual_ocr_map_task_feedback_dryrun_v1_smoke_v0/`
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
- `controlled_frame_input_planning_policy.json`
- `frame_source_candidate_schema.json`
- `controlled_frame_input_candidate_schema.json`
- `frame_intake_gate_policy.json`
- `frame_quality_gate_policy.json`
- `frame_privacy_tagging_policy.json`
- `frame_stc_freshness_policy.json`
- `frame_downstream_handoff_policy.json`
- `dual_device_redundant_perception_placeholder.json`
- `controlled_frame_input_readiness_gate.json`
- `controlled_frame_input_planning_scenario_matrix.json`
- `controlled_frame_input_boundary_matrix.json`
- `governance_debt_register.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## Verifier Pass Requirements

至少检查 170 项，baseline requirement = 130。

输入检查：

- `map_location_readonly_context_input_loaded=true`
- `post_vision_strengthening_roadmap_decision_input_loaded=true`
- `vision_strengthening_closure_input_loaded=true`
- `task_aware_visual_focus_input_loaded=true`
- `midplatform_perception_orchestration_input_loaded=true`
- `minimal_runtime_integration_closure_loaded=true`
- `ocr_final_closure_loaded=true`

schema / policy 检查：

- `controlled_frame_input_planning_policy_defined=true`
- `frame_source_candidate_schema_defined=true`
- `controlled_frame_input_candidate_schema_defined=true`
- `frame_intake_gate_policy_defined=true`
- `frame_quality_gate_policy_defined=true`
- `frame_privacy_tagging_policy_defined=true`
- `frame_stc_freshness_policy_defined=true`
- `frame_downstream_handoff_policy_defined=true`
- `controlled_frame_input_readiness_gate_generated=true`
- `dual_device_redundant_perception_placeholder_defined=true`
- `perception_input_channel_placeholder_defined=true`
- `perception_device_health_placeholder_defined=true`
- `perception_lane_failover_placeholder_defined=true`
- `dual_input_consistency_placeholder_defined=true`

场景检查：

- `scenario_matrix_generated=true`
- `scenario_count>=10`
- `static_test_image_allowed_for_schema_test` exists
- `pre_recorded_video_frame_allowed_for_controlled_dryrun` exists
- `simulation_frame_allowed_for_sim_lab` exists
- `uploaded_frame_requires_privacy_tags` exists
- `live_camera_placeholder_blocked_now` exists
- `external_stream_placeholder_blocked_now` exists
- `low_quality_frame_degraded` exists
- `privacy_sensitive_home_frame_restricted` exists
- `stale_frame_archive_candidate_only` exists
- `frame_to_ocr_requires_visual_focus` exists

边界检查：

- `live_camera_allowed=false`
- `device_camera_allowed=false`
- `external_stream_allowed=false`
- `dual_device_runtime_allowed=false`
- `dual_model_runtime_allowed=false`
- `failover_runtime_allowed=false`
- `automatic_hardware_switch_allowed=false`
- `hardware_stage_deferred=true`
- `frame_to_ocr_requires_visual_focus=true`
- `frame_to_tracking_requires_visual_focus=true`
- `frame_to_world_observation_requires_policy=true`
- `frame_to_navigation_action_allowed=false`
- `frame_to_speech_output_allowed=false`
- `frame_to_worldmodel_write_allowed=false`
- `frame_to_memory_write_allowed=false`
- `frame_to_fact_write_allowed=false`
- `privacy_tags_required_for_downstream=true`
- `source_chain_required=true`
- `timestamp_required=true`
- `stc_freshness_reuse_required=true`

runtime / write / action / speech 检查：

- `no_runtime_executed=true`
- `no_new_runtime_enabled=true`
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

- `governance_debt_register_generated=true`
- `future_midplatform_function_governance_required=true`
- `no_duplicate_governance_module_allowed=true`

readiness 检查：

- `final_decision=CONTROLLED_FRAME_INPUT_PLANNING_READY_FOR_CONTROLLED_FRAME_INPUT_DRYRUN`
- `recommended_next_phase=Phase-Controlled-Frame-Input-DryRun-v1-001`
