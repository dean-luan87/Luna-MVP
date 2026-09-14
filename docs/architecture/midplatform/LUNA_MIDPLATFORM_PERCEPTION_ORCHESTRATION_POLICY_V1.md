# Luna — MidPlatform Perception Orchestration Policy v1

**Phase**：`Phase-MidPlatform-Perception-Orchestration-Policy-v1-001`  
**性质**：policy / schema / contract / boundary only  
**边界**：不实现 runtime，不接视觉模型，不接 `camera`，不接 `OCR provider`，不接地图 API / 高德 API，不接 tracking runtime，不接 optical flow runtime，不写 `Memory` / `WorldModel` / `Fact` / `Library`，不做 `entity resolution`，不做 `fact admission`，不做 `memory consolidation`，不做 `library experience commit`，不生成 `Scene Delta`，不提交 `Task State`，不触发 `Navigation Action`

## 阶段定位

本阶段用于冻结 Luna 视角强化主线中的“中台感知编排 policy”。目标不是马上做功能治理合并，而是先把中台编排主链堆起来：

- 中台如何作为感知总调度层
- 中台如何根据任务阶段生成 `MidPlatformPerceptionWorkOrder`
- `Safety Lane` 和 `Task Lane` 如何被中台编排
- OCR 何时允许被激活
- tracking 何时允许被请求
- 地图 / 路线 / 位置 / 记忆如何只作为 context hint
- 资源预算如何归中台管理
- 隐私过滤如何归中台处理
- 视觉 / OCR / 地图 / 记忆 / 用户反馈冲突如何形成 correction / conflict candidate
- `WorldModel / Memory / Library` 如何继续保持 handoff-only / placeholder-only
- 下一阶段 `Phase-Task-Aware-Visual-Focus-Policy-v1-001` 应接收什么输入

当前策略明确为：

1. 先把中台能力堆起来
2. 完成感知编排主链
3. 完成视觉 / OCR / 地图 / 记忆 / 任务反馈的中台调度
4. 再单独做 `MidPlatform Function Governance / Consolidation`

因此本阶段必须保留 `reuse / duplicate / governance debt` 记录，但**不**在这里提前做功能治理合并。

## 输入 roots

本阶段正式依赖：

- `_eval_out/return_to_vision_mainline_planning_v1_smoke_v0/`
- `_eval_out/return_to_vision_mainline_preplan_v1/`
- `_eval_out/ocr_mainline_final_closure_v1_smoke_v0/`
- `_eval_out/minimal_runtime_integration_closure_v1_smoke_v0/`

并引用：

- `docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PLANNING_V1.md`
- `docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PREPLAN_V1.md`
- `docs/architecture/ocr/LUNA_OCR_MAINLINE_FINAL_CLOSURE_V1.md`
- `docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CLOSURE_V1.md`
- `docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md`

可选复用文档若不存在，只能标记 `optional_missing`，不得伪造能力。

## Core Object 1: MidPlatformPerceptionWorkOrder

`MidPlatformPerceptionWorkOrder` 是本阶段核心对象。它是中台感知工作单，是调度候选，不是 runtime 执行。

关键字段：

- `work_order_id`
- `related_task_id`
- `task_type`
- `task_phase`
- `priority`
- `perception_time_window`
- `safety_lane_required`
- `task_lane_required`
- `scene_context_ref`
- `map_context_ref`
- `route_context_ref`
- `location_context_ref`
- `memory_context_ref`
- `system_health_ref`
- `hardware_state_ref`
- `focus_request_targets`
- `ocr_activation_request`
- `tracking_request`
- `map_memory_hint_request`
- `world_observation_handoff_allowed`
- `privacy_filtering_required`
- `resource_budget_ref`
- `freshness_policy_ref`
- `stc_policy_ref`
- `conflict_policy_ref`
- `output_handoff_policy_ref`
- `runtime_action_allowed=false`
- `task_commit_allowed=false`
- `fact_write_allowed=false`
- `worldmodel_write_allowed=false`
- `memory_write_allowed=false`
- `library_write_allowed=false`
- `source_chain`

必须明确：

- `PerceptionWorkOrder` 不能直接触发 `camera / OCR / tracking / map API`
- 它只能作为后续 `visual focus / OCR / tracking / feedback dry-run` 的输入合同
- 它不等于真实感知执行

## Core Object 2: TaskPhasePerceptionPolicy

`TaskPhasePerceptionPolicy` 用来回答“不同任务阶段应该看什么、允许什么、禁止什么”。

本阶段至少冻结以下 phase：

### Navigation

- `ROUTE_START`
- `ROUTE_WALKING`
- `APPROACHING_CROSSING`
- `CROSSING_DECISION`
- `APPROACHING_TARGET`
- `TARGET_SEARCH`
- `TARGET_CONFIRMATION`
- `ARRIVED_CANDIDATE`
- `SAFETY_HOLD`

