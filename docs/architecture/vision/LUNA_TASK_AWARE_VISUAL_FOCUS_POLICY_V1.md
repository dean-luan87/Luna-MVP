# Luna — Task-Aware Visual Focus Policy v1

**Phase**：`Phase-Task-Aware-Visual-Focus-Policy-v1-001`  
**性质**：policy / schema / contract / boundary only  
**边界**：不实现视觉 runtime，不调用视觉模型，不接 `camera`，不接 `OCR provider`，不接地图 API / 高德 API，不接 tracking runtime，不接 optical flow runtime，不调用 `Supervision / ByteTrack / OC-SORT`，不写 `Memory` / `WorldModel` / `Fact` / `Library`，不做 `entity resolution`，不做 `fact admission`，不做 `memory consolidation`，不做 `library experience commit`，不生成 `Scene Delta`，不提交 `Task State`，不触发 `Navigation Action`

## 阶段定位

本阶段的核心不是 tracking、不是模型、不是 OCR，而是把：

`MidPlatformPerceptionWorkOrder`  
↓  
`SceneSketchCandidate`  
↓  
`VisualFocusPlan`  
↓  
`VisualFocusSlot`  
↓  
`ViewQualityCandidate`  
↓  
`ActiveViewAdjustmentCandidate`  
↓  
`VisualObservationLifecycle`

这条链正式定义为视觉侧 policy / schema / contract。

本阶段回答：

1. 视觉侧如何消费 `MidPlatformPerceptionWorkOrder`
2. 如何根据任务阶段生成 `SceneSketchCandidate`
3. 如何从环境速写和任务目标生成 `VisualFocusPlan`
4. `VisualFocusSlot` 如何表达任务相关、安全相关、OCR相关、追踪相关、地图/记忆相关
5. 什么时候允许请求 `OCR activation`
6. 什么时候允许请求 `tracking candidate`
7. 什么时候需要主动视角调整
8. 什么时候因为视角质量不足而降级
9. 视觉观察如何进入 `active / stale / expired / archived_candidate` 生命周期
10. 视觉候选如何回传中台形成 `TaskFeedbackCandidate / SafetyFeedbackCandidate`
11. 如何继续保持 `WorldModel / Memory / Library` handoff-only，不吞治理写入

## 输入 roots

本阶段正式依赖：

- `_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0/`
- `_eval_out/return_to_vision_mainline_planning_v1_smoke_v0/`
- `_eval_out/return_to_vision_mainline_preplan_v1/`
- `_eval_out/ocr_mainline_final_closure_v1_smoke_v0/`
- `_eval_out/minimal_runtime_integration_closure_v1_smoke_v0/`

并引用：

- `docs/architecture/midplatform/LUNA_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_V1.md`
- `docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PLANNING_V1.md`
- `docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PREPLAN_V1.md`
- `docs/architecture/ocr/LUNA_OCR_MAINLINE_FINAL_CLOSURE_V1.md`
- `docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CLOSURE_V1.md`
- `docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md`

可选复用文档若不存在，只能标记 `optional_missing`，不得伪造能力。

## Core Object 1: SceneSketchCandidate

`SceneSketchCandidate` 是环境速写候选，它不是环境事实，也不是动作指令。

关键字段：

- `scene_sketch_id`
- `source_work_order_id`
- `source_frame_ref_placeholder`
- `task_context_ref`
- `location_context_ref`
- `pose_or_view_context_ref`
- `scene_type_candidate`
- `self_position_hint`
- `left_context`
- `right_context`
- `front_context`
- `far_context`
- `near_ground_context`
- `walkable_area_hint`
- `human_density_candidate`
- `vehicle_presence_candidate`
- `signage_or_text_hint`
- `obstacle_hint`
- `traffic_light_or_crossing_hint`
- `temporary_facility_hint`
- `visibility_quality_ref`
- `uncertainty`
- `freshness_status`
- `ttl_policy_ref`
- `privacy_tags`
- `fact_status=not_fact`
- `write_allowed=false`
- `source_chain`

必须明确：

- `SceneSketchCandidate` 不是环境事实
- 不直接播报
- 不直接写 `WorldModel`
- 不直接触发导航动作
- 它只是 `VisualFocusPlan` 的输入候选

## Core Object 2: VisualFocusPlan

`VisualFocusPlan` 是视觉焦点计划，是规划合同，不是执行。

关键字段：

- `visual_focus_plan_id`
- `source_work_order_id`
- `source_scene_sketch_id`
- `task_id`
- `task_type`
- `task_phase`
- `focus_slots`
- `ignored_by_default`
- `ocr_activation_slots`
- `tracking_request_slots`
- `map_memory_binding_slots`
- `safety_focus_slots`
- `active_view_adjustment_slots`
- `budget_policy_ref`
- `privacy_policy_ref`
- `freshness_policy_ref`
- `conflict_policy_ref`
- `output_handoff_policy_ref`
- `fact_status=not_fact`
- `runtime_action_allowed=false`
- `source_chain`

