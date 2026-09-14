# Luna — GO / NO_GO Pack: MidPlatform Perception Orchestration Policy v1

## GO 条件

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
- `world_model_written=false`
- `memory_written=false`
- `library_written=false`
- `fact_written=false`
- `scene_delta_generated=false`
- `task_state_committed_now=false`
- `navigation_action_triggered=false`
- `boundary_ok=true`
- `future_midplatform_function_governance_required=true`
- `no_duplicate_governance_module_allowed=true`
- `final_decision=MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY`
- `recommended_next_phase=Phase-Task-Aware-Visual-Focus-Policy-v1-001`

## NO_GO 条件

- 未加载 `Return-To-Vision Mainline Planning`
- 未加载 `preplan`
- 未加载 `OCR final closure`
- 未加载 `Minimal Runtime Integration closure`
- 未定义 `MidPlatformPerceptionWorkOrder`
- 未定义 `TaskPhasePerceptionPolicy`
- 未定义 `Safety Lane / Task Lane` 编排
- 未定义资源预算或隐私过滤中台归属
- 未保留 `WorldModel / Memory / Library` handoff-only 边界
- 建议在当前 phase 内启用 runtime / tracking / OCR provider / map API
- 建议在当前 phase 内执行 `entity resolution / fact admission / memory consolidation / library experience commit`
- 未记录 `governance debt`
- 未固定下一阶段

## 判定语义

### GO

说明中台感知编排主链已经正式成立，可以继续切入：

- `Phase-Task-Aware-Visual-Focus-Policy-v1-001`

### NO_GO

说明当前仍停留在 policy review，必须先补齐 schema、phase matrix、boundary、governance debt 或 handoff-only 约束。

## 明确边界

即使 `GO`，本阶段也 **不等于**：

- 已接 `camera`
- 已接 `OCR provider`
- 已接 `tracking runtime`
- 已接 `map API`
- 已启用视觉 runtime
- 已写入 `WorldModel / Memory / Fact / Library`
- 已执行 `entity resolution`
- 已执行 `fact admission`
- 已执行 `memory consolidation`
- 已完成 `MidPlatform Function Governance / Consolidation`

本阶段 `GO` 只表示：

- 中台感知编排 policy 已冻结
- 感知工作单与 task phase 输入合同已冻结
- 资源预算 / 隐私过滤 / 冲突修正 / handoff 边界已纳入中台
- 为了推进速度先堆中台能力，但治理债务已被正式登记
