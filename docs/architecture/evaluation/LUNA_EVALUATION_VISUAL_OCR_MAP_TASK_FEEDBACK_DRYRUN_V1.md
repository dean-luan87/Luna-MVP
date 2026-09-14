# Luna — Evaluation: Visual OCR Map Task Feedback DryRun v1

```bash
python3 tools/evaluation/vision/run_visual_ocr_map_task_feedback_dryrun_v1.py \
  --workspace-root /Users/luanlei/Desktop/Luna-Workspace-Min \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/visual_ocr_map_task_feedback_dryrun_v1_smoke_v0 \
  --selective-tracking-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/selective_tracking_adapter_policy_v1_smoke_v0 \
  --world-observation-entity-feature-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/world_observation_and_entity_feature_policy_v1_smoke_v0 \
  --task-aware-visual-focus-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/task_aware_visual_focus_policy_v1_smoke_v0 \
  --midplatform-perception-orchestration-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0 \
  --return-to-vision-planning-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/return_to_vision_mainline_planning_v1_smoke_v0 \
  --preplan-input-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/return_to_vision_mainline_preplan_v1 \
  --ocr-final-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_mainline_final_closure_v1_smoke_v0 \
  --minimal-runtime-integration-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/minimal_runtime_integration_closure_v1_smoke_v0

python3 tools/evaluation/vision/verify_visual_ocr_map_task_feedback_dryrun_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/visual_ocr_map_task_feedback_dryrun_v1_smoke_v0
```

## 目标

验证 `Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001` 是否已经正式形成：

- `VisualOcrMapTaskFeedbackDryRunCase`
- `FeedbackFusionCandidate`
- `TaskFeedbackCandidate`
- `SafetyFeedbackCandidate`
- `OCRActivationFeedbackCandidate`
- `TrackingFeedbackCandidate`
- `MapMemoryContextFeedbackCandidate`
- `ConflictCorrectionFeedbackCandidate`
- `ActiveViewAdjustmentFeedbackCandidate`
- `DryRunBoundaryDecision`

## 产物要求

输出目录：

- `_eval_out/visual_ocr_map_task_feedback_dryrun_v1_smoke_v0/`

必须包含：

- `summary.json`
- `input_root_matrix.json`
- `dryrun_case_schema.json`
- `feedback_fusion_candidate_schema.json`
- `task_feedback_candidate_schema.json`
- `safety_feedback_candidate_schema.json`
- `ocr_activation_feedback_candidate_schema.json`
- `tracking_feedback_candidate_schema.json`
- `map_memory_context_feedback_candidate_schema.json`
- `conflict_correction_feedback_candidate_schema.json`
- `active_view_adjustment_feedback_candidate_schema.json`
- `dryrun_boundary_decision_schema.json`
- `visual_ocr_map_task_feedback_scenario_matrix.json`
- `visual_ocr_map_task_feedback_dryrun_results.json`
- `feedback_boundary_matrix.json`
- `governance_debt_register.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## 通过要求

至少确认：

- `dryrun_scope=visual_ocr_map_task_feedback_dryrun_only`
- `selective_tracking_input_loaded=true`
- `world_observation_entity_feature_input_loaded=true`
- `task_aware_visual_focus_input_loaded=true`
- `midplatform_perception_orchestration_input_loaded=true`
- `return_to_vision_planning_input_loaded=true`
- `preplan_input_loaded=true`
- `dryrun_case_schema_defined=true`
- `feedback_fusion_candidate_schema_defined=true`
- `task_feedback_candidate_schema_defined=true`
- `safety_feedback_candidate_schema_defined=true`
- `ocr_activation_feedback_candidate_schema_defined=true`
- `tracking_feedback_candidate_schema_defined=true`
- `map_memory_context_feedback_candidate_schema_defined=true`
- `conflict_correction_feedback_candidate_schema_defined=true`
- `active_view_adjustment_feedback_candidate_schema_defined=true`
- `dryrun_boundary_decision_schema_defined=true`
- `scenario_matrix_generated=true`
- `scenario_count>=10`
- `dryrun_results_generated=true`
- `feedback_candidate_count>=10`
- `task_feedback_candidate_generated=true`
- `safety_feedback_candidate_generated=true`
- `ocr_activation_feedback_candidate_generated=true`
- `tracking_feedback_candidate_generated=true`
- `map_memory_context_feedback_candidate_generated=true`
- `conflict_correction_feedback_candidate_generated=true`
- `active_view_adjustment_feedback_candidate_generated=true`

## 候选边界

必须继续保持：

- `feedback_candidates_require_arbitration=true`
- `speech_allowed_false_until_gate=true`
- `action_allowed_false=true`
- `fact_status_not_fact=true`
- `ocrrequest_submission_allowed=false`
- `ocr_provider_allowed=false`
- `tracking_runtime_allowed=false`
- `crossing_action_instruction_allowed=false`
- `crowd_flow_follow_action_allowed=false`
- `fixed_poi_commit_allowed=false`
- `identity_fact_allowed=false`

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
- `tts_invoked=false`
- `boundary_ok=true`
- `violations=[]`

## 场景矩阵要求

至少覆盖：

- `navigation_route_walking_clear_path`
- `navigation_approaching_destination_with_signage`
- `shop_search_right_side_storefront`
- `object_search_home_keys`
- `home_familiar_object_interaction`
- `crowded_path_occluded_surface`
- `crossing_uncertain_traffic_light`
- `temporary_mobile_vendor_near_route`
- `visual_map_memory_conflict`
- `low_quality_view_requires_hold_still`

## 最终目标

如果 verifier 为 `GO`，则说明 Luna 已正式完成视觉 / OCR / 地图 / 记忆 / tracking candidate / 任务反馈 dry-run 链，下一阶段应切入：

- `Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001`