必须明确：

- `VisualFocusPlan` 不等于真实画面切割
- 不等于模型已执行
- 不等于 tracking 已执行
- 只是后续 `visual candidate / OCR activation / tracking candidate` 的规划合同

## Core Object 3: VisualFocusSlot

`VisualFocusSlot` 用来表达“具体要看什么、为什么看、允许看多深”。

关键字段：

- `slot_id`
- `source_visual_focus_plan_id`
- `slot_type`
- `target`
- `priority`
- `task_relevance`
- `safety_relevance`
- `route_relevance`
- `map_memory_relevance`
- `expected_evidence_type`
- `tracking_required`
- `ocr_required`
- `map_binding_required`
- `active_view_adjustment_allowed`
- `activation_condition`
- `expiration_condition`
- `max_budget`
- `stc_policy_ref`
- `ttl_policy_ref`
- `freshness_requirement`
- `privacy_filter_required`
- `output_allowed=false`
- `action_allowed=false`
- `fact_status=not_fact`
- `source_chain`

`slot_type` 至少覆盖：

- `safety_focus`
- `route_path_focus`
- `walkable_surface_focus`
- `route_alignment_focus`
- `crossing_focus`
- `traffic_light_focus`
- `dynamic_obstacle_focus`
- `pedestrian_flow_focus`
- `vehicle_flow_focus`
- `destination_landmark_focus`
- `shopfront_focus`
- `signage_focus`
- `doorway_or_entrance_focus`
- `support_surface_focus`
- `tabletop_focus`
- `shelf_or_counter_focus`
- `floor_near_user_focus`
- `readable_region_focus`
- `temporary_facility_focus`
- `user_feedback_focus`
- `world_observation_focus`

必须明确：

- `VisualFocusSlot` 不等于真实视觉执行
- 不等于直接用户指令
- 不得直接输出 action

## Core Object 4: ViewQualityCandidate

`ViewQualityCandidate` 是视角质量候选，不是事实层。

关键字段：

- `view_quality_id`
- `source_work_order_id`
- `source_frame_ref_placeholder`
- `blur_level_candidate`
- `brightness_quality_candidate`
- `exposure_quality_candidate`
- `occlusion_level_candidate`
- `camera_shake_candidate`
- `target_distance_quality_candidate`
- `dynamic_motion_quality_candidate`
- `crowd_occlusion_candidate`
- `reflection_or_weather_candidate`
- `frame_stability_candidate`
- `readable_region_quality_hint`
- `safe_for_scene_sketch`
- `safe_for_ocr_activation`
- `safe_for_tracking_request`
- `requires_active_view_adjustment`
- `recommended_degradation`
- `fact_status=not_fact`
- `source_chain`

必须定义降级策略：

- `GOOD`：允许生成 `SceneSketch` 和 `VisualFocusPlan`
- `DEGRADED`：只允许 `safety + primary task focus`
- `POOR`：只允许 `safety focus / active view adjustment candidate`
- `BLOCKED`：暂停任务视觉，只保留 `safety candidate`

## Core Object 5: ActiveViewAdjustmentCandidate

`ActiveViewAdjustmentCandidate` 是主动视角调整候选，不是直接命令。

关键字段：

- `active_view_adjustment_id`
- `source_focus_slot_id`
- `missing_visual_evidence`
- `suggested_view_adjustment`
- `adjustment_type`
- `urgency`
- `safety_constraint`
- `user_message_candidate`
- `speech_gate_required=true`
- `output_allowed=false until gate`
- `action_allowed=false`
- `fact_status=not_fact`
- `source_chain`

`adjustment_type` 可包括：

- `turn_left_slightly`
- `turn_right_slightly`
- `look_up`
- `look_down`
- `move_closer`
- `step_back`
- `hold_still`
- `center_target`
- `scan_right_side`
- `scan_left_side`
- `focus_on_tabletop`
- `focus_on_doorplate`
- `focus_on_shopfront`

必须明确：

- `ActiveViewAdjustmentCandidate` 只是用户引导候选
- 不直接控制用户行动
- 不直接播报
- 必须经过 `Speech Gate / Output boundary`

## Core Object 6: VisualObservationLifecyclePolicy

视觉候选生命周期冻结为：

- `active`
- `stale`
- `expired`
- `archived_candidate`
- `worldmodel_handoff_candidate`
- `rejected`
- `promoted_later_placeholder`

每一层都定义：

- `current_action_allowed`
- `task_feedback_allowed`
- `archive_allowed`
- `worldmodel_handoff_allowed_candidate`
- `memory_handoff_allowed_candidate`
- `library_handoff_placeholder_allowed`
- `ttl_required`
- `source_chain_required`
- `privacy_filter_required`

必须明确：

