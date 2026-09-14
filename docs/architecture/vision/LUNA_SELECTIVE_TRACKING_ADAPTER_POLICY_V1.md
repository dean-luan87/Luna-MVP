# Luna — Selective Tracking Adapter Policy v1

**Phase**：`Phase-Selective-Tracking-Adapter-Policy-v1-001`  
**性质**：policy / schema / contract / boundary only  
**边界**：不实现 tracking runtime，不调用 `Supervision`，不调用 `ByteTrack`，不调用 `OC-SORT`，不调用 `optical flow runtime`，不调用视觉模型，不接 `camera`，不接 `OCR provider`，不接地图 API / 高德 API，不提交 `OCRRequest`，不写 `Memory` / `WorldModel` / `Fact` / `Library`，不做 `entity resolution`，不做 `fact admission`，不做 `memory consolidation`，不做 `library experience commit`，不生成 `Scene Delta`，不提交 `Task State`，不触发 `Navigation Action`

## 阶段定位

本阶段正式定义 Luna 视角强化主线中的“选择性追踪适配器 policy”。它承接：

`MidPlatformPerceptionWorkOrder`  
↓  
`VisualFocusPlan / VisualFocusSlot`  
↓  
`WorldObservationCandidate / WorldEntityFeatureCandidate`

并继续冻结：

`SelectiveTrackingAdapterPolicy`  
↓  
`TrackingRequestCandidate`  
↓  
`TrackletCandidate`  
↓  
`TrackingFeedbackCandidate / Handoff Candidate`

本阶段回答：

1. Luna 为什么不能 `full-scene tracking`。
2. 谁有权决定是否追踪。
3. 哪些 `VisualFocusSlot` 可以请求 tracking。
4. `TrackingRequestCandidate` 的准入条件是什么。
5. `TrackletCandidate` 如何保持 `candidate-only`。
6. tracking budget 如何由中台控制。
7. `road / route surface / pedestrian / vehicle / crowd flow` 如何作为不同追踪策略。
8. 当路面被遮挡时，`crowd flow` 如何只作为 `fallback candidate`。
9. `Supervision / ByteTrack / OC-SORT / optical flow` 如何只作为 `future adapter candidate`。
10. tracking 结果如何进入 `feedback / arbitration / handoff`，而不是直接导航。
11. tracking 信息过期后如何进入 `lifecycle / archive candidate`。
12. 如何继续保持 `no-runtime / no-write / no-fact` 边界。

## 输入 roots

本阶段正式依赖：

- `_eval_out/world_observation_and_entity_feature_policy_v1_smoke_v0/`
- `_eval_out/task_aware_visual_focus_policy_v1_smoke_v0/`
- `_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0/`
- `_eval_out/return_to_vision_mainline_planning_v1_smoke_v0/`
- `_eval_out/return_to_vision_mainline_preplan_v1/`
- `_eval_out/ocr_mainline_final_closure_v1_smoke_v0/`
- `_eval_out/minimal_runtime_integration_closure_v1_smoke_v0/`

并引用：

- `docs/architecture/vision/LUNA_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_V1.md`
- `docs/architecture/vision/LUNA_TASK_AWARE_VISUAL_FOCUS_POLICY_V1.md`
- `docs/architecture/midplatform/LUNA_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_V1.md`
- `docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PLANNING_V1.md`
- `docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PREPLAN_V1.md`
- `docs/architecture/ocr/LUNA_OCR_MAINLINE_FINAL_CLOSURE_V1.md`
- `docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CLOSURE_V1.md`
- `docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md`

可选复用文档若不存在，只能标记 `optional_missing`，不得失败，不得伪造能力。

## Core Object 1: SelectiveTrackingAdapterPolicy

关键字段：

- `policy_id`
- `scope`
- `tracking_authority_owner=MidPlatform`
- `allowed_tracking_sources`
- `allowed_focus_slot_types`
- `forbidden_tracking_modes`
- `adapter_candidate_registry`
- `tracking_budget_policy_ref`
- `lifecycle_policy_ref`
- `arbitration_handoff_policy_ref`
- `no_runtime_boundary_ref`
- `no_write_boundary_ref`
- `source_chain`

必须明确：

- tracking authority belongs to `MidPlatform`
- vision module cannot start tracking by itself
- detector cannot start tracking by itself
- adapter cannot start tracking by itself
- tracking requires approved `VisualFocusSlot`
- tracking requires `MidPlatform` resource budget
- tracking requires safety/task relevance
- tracking result is `candidate-only`
- tracking result cannot directly trigger navigation action

## Core Object 2: TrackingRequestCandidate

关键字段：

