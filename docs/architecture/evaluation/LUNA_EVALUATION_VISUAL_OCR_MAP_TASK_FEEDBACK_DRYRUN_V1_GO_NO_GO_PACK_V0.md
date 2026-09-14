# Luna — GO / NO_GO Pack: Visual OCR Map Task Feedback DryRun v1

## GO 条件

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
- `dryrun_only=true`
- `no_runtime_executed=true`
- `no_new_runtime_enabled=true`
- `supervision_imported=false`
- `supervision_invoked=false`
- `bytetrack_imported=false`
- `bytetrack_invoked=false`
- `ocsort_imported=false`
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
- `tts_invoked=false`
- `boundary_ok=true`
- `future_midplatform_function_governance_required=true`
- `no_duplicate_governance_module_allowed=true`
- `final_decision=VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN_READY_FOR_BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING`
- `recommended_next_phase=Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001`

## NO_GO 条件

- 未加载 `Selective Tracking Adapter Policy`
- 未加载 `World Observation and Entity Feature Policy`
- 未加载 `Task-Aware Visual Focus Policy`
- 未加载 `MidPlatform Perception Orchestration Policy`
- 未加载 `Return-To-Vision Mainline Planning`
- 未加载 `preplan`
- 未定义 dry-run case / fusion / task / safety / OCR / tracking / map-memory / conflict / view-adjustment / boundary schema
- 场景矩阵少于 10 个
- 未生成 dry-run 结果
- 未生成多类 feedback candidate
- 建议本阶段直接提交 `OCRRequest`
- 建议本阶段直接调用 `OCR provider / tracking runtime / map API`
- 建议本阶段直接调用 `Supervision / ByteTrack / OC-SORT`
- 建议本阶段直接触发导航动作
- 建议本阶段直接写 `WorldModel / Memory / Fact / Library`
- 未记录 `governance debt`
- 未固定下一阶段

## 判定语义

### GO

说明视觉 / OCR / 地图 / 记忆 / tracking candidate / 任务反馈 dry-run 链已经成立，可以继续切入：

- `Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001`

### NO_GO

说明当前仍停留在 feedback dry-run review，必须先补齐 schema、scenario matrix、dry-run results、boundary 或治理债务登记。

## 明确边界

即使 `GO`，本阶段也 **不等于**：

- 已接 `camera`
- 已接 `OCR provider`
- 已提交 `OCRRequest`
- 已接 tracking runtime
- 已接 `map API`
- 已调用 `Supervision / ByteTrack / OC-SORT`
- 已调用 `Speech Gate / VOP / TTS`
- 已执行 `entity resolution / fact admission / memory consolidation`
- 已写入 `WorldModel / Memory / Fact / Library`
- 已触发真实导航动作

本阶段 `GO` 只表示：

- 多条上游 policy 首次在中台层通过 dry-run 串联起来
- `visual / OCR activation / tracking / map-memory hint / world observation` 能形成 feedback candidate
- 整条链继续保持 `candidate-only / no-runtime / no-write / no-fact`
