# Luna Evaluation — Map / Location Read-Only Context Policy v1

对应 phase：`Phase-Map-Location-ReadOnly-Context-Policy-v1-001`

## 运行命令

```bash
python3 tools/evaluation/midplatform/run_map_location_readonly_context_policy_v1.py
python3 tools/evaluation/midplatform/verify_map_location_readonly_context_policy_v1.py
```

runner 默认输出目录：

- `_eval_out/map_location_readonly_context_policy_v1_smoke_v0/`

## 必须输入

- `_eval_out/post_vision_strengthening_roadmap_decision_v1_smoke_v0/`
- `_eval_out/basic_navigation_loop_vision_strengthening_closure_v1_smoke_v0/`
- `_eval_out/basic_navigation_loop_vision_strengthening_post_dryrun_review_v1_smoke_v0/`
- `_eval_out/basic_navigation_loop_vision_strengthening_dryrun_v1_smoke_v0/`
- `_eval_out/visual_ocr_map_task_feedback_dryrun_v1_smoke_v0/`
- `_eval_out/selective_tracking_adapter_policy_v1_smoke_v0/`
- `_eval_out/world_observation_and_entity_feature_policy_v1_smoke_v0/`
- `_eval_out/task_aware_visual_focus_policy_v1_smoke_v0/`
- `_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0/`
- `_eval_out/minimal_runtime_integration_closure_v1_smoke_v0/`
- `_eval_out/ocr_mainline_final_closure_v1_smoke_v0/`

如存在，也加载：

- existing `MapAnchor / GPS / Route context` outputs
- basic navigation guidance loop outputs
- safety task arbitration outputs
- route or map preplan outputs

可选 root 不存在时必须标记 `optional_missing`，不得失败，不得伪造能力。

## 必须输出

- `summary.json`
- `input_root_matrix.json`
- `map_location_readonly_context_policy.json`
- `map_location_context_candidate_schema.json`
- `route_stage_hint_candidate_schema.json`
- `target_proximity_hint_candidate_schema.json`
- `side_orientation_hint_candidate_schema.json`
- `entrance_intersection_hint_candidate_schema.json`
- `map_visual_memory_conflict_policy.json`
- `map_location_to_visual_focus_binding_policy.json`
- `map_location_to_ocr_activation_hint_policy.json`
- `map_location_feedback_policy.json`
- `map_location_readonly_context_scenario_matrix.json`
- `map_location_boundary_matrix.json`
- `governance_debt_register.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## Verifier Pass Requirements

至少检查 180 项，baseline requirement = 140。

输入检查：

- `post_vision_strengthening_roadmap_decision_input_loaded=true`
- `vision_strengthening_closure_input_loaded=true`
- `visual_ocr_map_task_feedback_input_loaded=true`
- `task_aware_visual_focus_input_loaded=true`
- `midplatform_perception_orchestration_input_loaded=true`
- `minimal_runtime_integration_closure_loaded=true`
- `ocr_final_closure_loaded=true`

schema / policy 检查：

- `map_location_readonly_context_policy_defined=true`
- `map_location_context_candidate_schema_defined=true`
- `route_stage_hint_candidate_schema_defined=true`
- `target_proximity_hint_candidate_schema_defined=true`
- `side_orientation_hint_candidate_schema_defined=true`
- `entrance_intersection_hint_candidate_schema_defined=true`
- `map_visual_memory_conflict_policy_defined=true`
- `map_location_to_visual_focus_binding_policy_defined=true`
- `map_location_to_ocr_activation_hint_policy_defined=true`
- `map_location_feedback_policy_defined=true`

场景检查：

- `scenario_matrix_generated=true`
- `scenario_count>=10`
- `route_walking_map_hint` exists
- `approaching_destination_nearby` exists
- `right_side_shop_search` exists
- `intersection_approach_hint` exists
- `entrance_hint_candidate` exists
- `off_route_uncertain_hint` exists
- `map_visual_conflict_shop_absent` exists
- `stale_map_or_old_poi` exists
- `indoor_floor_directory_hint` exists
- `gps_low_confidence_location_uncertain` exists

只读语义检查：

- `map_context_role=readonly_hint`
- `location_context_role=readonly_hint`
- `route_context_role=readonly_hint`
- `poi_context_role=readonly_hint`
- `map_is_fact_authority=false`
- `map_is_navigation_authority=false`
- `map_is_safety_authority=false`
- `map_can_trigger_action=false`
- `map_can_prove_arrival=false`
- `map_can_grant_crossing_permission=false`
- `map_can_write_worldmodel=false`
- `map_can_write_memory=false`
- `map_can_write_fact=false`
- `map_location_feedback_candidate_only=true`

联动边界检查：

- `ocr_activation_from_map_requires_visual_focus=true`
- `tracking_request_from_map_requires_visual_focus=true`
- `crossing_action_instruction_allowed=false`
- `arrival_fact_written=false`

runtime / write / action / speech 检查：

- `no_runtime_executed=true`
- `no_new_runtime_enabled=true`
- `map_api_invoked=false`
- `gaode_api_invoked=false`
- `gps_runtime_invoked=false`
- `route_planning_runtime_invoked=false`
- `camera_invoked=false`
- `visual_model_invoked=false`
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

- `final_decision=MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING`
- `recommended_next_phase=Phase-Controlled-Frame-Input-Planning-v1-001`