- `tracking_request_candidate_id`
- `source_work_order_id`
- `source_visual_focus_plan_id`
- `source_focus_slot_id`
- `requested_target_type`
- `requested_tracking_reason`
- `priority`
- `task_relevance`
- `safety_relevance`
- `route_relevance`
- `map_memory_relevance`
- `allowed_adapter_candidates`
- `max_duration`
- `max_tracklets`
- `freshness_requirement`
- `ttl_policy_ref`
- `privacy_filter_required`
- `budget_ref`
- `approval_status=not_approved`
- `runtime_invocation_allowed=false`
- `fact_status=not_fact`
- `source_chain`

`requested_target_type` 至少覆盖：

- `walkable_path`
- `road_surface`
- `route_alignment`
- `near_field_obstacle`
- `dynamic_obstacle`
- `pedestrian`
- `vehicle`
- `bike_or_e_scooter`
- `traffic_light`
- `crosswalk`
- `pedestrian_flow`
- `vehicle_flow`
- `crowd_flow`
- `destination_landmark`
- `shopfront`
- `doorway_or_entrance`
- `temporary_facility`
- `user_feedback_target`

## Core Object 3: TrackletCandidate

`TrackletCandidate` 必须保持 candidate-only。

关键字段：

- `tracklet_candidate_id`
- `source_tracking_request_candidate_id`
- `target_type`
- `target_candidate_ref`
- `track_state`
- `temporal_span_candidate`
- `spatial_path_candidate`
- `motion_state_candidate`
- `relative_position_candidate`
- `approach_or_departure_candidate`
- `occlusion_status_candidate`
- `stability_score_candidate`
- `confidence`
- `freshness_status`
- `ttl_policy_ref`
- `privacy_tags`
- `current_action_allowed=false`
- `feedback_allowed_candidate`
- `archive_allowed_candidate`
- `worldmodel_handoff_allowed_candidate=false by default`
- `fact_status=not_fact`
- `source_chain`

`track_state` 至少覆盖：

- `active_candidate`
- `tentative_candidate`
- `lost_candidate`
- `stale_candidate`
- `expired_candidate`
- `archived_candidate`
- `rejected_candidate`

## Core Object 4: TrackingBudgetPolicy

资源预算由中台控制。

关键原则：

- `P0 safety tracklet budget reserved`
- `primary task over secondary task`
- `secondary task cannot consume safety budget`
- `background world observation tracking limited or disabled`
- `low-value tracklets dropped`
- `high privacy low task-value tracklets suppressed`
- `no unbounded tracking logs`

## Core Object 5: TrackingTargetAdmissionPolicy

允许追踪：

- `P0 safety target`
- `task-relevant target`
- `route-relevant target`
- `user-feedback target`
- `crossing / traffic safety target`
- `destination confirmation target`
- `temporary facility only if task/safety relevant`
- `world observation target only under low-frequency budget`

禁止追踪：

- `full scene`
- `all moving objects`
- `all persons`
- `all vehicles`
- `unrelated background pedestrians`
- `distant unrelated vehicles`
- `privacy-sensitive targets without filtering`
- `low-confidence one-frame noise`
- `curiosity-only targets`
- `emotional-interest-only targets`
- `no source_chain targets`

## Core Object 6: RoadSurfaceTrackingPolicy

必须覆盖：

- `walkable_surface tracking candidate`
- `road_surface candidate`
- `route_direction candidate`
- `sidewalk_boundary candidate`
- `curb / step candidate`
- `crossing surface candidate`
- `path_continuity candidate`

原则：

- 路面/可通行路径优先级高于普通对象
- 路面不稳定时降级为 `route_path_focus + active view adjustment`
- 路面被人群遮挡时可请求 `crowd_flow fallback candidate`
- 路面追踪结果不得直接导航
- 必须进入 `Safety / Task arbitration`

## Core Object 7: PedestrianVehicleTrackingPolicy

必须覆盖：

- `pedestrian_approach_candidate`
- `vehicle_approach_candidate`
- `bike_or_e_scooter_candidate`
- `crossing_conflict_candidate`
- `near_field_dynamic_obstacle_candidate`

原则：

- 只追踪与安全/路线/任务相关者
- 不追踪所有行人
- 不追踪所有车辆
- 陌生人身份不识别
- 车牌不识别
- 只保留运动/风险/空间关系候选
- 不写身份事实

## Core Object 8: CrowdFlowTrackingPolicy

必须覆盖：

- `crowd_flow_candidate`
- `pedestrian_flow_direction_candidate`
- `crowd_density_candidate`
- `queue_flow_candidate`
- `occluded_path_fallback_candidate`

原则：

- 人流可作为遮挡场景下的辅助候选
- `crowd_flow_follow_candidate` 不是导航指令
- 人流方向不等于安全路线
- 人流不得覆盖地图/任务/安全判断
- crowd flow 必须进入 `Safety-Task Arbitration`
- crowded path 下必须保持保守输出

## Core Object 9: TrafficLightAndCrossingTrackingPolicy

必须覆盖：

