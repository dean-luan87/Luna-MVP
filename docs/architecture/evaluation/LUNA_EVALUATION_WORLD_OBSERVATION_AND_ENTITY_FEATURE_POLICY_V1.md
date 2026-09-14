# Luna — Evaluation: World Observation and Entity Feature Policy v1

```bash
python3 tools/evaluation/vision/run_world_observation_and_entity_feature_policy_v1.py \
  --workspace-root /Users/luanlei/Desktop/Luna-Workspace-Min \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/world_observation_and_entity_feature_policy_v1_smoke_v0 \
  --task-aware-visual-focus-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/task_aware_visual_focus_policy_v1_smoke_v0 \
  --midplatform-perception-orchestration-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0 \
  --return-to-vision-planning-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/return_to_vision_mainline_planning_v1_smoke_v0 \
  --preplan-input-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/return_to_vision_mainline_preplan_v1 \
  --ocr-final-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_mainline_final_closure_v1_smoke_v0 \
  --minimal-runtime-integration-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/minimal_runtime_integration_closure_v1_smoke_v0

python3 tools/evaluation/vision/verify_world_observation_and_entity_feature_policy_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/world_observation_and_entity_feature_policy_v1_smoke_v0
```

## 目标

验证 `Phase-World-Observation-and-Entity-Feature-Policy-v1-001` 是否已经正式冻结：

- `WorldObservationLayerPolicy`
- `WorldObservationCandidate`
- `WorldObservationValueFilteringPolicy`
- `WorldEntityFeatureCandidate`
- `ObjectIdentityCandidate`
- `TemporaryMobileSocialFacilityPolicy`
- `EmotionalAttachmentCandidatePolicy`
- `WorldModelMemoryLibraryPlaceholderPolicy`
- `WorldObservationFeedbackPolicy`
- `WorldObservationEntityFeatureScenarioMatrix`

## 产物要求

输出目录：

- `_eval_out/world_observation_and_entity_feature_policy_v1_smoke_v0/`

必须包含：

- `summary.json`
- `input_root_matrix.json`
- `world_observation_layer_policy.json`
- `world_observation_candidate_schema.json`
- `world_observation_value_filtering_policy.json`
- `world_entity_feature_candidate_schema.json`
- `object_identity_candidate_schema.json`
- `temporary_mobile_social_facility_policy.json`
- `emotional_attachment_candidate_policy.json`
- `worldmodel_memory_library_placeholder_policy.json`
- `world_observation_feedback_policy.json`
- `world_observation_entity_feature_scenario_matrix.json`
- `world_observation_boundary_matrix.json`
- `governance_debt_register.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## 通过要求

至少确认：

- `policy_scope=world_observation_and_entity_feature_policy_only`
- `task_aware_visual_focus_input_loaded=true`
- `midplatform_perception_orchestration_input_loaded=true`
- `return_to_vision_planning_input_loaded=true`
- `preplan_input_loaded=true`
- `world_observation_layer_policy_defined=true`
- `world_observation_candidate_schema_defined=true`
- `world_observation_value_filtering_policy_defined=true`
- `world_entity_feature_candidate_schema_defined=true`
- `object_identity_candidate_schema_defined=true`
- `temporary_mobile_social_facility_policy_defined=true`
- `emotional_attachment_candidate_policy_defined=true`
- `worldmodel_memory_library_placeholder_policy_defined=true`
- `world_observation_feedback_policy_defined=true`
- `scenario_matrix_generated=true`
- `scenario_count>=8`
- `full_background_recording_allowed=false`
- `world_observation_runtime_enabled=false`
- `object_identity_fact_allowed=false`
- `emotional_attachment_fact_allowed=false`
- `fixed_poi_commit_allowed=false`

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
- `world_observation_runtime_enabled=false`
- `camera_invoked=false`
- `map_api_invoked=false`
- `ocr_provider_invoked=false`
- `ocrrequest_submitted=false`
- `tracking_runtime_invoked=false`
- `optical_flow_runtime_invoked=false`
- `supervision_invoked=false`
- `bytetrack_invoked=false`
- `ocsort_invoked=false`
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

- `route_structure_observation`
- `shopfront_entity_feature_candidate`
- `home_familiar_object_candidate`
- `temporary_mobile_vendor_candidate`
- `recurring_temporary_pattern_candidate`
- `emotional_attachment_candidate_placeholder`
- `scene_change_candidate`
- `low_value_background_discard`

## 最终目标

如果 verifier 为 `GO`，则说明 Luna 已正式完成后台世界观察与实体特征候选 policy，下一阶段应切入：

- `Phase-Selective-Tracking-Adapter-Policy-v1-001`
