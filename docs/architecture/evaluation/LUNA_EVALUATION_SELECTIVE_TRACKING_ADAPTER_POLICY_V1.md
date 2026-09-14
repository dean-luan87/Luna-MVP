# Luna — Evaluation: Selective Tracking Adapter Policy v1

```bash
python3 tools/evaluation/vision/run_selective_tracking_adapter_policy_v1.py \
  --workspace-root /Users/luanlei/Desktop/Luna-Workspace-Min \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/selective_tracking_adapter_policy_v1_smoke_v0 \
  --world-observation-entity-feature-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/world_observation_and_entity_feature_policy_v1_smoke_v0 \
  --task-aware-visual-focus-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/task_aware_visual_focus_policy_v1_smoke_v0 \
  --midplatform-perception-orchestration-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0 \
  --return-to-vision-planning-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/return_to_vision_mainline_planning_v1_smoke_v0 \
  --preplan-input-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/return_to_vision_mainline_preplan_v1 \
  --ocr-final-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_mainline_final_closure_v1_smoke_v0 \
  --minimal-runtime-integration-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/minimal_runtime_integration_closure_v1_smoke_v0

python3 tools/evaluation/vision/verify_selective_tracking_adapter_policy_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/selective_tracking_adapter_policy_v1_smoke_v0
```

## 目标

验证 `Phase-Selective-Tracking-Adapter-Policy-v1-001` 是否已经正式冻结：

- `SelectiveTrackingAdapterPolicy`
- `TrackingRequestCandidate`
- `TrackletCandidate`
- `TrackingBudgetPolicy`
- `TrackingTargetAdmissionPolicy`
- `RoadSurfaceTrackingPolicy`
- `PedestrianVehicleTrackingPolicy`
- `CrowdFlowTrackingPolicy`
- `TrafficLightAndCrossingTrackingPolicy`
- `TrackingAdapterCandidateRegistry`
- `TrackingLifecyclePolicy`
- `TrackingFeedbackPolicy`

## 产物要求

输出目录：

- `_eval_out/selective_tracking_adapter_policy_v1_smoke_v0/`

必须包含：

- `summary.json`
- `input_root_matrix.json`
- `selective_tracking_adapter_policy.json`
- `tracking_request_candidate_schema.json`
- `tracklet_candidate_schema.json`
- `tracking_budget_policy.json`
- `tracking_target_admission_policy.json`
- `road_surface_tracking_policy.json`
- `pedestrian_vehicle_tracking_policy.json`
- `crowd_flow_tracking_policy.json`
- `traffic_light_crossing_tracking_policy.json`
- `tracking_adapter_candidate_registry.json`
- `tracking_lifecycle_policy.json`
- `tracking_feedback_policy.json`
- `selective_tracking_scenario_matrix.json`
- `selective_tracking_boundary_matrix.json`
- `governance_debt_register.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## 通过要求

至少确认：

- `policy_scope=selective_tracking_adapter_policy_only`
- `world_observation_entity_feature_input_loaded=true`
- `task_aware_visual_focus_input_loaded=true`
- `midplatform_perception_orchestration_input_loaded=true`
- `return_to_vision_planning_input_loaded=true`
- `preplan_input_loaded=true`
- `selective_tracking_adapter_policy_defined=true`
- `tracking_request_candidate_schema_defined=true`
- `tracklet_candidate_schema_defined=true`
- `tracking_budget_policy_defined=true`
- `tracking_target_admission_policy_defined=true`
- `road_surface_tracking_policy_defined=true`
- `pedestrian_vehicle_tracking_policy_defined=true`
- `crowd_flow_tracking_policy_defined=true`
- `traffic_light_crossing_tracking_policy_defined=true`
- `tracking_adapter_candidate_registry_defined=true`
- `tracking_lifecycle_policy_defined=true`
- `tracking_feedback_policy_defined=true`
- `scenario_matrix_generated=true`
- `scenario_count>=10`
- `tracking_authority_owner=MidPlatform`
- `full_scene_tracking_allowed=false`
- `all_moving_objects_tracking_allowed=false`
- `all_person_tracking_allowed=false`
- `all_vehicle_tracking_allowed=false`
- `crowd_flow_follow_action_allowed=false`
- `traffic_light_crossing_action_allowed=false`
- `tracking_request_candidate_only=true`
- `tracklet_candidate_not_fact=true`
- `external_tracking_adapters_future_candidate_only=true`

## WorldModel / Memory / Library Boundary

必须继续保持：

- `worldmodel_handoff_candidate_allowed=true`
- `memory_handoff_candidate_allowed=true`
- `library_handoff_placeholder_allowed=true`
- `entity_resolution_deferred=true`
- `fact_admission_deferred=true`
- `memory_consolidation_deferred=true`
- `library_experience_governance_deferred=true`
- `worldmodel_write_allowed=false`
- `memory_write_allowed=false`
- `library_write_allowed=false`
- `handoff_candidate_not_fact=true`
- `placeholder_not_runtime=true`

## Runtime / Write Boundary

本阶段必须继续保持：

- `no_runtime_executed=true`
- `no_new_runtime_enabled=true`
- `tracking_runtime_enabled=false`
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
- `sort_invoked=false`
- `botsort_invoked=false`
- `entity_resolution_runtime_invoked=false`
- `fact_admission_runtime_invoked=false`
- `memory_consolidation_invoked=false`
- `library_experience_commit_invoked=false`
- `world_model_written=false`
- `memory_written=false`
- `library_written=false`
- `fact_written=false`
- `scene_delta_generated=false`
- `task_state_committed_now=false`
- `navigation_action_triggered=false`
- `speech_gate_invoked=false`
- `vop_invoked=false`
- `boundary_ok=true`
- `violations=[]`

## 场景矩阵要求

至少覆盖：

- `route_surface_tracking_candidate`
- `near_field_obstacle_tracking_candidate`
- `pedestrian_approach_safety_candidate`
- `vehicle_approach_safety_candidate`
- `crowded_path_occluded_surface`
- `traffic_light_state_tracking_candidate`
- `shopfront_tracking_for_target_confirmation`
- `temporary_facility_tracking_candidate`
- `user_feedback_target_tracking_candidate`
- `low_value_background_tracking_rejected`

## 最终目标

如果 verifier 为 `GO`，则说明 Luna 已正式完成 Selective Tracking Adapter Policy，下一阶段应切入：

- `Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001`