- `traffic_light_candidate`
- `traffic_light_state_change_candidate`
- `countdown_text_tracking_candidate placeholder`
- `crosswalk_candidate`
- `vehicle_flow_near_crossing`
- `pedestrian_flow_near_crossing`

原则：

- crossing 不在本阶段做行动判断
- traffic light tracking 不等于允许过马路
- OCR countdown 不等于允许过马路
- 人流通过不等于允许过马路
- 输出必须交给未来 `Crossing Decision Governance`
- `current_action_instruction_allowed=false`

## Core Object 10: TrackingAdapterCandidateRegistry

必须包含：

- `Supervision candidate`
- `ByteTrack candidate`
- `OC-SORT candidate`
- `SORT candidate`
- `BoT-SORT candidate`
- `Optical Flow candidate`
- `Frame-diff / motion-score candidate`
- `Tracklet stability evaluator candidate`

每项必须包含：

- `adapter_name`
- `adapter_type`
- `possible_use`
- `maturity_hint`
- `integration_status=future_candidate`
- `runtime_invoked=false`
- `allowed_now=false`
- `experiment_branch_required=true`
- `license_review_required`
- `privacy_review_required`
- `performance_budget_required`
- `source_chain`

必须明确：

- 本阶段不安装、不调用、不导入、不执行任何外部 tracking adapter

## Core Object 11: TrackingLifecyclePolicy

必须定义：

- `requested`
- `admitted_candidate`
- `active_candidate`
- `tentative_candidate`
- `lost_candidate`
- `stale_candidate`
- `expired_candidate`
- `archived_candidate`
- `rejected_candidate`

每个状态都定义：

- `current_action_allowed`
- `feedback_allowed_candidate`
- `archive_allowed_candidate`
- `worldmodel_handoff_allowed_candidate`
- `memory_handoff_allowed_candidate`
- `ttl_required`
- `privacy_filter_required`
- `source_chain_required`

## Core Object 12: TrackingFeedbackPolicy

输出候选：

- `TrackingFeedbackCandidate`
- `SafetyTrackingFeedbackCandidate`
- `TaskTrackingFeedbackCandidate`
- `RouteTrackingFeedbackCandidate`
- `CrowdFlowFeedbackCandidate`
- `CrossingTrackingFeedbackCandidate`
- `TrackingDegradationFeedbackCandidate`

原则：

- feedback candidate 不直接播报
- `speech_allowed=false until Speech Gate`
- `action_allowed=false`
- `fact_status=not_fact`
- `requires_arbitration=true`
- `source_chain required`

## 场景矩阵

本阶段场景矩阵固定至少覆盖 10 个场景：

1. `route_surface_tracking_candidate`
2. `near_field_obstacle_tracking_candidate`
3. `pedestrian_approach_safety_candidate`
4. `vehicle_approach_safety_candidate`
5. `crowded_path_occluded_surface`
6. `traffic_light_state_tracking_candidate`
7. `shopfront_tracking_for_target_confirmation`
8. `temporary_facility_tracking_candidate`
9. `user_feedback_target_tracking_candidate`
10. `low_value_background_tracking_rejected`

其中必须继续保持：

- 路面/可行走路径追踪候选不直接导航
- 近场障碍追踪必须进入 `Safety arbitration`
- 行人靠近风险不做人身份识别
- 车辆靠近风险不识别车牌
- 路面遮挡时只允许 `crowd_flow fallback candidate`
- 红绿灯变化追踪不等于允许过马路
- 商铺门头追踪只作为目标确认候选
- 临时设施追踪必须 `TTL required`
- 用户反馈目标追踪必须依赖 focus slot 调整
- 低价值背景移动目标必须 `rejected`

## Runtime / Write Boundary

本阶段必须保持：

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

## Final Verdict

当 runner / verifier 全部通过时，本阶段的正式结论是：

- `final_decision=SELECTIVE_TRACKING_ADAPTER_POLICY_READY_FOR_VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN`
- `phase verdict=GO`
- `recommended_next_phase=Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001`

这表示：

- `Selective Tracking Adapter Policy` 已正式成立
- 当前只冻结 `policy / schema / contract / boundary`
- 下一阶段进入 `Visual-OCR-Map-Task Feedback DryRun`
- 仍然不要接 runtime
- 仍然不要接 `camera / OCR provider / tracking / map API`
- 仍然不要调用 `Supervision / ByteTrack / OC-SORT`
- 仍然不要写 `WorldModel / Memory / Fact / Library`

后续状态更新：

- `Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001 = GO`
- `Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001 = GO`
- `Phase-Basic-Navigation-Loop-Vision-Strengthening-Post-DryRun-Review-v1-001 = GO`
- `Phase-Basic-Navigation-Loop-Vision-Strengthening-Closure-v1-001 = GO`
- 当前推荐下一阶段：`Phase-Post-Vision-Strengthening-Roadmap-Decision-v1-001`
