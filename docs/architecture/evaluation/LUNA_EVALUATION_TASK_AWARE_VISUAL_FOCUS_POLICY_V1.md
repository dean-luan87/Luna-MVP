# Luna — Evaluation: Task-Aware Visual Focus Policy v1

```bash
python3 tools/evaluation/vision/run_task_aware_visual_focus_policy_v1.py \
  --workspace-root /Users/luanlei/Desktop/Luna-Workspace-Min \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/task_aware_visual_focus_policy_v1_smoke_v0 \
  --midplatform-perception-orchestration-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0 \
  --return-to-vision-planning-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/return_to_vision_mainline_planning_v1_smoke_v0 \
  --preplan-input-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/return_to_vision_mainline_preplan_v1 \
  --ocr-final-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_mainline_final_closure_v1_smoke_v0 \
  --minimal-runtime-integration-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/minimal_runtime_integration_closure_v1_smoke_v0

python3 tools/evaluation/vision/verify_task_aware_visual_focus_policy_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/task_aware_visual_focus_policy_v1_smoke_v0
```

## 目标

验证 `Phase-Task-Aware-Visual-Focus-Policy-v1-001` 是否已经正式冻结：

- `SceneSketchCandidate`
- `VisualFocusPlan`
- `VisualFocusSlot`
- `ViewQualityCandidate`
- `ActiveViewAdjustmentCandidate`
- `VisualObservationLifecyclePolicy`
- `FocusToOCRActivationPolicy`
- `FocusToTrackingRequestPolicy`
- `VisualFocusFeedbackPolicy`
- `DeferredWorldModelMemoryLibraryBoundary`
- `TaskAwareVisualFocusScenarioMatrix`

## 产物要求

输出目录：

- `_eval_out/task_aware_visual_focus_policy_v1_smoke_v0/`

必须包含：

- `summary.json`
- `input_root_matrix.json`
- `scene_sketch_candidate_schema.json`
- `visual_focus_plan_schema.json`
- `visual_focus_slot_schema.json`
- `view_quality_candidate_schema.json`
- `active_view_adjustment_candidate_schema.json`
- `visual_observation_lifecycle_policy.json`
- `focus_to_ocr_activation_policy.json`
- `focus_to_tracking_request_policy.json`
- `visual_focus_feedback_policy.json`
- `deferred_worldmodel_memory_library_boundary.json`
- `task_aware_visual_focus_scenario_matrix.json`
- `visual_focus_boundary_matrix.json`
- `governance_debt_register.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## 通过要求

至少确认：

- `policy_scope=task_aware_visual_focus_policy_only`
- `midplatform_perception_orchestration_input_loaded=true`
- `return_to_vision_planning_input_loaded=true`
- `preplan_input_loaded=true`
- `scene_sketch_candidate_schema_defined=true`
- `visual_focus_plan_schema_defined=true`
- `visual_focus_slot_schema_defined=true`
- `view_quality_candidate_schema_defined=true`
- `active_view_adjustment_candidate_schema_defined=true`
- `visual_observation_lifecycle_policy_defined=true`
- `focus_to_ocr_activation_policy_defined=true`
- `focus_to_tracking_request_policy_defined=true`
- `visual_focus_feedback_policy_defined=true`
- `scenario_matrix_generated=true`
- `scenario_count>=8`
- `safety_focus_slots_defined=true`
- `task_focus_slots_defined=true`
- `view_quality_degradation_policy_defined=true`
- `active_view_adjustment_policy_defined=true`
- `ocr_activation_request_candidate_only=true`
- `tracking_request_candidate_only=true`
- `full_frame_ocr_allowed=false`
- `full_scene_tracking_allowed=false`

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
- `camera_invoked=false`
- `map_api_invoked=false`
- `ocr_provider_invoked=false`
- `ocrrequest_submitted=false`
- `tracking_runtime_invoked=false`
- `optical_flow_runtime_invoked=false`
- `supervision_invoked=false`
- `bytetrack_invoked=false`
- `ocsort_invoked=false`
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

## 最终目标

如果 verifier 为 `GO`，则说明 Luna 已正式完成任务感知视觉焦点 policy，下一阶段应切入：

- `Phase-World-Observation-and-Entity-Feature-Policy-v1-001`
