# Luna — Evaluation: MidPlatform Perception Orchestration Policy v1

```bash
python3 tools/evaluation/midplatform/run_midplatform_perception_orchestration_policy_v1.py \
  --workspace-root /Users/luanlei/Desktop/Luna-Workspace-Min \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0 \
  --return-to-vision-planning-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/return_to_vision_mainline_planning_v1_smoke_v0 \
  --preplan-input-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/return_to_vision_mainline_preplan_v1 \
  --ocr-final-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_mainline_final_closure_v1_smoke_v0 \
  --minimal-runtime-integration-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/minimal_runtime_integration_closure_v1_smoke_v0

python3 tools/evaluation/midplatform/verify_midplatform_perception_orchestration_policy_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0
```

## 目标

验证 `Phase-MidPlatform-Perception-Orchestration-Policy-v1-001` 是否已经正式冻结：

- `MidPlatformPerceptionWorkOrder`
- `TaskPhasePerceptionPolicy`
- `SafetyLaneOrchestrationPolicy`
- `TaskLaneOrchestrationPolicy`
- `MidPlatformResourceBudgetPolicy`
- `MidPlatformPrivacyFilteringPolicy`
- `PerceptionConflictCorrectionPolicy`
- `MapMemoryContextHintPolicy`
- `WorldModelMemoryLibraryHandoffBoundary`
- `PerceptionFeedbackCandidatePolicy`
- `GovernanceDebtRegister`

## 产物要求

输出目录：

- `_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0/`

必须包含：

- `summary.json`
- `input_root_matrix.json`
- `perception_work_order_schema.json`
- `task_phase_perception_policy_matrix.json`
- `safety_lane_orchestration_policy.json`
- `task_lane_orchestration_policy.json`
- `midplatform_resource_budget_policy.json`
- `midplatform_privacy_filtering_policy.json`
- `perception_conflict_correction_policy.json`
- `map_memory_context_hint_policy.json`
- `worldmodel_memory_library_handoff_boundary.json`
- `perception_feedback_candidate_policy.json`
- `orchestration_boundary_matrix.json`
- `governance_debt_register.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## 通过要求

至少确认：

- `policy_scope=midplatform_perception_orchestration_policy_only`
- `return_to_vision_planning_input_loaded=true`
- `preplan_input_loaded=true`
- `ocr_final_closure_loaded=true`
- `minimal_runtime_integration_closure_loaded=true`
- `perception_work_order_schema_defined=true`
- `task_phase_perception_policy_defined=true`
- `safety_lane_orchestration_defined=true`
- `task_lane_orchestration_defined=true`
- `midplatform_resource_budget_policy_defined=true`
- `midplatform_privacy_filtering_policy_defined=true`
- `perception_conflict_correction_policy_defined=true`
- `map_memory_context_hint_policy_defined=true`
- `worldmodel_memory_library_handoff_boundary_defined=true`
- `perception_feedback_candidate_policy_defined=true`
- `governance_debt_register_generated=true`
- `resource_budget_owned_by_midplatform=true`
- `privacy_filtering_owned_by_midplatform=true`
- `safety_lane_always_on=true`
- `task_lane_task_dependent=true`
- `full_scene_tracking_allowed=false`
- `full_frame_ocr_allowed=false`
- `map_memory_context_hint_only=true`
- `worldmodel_handoff_candidate_allowed=true`
- `memory_handoff_candidate_allowed=true`
- `library_handoff_placeholder_allowed=true`

## WorldModel / Memory / Library Boundary

必须继续保持：

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
- `camera_invoked=false`
- `map_api_invoked=false`
- `ocr_provider_invoked=false`
- `tracking_runtime_invoked=false`
- `optical_flow_runtime_invoked=false`
- `world_model_written=false`
- `memory_written=false`
- `library_written=false`
- `fact_written=false`
- `scene_delta_generated=false`
- `task_state_committed_now=false`
- `navigation_action_triggered=false`
- `boundary_ok=true`
- `violations=[]`

## 最终目标

如果 verifier 为 `GO`，则说明 Luna 已正式完成中台感知编排 policy，下一阶段应切入：

- `Phase-Task-Aware-Visual-Focus-Policy-v1-001`
