# Luna — GO / NO_GO Pack: Task-Aware Visual Focus Policy v1

## GO 条件

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
- `no_runtime_executed=true`
- `no_new_runtime_enabled=true`
- `ocrrequest_submitted=false`
- `tracking_runtime_invoked=false`
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
- `future_midplatform_function_governance_required=true`
- `no_duplicate_governance_module_allowed=true`
- `final_decision=TASK_AWARE_VISUAL_FOCUS_POLICY_READY_FOR_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY`
- `recommended_next_phase=Phase-World-Observation-and-Entity-Feature-Policy-v1-001`

## NO_GO 条件

- 未加载 `MidPlatform Perception Orchestration Policy`
- 未加载 `Return-To-Vision Mainline Planning`
- 未加载 `preplan`
- 未定义 `SceneSketchCandidate / VisualFocusPlan / VisualFocusSlot`
- 未定义 `ViewQualityCandidate / ActiveViewAdjustmentCandidate`
- 未定义 `VisualObservationLifecyclePolicy`
- 未定义 `FocusToOCRActivationPolicy / FocusToTrackingRequestPolicy`
- 未定义 `WorldModel / Memory / Library` handoff-only 边界
- 建议本阶段直接接 `camera / OCR provider / tracking / map API`
- 建议本阶段直接提交 `OCRRequest`
- 建议本阶段调用 `Supervision / ByteTrack / OC-SORT`
- 建议本阶段直接写 `WorldModel / Memory / Fact / Library`
- 未记录 `governance debt`
- 未固定下一阶段

## 判定语义

### GO

说明视觉焦点主链已经正式成立，可以继续切入：

- `Phase-World-Observation-and-Entity-Feature-Policy-v1-001`

### NO_GO

说明当前仍停留在 visual focus policy review，必须先补齐 schema、scenario matrix、boundary、request gating 或治理债务登记。

## 明确边界

即使 `GO`，本阶段也 **不等于**：

- 已接 `camera`
- 已接 `OCR provider`
- 已接 `tracking runtime`
- 已接 `map API`
- 已提交 `OCRRequest`
- 已执行 `Supervision / ByteTrack / OC-SORT`
- 已写入 `WorldModel / Memory / Fact / Library`
- 已执行 `entity resolution / fact admission / memory consolidation`
- 已经存在真实用户动作指令

本阶段 `GO` 只表示：

- 任务感知视觉焦点 policy 已冻结
- `SceneSketch → FocusPlan → FocusSlot → ViewQuality → ActiveViewAdjustment → Lifecycle` 链已定义
- `OCR / tracking` 仍然只是 request candidate
- `WorldModel / Memory / Library` 继续保持 handoff-only / placeholder-only