- 过期视觉信息可归档为历史候选，但不得作为当前行动依据
- `WorldModel / Memory / Library` 只允许 `handoff candidate / placeholder`

## Core Object 7: FocusToOCRActivationPolicy

允许：

- `readable_region_focus`
- `signage_focus`
- `shopfront_focus`
- `doorway_or_entrance_focus`
- `destination_landmark_focus`
- `traffic_light_focus` when countdown/sign text present
- `temporary_facility_focus` when text notice present

禁止：

- `full_frame_ocr`
- `low_quality_view_ocr`
- `non_task_relevant_background_text`
- `privacy_sensitive_text without filtering`
- 本阶段内的 `OCR provider runtime invocation`

必须明确：

- 本阶段只定义 `OCR activation request candidate`
- 不提交 `OCRRequest`
- 不调用 provider

## Core Object 8: FocusToTrackingRequestPolicy

允许：

- `safety_focus`
- `route_path_focus`
- `walkable_surface_focus`
- `dynamic_obstacle_focus`
- `traffic_light_focus`
- `pedestrian_flow_focus`
- `vehicle_flow_focus`
- `destination_landmark_focus`
- `user_feedback_focus`

禁止：

- `full_scene_tracking`
- `all_moving_objects_tracking`
- `all_person_tracking`
- `all_vehicle_tracking`
- `background_tracking_without_task_or_safety_relevance`
- 本阶段内的 `tracking runtime invocation`

必须明确：

- 本阶段只定义 `tracking request candidate`
- 不调用 tracking runtime

## Core Object 9: VisualFocusFeedbackPolicy

输出候选：

- `VisualFocusFeedbackCandidate`
- `SceneSketchFeedbackCandidate`
- `ViewQualityFeedbackCandidate`
- `ActiveViewAdjustmentFeedbackCandidate`
- `OCRActivationRequestCandidate`
- `TrackingRequestCandidate`
- `SafetyFocusFeedbackCandidate`
- `TaskFocusFeedbackCandidate`

原则：

- `feedback candidate` 不直接播报
- `speech_allowed=false until Speech Gate`
- `action_allowed=false`
- `fact_status=not_fact`
- `requires_arbitration=true`
- `source_chain required`

## Core Object 10: DeferredWorldModelMemoryLibraryBoundary

必须继承上一阶段边界：

- `entity_resolution_deferred=true`
- `fact_admission_deferred=true`
- `memory_consolidation_deferred=true`
- `library_experience_governance_deferred=true`
- `worldmodel_write_allowed=false`
- `memory_write_allowed=false`
- `library_write_allowed=false`
- `handoff_candidate_not_fact=true`
- `placeholder_not_runtime=true`

## Task Scenario Matrix

本阶段至少覆盖以下 8 个场景：

1. `navigation_route_walking`
2. `navigation_approaching_crossing`
3. `navigation_approaching_destination`
4. `shop_search_right_side_storefront`
5. `object_search_home_keys`
6. `home_familiar_object_interaction`
7. `low_quality_view_hold_still`
8. `crowded_path_occluded_surface`

这些场景正式回答：

- 任务 walking / crossing / destination 时的 focus slots
- 低质量视角时何时降级到 `POOR / BLOCKED`
- 如何保留 `safety focus` 同时压低任务视觉
- `OCR activation candidate` 与 `tracking request candidate` 何时允许存在
- `home familiar object interaction` 中如何只保留 placeholder / handoff，不提前写长期层

## Governance Debt Register

本阶段继续保持“先把主链堆起来，治理后置”的策略，但必须登记治理债务。

至少登记：

- `visual focus slot schema complexity`
- `view quality degradation complexity`
- `active view adjustment boundary complexity`
- `visual observation lifecycle complexity`
- `ocr activation request gating complexity`
- `tracking request gating complexity`
- `duplicated schema risk`
- `future midplatform function governance required`

结论：

- `future_midplatform_function_governance_required=true`
- `no_duplicate_governance_module_allowed=true`

## 输出目录

runner 输出目录：

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

## 最终结论

如果 verifier 为 `GO`，则本阶段最终决定应为：

- `TASK_AWARE_VISUAL_FOCUS_POLICY_READY_FOR_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY`

推荐下一阶段固定为：

- `Phase-World-Observation-and-Entity-Feature-Policy-v1-001`

注意：

- 本阶段完成后，视觉焦点 policy 成立
- 下一阶段进入 `World Observation / Entity Feature policy`
- 仍然不要接 runtime
- 仍然不要接 `camera / OCR provider / tracking / map API`
- 仍然不要写 `WorldModel / Memory / Fact / Library`

后续状态更新：

- `Phase-World-Observation-and-Entity-Feature-Policy-v1-001 = GO`
- `Phase-Selective-Tracking-Adapter-Policy-v1-001 = GO`
- 当前推荐下一阶段：`Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001`