### Shop Search

- `SEARCH_AREA_APPROACHING`
- `SHOPFRONT_SCAN`
- `SIGNAGE_CONFIRMATION`
- `ENTRANCE_CONFIRMATION`
- `TARGET_FOUND_CANDIDATE`

### Object Search

- `SEARCH_CONTEXT_IDENTIFICATION`
- `LIKELY_SURFACE_SCAN`
- `OBJECT_CANDIDATE_CONFIRMATION`
- `OBJECT_LOCATION_GUIDANCE`

### Extended Task Types

- `reading_task`
- `queue_or_crowd_observation`
- `target_confirmation`
- `user_visual_feedback_response`

每个 `task_phase` 必须定义：

- `required_focus_targets`
- `optional_focus_targets`
- `safety_lane_policy`
- `task_lane_policy`
- `ocr_activation_policy`
- `tracking_policy`
- `map_memory_hint_policy`
- `output_policy`
- `handoff_boundary`
- `forbidden_runtime_actions`

## Core Object 3: SafetyLaneOrchestrationPolicy

`Safety Lane` 必须被冻结为：

- `always_on=true`
- 不受普通 `task` 禁用
- 只生成 `SafetyObservationCandidate`
- 不直接行动
- 必须进入 `Safety-Task Arbitration`
- 可抢占 `Task Lane budget`
- 保留 `P0 / P1 priority`
- 可请求 `view quality / active adjustment candidate`
- 不写事实

覆盖目标：

- `near_field_obstacle`
- `moving_vehicle`
- `pedestrian_approach`
- `bike_or_e_scooter`
- `traffic_light`
- `crosswalk`
- `curb_or_step`
- `pothole_or_ground_risk`
- `walkable_path_interruption`
- `sudden_dynamic_risk`

## Core Object 4: TaskLaneOrchestrationPolicy

`Task Lane` 必须被冻结为：

- `task-dependent`
- 只处理中台批准的 `focus targets`
- 受资源预算控制
- 不允许 `full-scene tracking`
- 不允许 `full-frame OCR`
- 不允许绕过 `Safety Lane`
- 输出 `TaskObservationCandidate / TaskFeedbackCandidate`
- 必须进入 `Safety-Task Arbitration` 或后续 `Speech Gate` 前置链
- 不直接行动
- 不写事实

覆盖任务类别：

- `navigation`
- `shop_search`
- `object_search`
- `reading_task`
- `queue_or_crowd_observation`
- `target_confirmation`
- `user_visual_feedback_response`

## Core Object 5: MidPlatformResourceBudgetPolicy

资源预算归中台。

关键字段：

- `budget_policy_id`
- `hardware_state_ref`
- `system_health_ref`
- `task_priority_ref`
- `safety_reserved_budget`
- `primary_task_budget`
- `secondary_task_budget`
- `background_world_observation_budget`
- `ocr_budget`
- `tracking_budget`
- `map_memory_query_budget`
- `max_active_focus_slots`
- `max_active_tracklets`
- `max_ocr_requests_per_window`
- `max_background_observation_items`
- `degradation_policy`
- `preemption_policy`
- `source_chain`

核心原则：

- `P0 Safety budget` 永远保留
- 主任务优先于附加任务
- 附加任务不得挤占安全链
- 后台 `World Observation` 只能低频运行
- `OCR / tracking / map query` 均需受中台预算控制
- 视觉模块不能自行扩展追踪数量
- 资源不足时降级为 `safety-first + primary-task-only`
- `hardware/system health` 不足时，中台可关闭后台观察、降低 OCR、降低 tracking 频率

## Core Object 6: MidPlatformPrivacyFilteringPolicy

隐私过滤归中台信息处理阶段。

候选阶段：

- `Raw Observation Candidate`
- `Privacy-Filtered Candidate`
- `Restricted Use Candidate`
- `Long-Term Eligible Candidate`

隐私标签：

- `human_identity_sensitive`
- `face_visible`
- `license_plate_visible`
- `private_space_candidate`
- `medical_context_candidate`
- `school_or_child_context_candidate`
- `home_context_candidate`
- `workplace_context_candidate`
- `commercial_sensitive_candidate`
- `personal_item_candidate`
- `bystander_presence_candidate`

核心原则：

- 采集阶段不直接等于可用
- 可用不等于可存
- 可存不等于可写 `WorldModel`
- 可写候选不等于事实
- 陌生人 / 车牌 / 私人空间默认限制使用
- 用户相关对象 / 地点 / 关系可在授权与治理后进入长期候选
- 隐私过滤应由中台统一执行，不由视觉模块自行判断

## Core Object 7: PerceptionConflictCorrectionPolicy

冲突来源：

- `visual_vs_ocr`
- `visual_vs_map`
- `visual_vs_memory`
- `visual_vs_user_feedback`
- `ocr_vs_actual_function`
- `signboard_vs_business_function`
- `map_poi_vs_current_scene`
- `historical_observation_vs_current_observation`
- `temporary_facility_vs_static_poi`
- `fresh_vs_stale_conflict`

输出候选：

- `PerceptionConflictCandidate`
- `PerceptionCorrectionCandidate`
- `RealityMismatchCandidate`
- `WorldModelCorrectionHandoffCandidate`

核心原则：

- 冲突不等于自动修正
- 用户反馈也先是 `correction candidate`
- 多次观察一致后才可进入 `WorldModel correction handoff`
- 对当前导航安全有影响时，可生成 `safety/task feedback candidate`
- 对长期信息有价值时，进入 `review / memory / worldmodel governance`
- 当前阶段不写事实

## Core Object 8: MapMemoryContextHintPolicy

允许：

- 提供目标接近 hint
- 提供路线阶段 hint
- 提供方向 / 左右侧 / 入口 / 路口 / POI hint
- 提供历史混淆点
- 提供过去观察候选
- 提供下次观察优先级

禁止：

- 直接触发行动
- 直接播报为事实
- 覆盖实时安全视觉
- 直接写 `WorldModel / Memory / Fact`
- 直接触发 `OCR / tracking runtime`
- 直接判定到达

核心原则：

- `map / route / location / memory` 仍然只是 `context hint`
- `realtime safety visual` 优先于历史 hint

## Core Object 9: WorldModelMemoryLibraryHandoffBoundary

本阶段必须把上一阶段边界前置到中台编排目标。

当前只允许：

- `WorldModelHandoffCandidate`
- `MemoryHandoffCandidate`
- `LibraryHandoffPlaceholder`
- `ExperienceCandidatePlaceholder`

禁止：

- `entity_resolution_runtime`
- `fact_admission`
- `worldmodel_write`
- `memory_write`
- `library_experience_commit`
- `memory_consolidation`
- `object_identity_fact_commit`
- `emotional_attachment_fact_commit`
- `temporary_facility_long_term_promotion`
- `route_experience_commit`

必须保留字段：

- `entity_resolution_deferred=true`
- `fact_admission_deferred=true`
- `memory_consolidation_deferred=true`
- `library_experience_governance_deferred=true`
- `worldmodel_write_allowed=false`
- `memory_write_allowed=false`
- `library_write_allowed=false`
- `handoff_candidate_not_fact=true`
- `placeholder_not_runtime=true`

## Core Object 10: PerceptionFeedbackCandidatePolicy

输出候选：

- `SafetyFeedbackCandidate`
- `TaskFeedbackCandidate`
- `ViewAdjustmentFeedbackCandidate`
- `OCRActivationFeedbackCandidate`
- `MapMemoryConflictFeedbackCandidate`
- `UserVisualFeedbackCandidate`

核心原则：

- `feedback candidate` 不直接播报
- `speech_allowed=false until Speech Gate`
- `action_allowed=false`
- `fact_status=not_fact`
- `requires_arbitration=true`
- `source_chain required`

## Governance Debt Register

本阶段明确承认，为了推进速度，先把关键中台能力堆起来，但必须留下治理债务记录，后续统一收束。

必须记录：

- `resource budget complexity`
- `privacy filtering complexity`
- `conflict correction complexity`
- `temporary facility governance complexity`
- `world observation handoff complexity`
- `duplicated schema risk`
- `future midplatform function governance required`

结论：

- 当前 `future_midplatform_function_governance_required=true`
- 当前 `no_duplicate_governance_module_allowed=true`
- 先完成主链，再做 `MidPlatform Function Governance / Consolidation`

## 输出目录

runner 输出目录：

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

## 最终结论

如果 verifier 为 `GO`，则本阶段最终决定应为：

- `MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY`

推荐下一阶段固定为：

- `Phase-Task-Aware-Visual-Focus-Policy-v1-001`

注意：

- 本阶段完成后，中台感知编排 policy 成立
- 下一阶段进入 `Task-Aware Visual Focus Policy`
- 仍然不要接 runtime
- 仍然不要接 tracking / camera / OCR provider / map API
- 仍然不要写 `WorldModel / Memory / Fact / Library`
- 中台功能先堆起来，完成一轮后再单独开 `MidPlatform Function Governance / Consolidation phase`

后续状态更新：

- `Phase-Task-Aware-Visual-Focus-Policy-v1-001 = GO`
- `Phase-World-Observation-and-Entity-Feature-Policy-v1-001 = GO`
- 当前推荐下一阶段：`Phase-Selective-Tracking-Adapter-Policy-v1-001`
