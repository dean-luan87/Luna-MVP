# Luna — Map / Location Read-Only Context Policy v1

**Phase**：`Phase-Map-Location-ReadOnly-Context-Policy-v1-001`  
**性质**：policy / schema / contract / boundary only  
**边界**：不调用真实地图 API，不调用高德 API，不调用 GPS runtime，不接 `camera`，不调用视觉模型，不调用 `OCR provider`，不提交 `OCRRequest`，不调用 tracking runtime，不调用 optical flow runtime，不导入或调用 `Supervision / ByteTrack / OC-SORT`，不写 `Memory` / `WorldModel` / `Fact` / `Library`，不做 `entity resolution`，不做 `fact admission`，不做 `memory consolidation`，不做 `library experience commit`，不生成 `Scene Delta`，不提交 `Task State`，不触发 `Navigation Action`，不调用 `Speech Gate / VOP / TTS`，不输出真实用户可听语音

## 目标

本阶段正式定义 Luna 中台中的 `Map / Location Read-Only Context Policy`。

核心结论：

- `map / location / route / POI = readonly_hint`
- 它们只能作为 context hint
- 它们不是事实权威
- 它们不是导航权威
- 它们不是安全权威
- 它们不能直接触发动作
- 它们不能证明已到达
- 它们不能赋予过街许可
- 它们不能写入 `WorldModel / Memory / Fact`

## Map / Location Role

本阶段回答：

1. Map / Location 在 Luna 中台中的角色是 `readonly_hint`
2. 地图、位置、路线、POI 不可作为事实
3. 地图 hint 可以参与任务阶段判断，但只能生成 candidate
4. 地图 hint 可以辅助 `VisualFocusPlan`
5. 地图 hint 可以辅助 `OCR activation candidate`
6. 地图 hint 可以辅助 `tracking request candidate`
7. 地图 / 位置与视觉 / OCR / 记忆冲突时必须进入 conflict / correction candidate
8. 目标接近、左右侧、入口、路口、路线阶段只允许表达为 candidate
9. 地图信息过期、偏移、不确定、无信号时必须降级
10. 本阶段不接真实高德 API，不触发导航动作

## Core Objects

### MapLocationReadOnlyContextPolicy

必须固定：

- `map_context_role=readonly_hint`
- `location_context_role=readonly_hint`
- `route_context_role=readonly_hint`
- `poi_context_role=readonly_hint`
- `safety_arbitration_required=true`

允许用途：

- task phase hinting
- route stage candidate generation
- target proximity hinting
- side and orientation hinting
- entrance and intersection hinting
- VisualFocusPlan assistance
- OCR activation candidate assistance after visual focus binding
- tracking request candidate assistance after visual focus binding
- NavigationGuidanceCandidate assistance as readonly context
- conflict detection and correction handoff placeholder generation

禁止用途：

- fact authority
- navigation authority
- safety authority
- action trigger
- arrival proof
- crossing permission
- `WorldModel fact write`
- `Memory fact write`
- direct OCR runtime invocation
- direct tracking runtime invocation
- direct Navigation Action
- direct Task State commit

### MapLocationContextCandidate

支持的 `source_type`：

- `simulated_map_hint`
- `cached_map_placeholder`
- `user_provided_location_hint`
- `memory_derived_location_hint`
- `route_plan_placeholder`
- `gps_placeholder`
- `poi_placeholder`
- `map_anchor_placeholder`

必须保持：

- `provider_runtime_invoked=false`
- `fact_status=not_fact`
- `action_allowed=false`

### RouteStageHintCandidate

覆盖至少以下 `route_stage`：

- `route_not_started`
- `route_walking`
- `approaching_crossing`
- `crossing_area_candidate`
- `after_crossing_candidate`
- `approaching_destination`
- `target_search_area`
- `target_confirmation_area`
- `arrived_candidate`
- `off_route_candidate`
- `route_uncertain`

必须明确：

- `arrived_candidate` 不等于已到达事实
- `crossing_area_candidate` 不等于允许过马路
- `off_route_candidate` 不等于真实偏航事实

### TargetProximityHintCandidate

覆盖：

- `far`
- `nearby`
- `approaching`
- `very_close`
- `uncertain`

### SideAndOrientationHintCandidate

覆盖：

- `left`
- `right`
- `front`
- `behind`
- `across_road`
- `same_side`
- `opposite_side`
- `unknown`

### EntranceIntersectionHintCandidate

用于表达：

- entrance hint
- intersection hint
- crossing hint
- floor hint

必须保持：

- `crossing_action_allowed=false`
- `arrival_fact_allowed=false`
- `fact_status=not_fact`

## Conflict Policy

`MapVisualMemoryConflictPolicy` 必须覆盖：

- `map_vs_visual`
- `map_vs_ocr`
- `map_vs_memory`
- `location_vs_visual`
- `route_vs_visual`
- `poi_vs_signage`
- `side_hint_vs_scene_sketch`
- `arrival_hint_vs_visual_absence`
- `crossing_hint_vs_safety_uncertain`
- `stale_map_vs_current_observation`

冲突输出只能进入：

- `MapLocationConflictCandidate`
- `ReobserveRequestCandidate`
- `UserConfirmationCandidate`
- `CorrectionHandoffCandidate`

原则：

- 地图冲突不自动修正事实
- 地图不能覆盖视觉安全
- 地图不能覆盖用户反馈
- 地图不能直接更新 `WorldModel`
- 地图 conflict 可进入 correction candidate / handoff placeholder

## Visual Focus / OCR / Tracking Binding

### MapLocationToVisualFocusBindingPolicy

允许：

- 目标接近时提高 `destination_landmark_focus`
- 右侧店铺 hint 触发 `right-side shopfront focus`
- 路口 hint 触发 `crossing_focus / traffic_light_focus`
- 入口 hint 触发 `doorway_or_entrance_focus`
- POI hint 触发 `signage_focus / OCR activation candidate`
- 路线不确定时触发 `active view adjustment / reobserve`

禁止：

- 地图直接触发 OCR runtime
- 地图直接触发 tracking runtime
- 地图直接生成导航动作
- 地图直接判断已到达
- 地图直接判断可过马路

### MapLocationToOCRActivationHintPolicy

允许：

- `approaching_destination -> signage OCR target candidate`
- `shop_search_area -> shopfront / doorplate OCR target candidate`
- `intersection_area -> traffic sign / countdown text OCR target candidate placeholder`
- `indoor_floor_hint -> directory sign OCR target candidate`
- `temporary_notice_area -> notice OCR target candidate`

禁止：

- `full-frame OCR`
- `OCR provider invocation`
- `OCRRequest submission`
- OCR from map alone without visual / readable region candidate
- OCR on privacy-sensitive text without filtering

必须明确：

- `ocr_activation_from_map_requires_visual_focus=true`
- `tracking_request_from_map_requires_visual_focus=true`

## Feedback Policy

只允许输出：

- `MapLocationFeedbackCandidate`
- `RouteStageFeedbackCandidate`
- `TargetProximityFeedbackCandidate`
- `SideOrientationFeedbackCandidate`
- `EntranceIntersectionFeedbackCandidate`
- `MapVisualMemoryConflictFeedbackCandidate`

并保持：

- `feedback candidate only`
- `speech_allowed=false`
- `action_allowed=false`
- `navigation_action_allowed=false`
- `fact_status=not_fact`
- `requires_arbitration=true`

## Scenario Matrix

本阶段覆盖 10 个最小场景：

1. `route_walking_map_hint`
2. `approaching_destination_nearby`
3. `right_side_shop_search`
4. `intersection_approach_hint`
5. `entrance_hint_candidate`
6. `off_route_uncertain_hint`
7. `map_visual_conflict_shop_absent`
8. `stale_map_or_old_poi`
9. `indoor_floor_directory_hint`
10. `gps_low_confidence_location_uncertain`

每个场景都必须保持：

- `action_allowed=false`
- `navigation_action_allowed=false`
- `fact_status=not_fact`
- `crossing_action_allowed=false`
- `arrival_fact_allowed=false`

## Boundary

本阶段正式冻结：

- `no-runtime`
- `no-write`
- `no-action`
- `no-speech`
- `no-fact`
- `map_api_invoked=false`
- `gaode_api_invoked=false`
- `gps_runtime_invoked=false`
- `route_planning_runtime_invoked=false`
- `camera_invoked=false`
- `ocr_provider_invoked=false`
- `tracking_runtime_invoked=false`
- `navigation_action_triggered=false`
- `arrival_fact_written=false`
- `crossing_action_instruction_allowed=false`
- `world_model_written=false`
- `memory_written=false`
- `library_written=false`
- `fact_written=false`

## Governance Debt

本阶段保留的 debt 包括：

- map/location freshness and offset governance complexity
- route-stage candidate calibration debt
- side and orientation ambiguity debt
- entrance and intersection uncertainty debt
- map-visual-memory conflict escalation debt
- privacy filtering for map-guided OCR target debt
- controlled frame input dependency debt
- crossing governance dependency debt
- schema consolidation risk

并继续明确：

- `future_midplatform_function_governance_required=true`
- `no_duplicate_governance_module_allowed=true`

## Final Verdict

当 runner / verifier 全部通过时，本阶段正式结论为：

- `final_decision=MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING`
- `phase verdict=GO`
- `recommended_next_phase=Phase-Controlled-Frame-Input-Planning-v1-001`

这表示：

- `Map / Location / Route / POI` 只读上下文合同已经正式定义
- 它们仍然只是 context hint
- 不进入真实地图 API / 高德 API / GPS runtime
- 不进入 live navigation
- 不进入 action
- 不写 `WorldModel / Memory / Fact / Library`
- 下一阶段进入 `Controlled Frame Input Planning`

当前状态更新：

- `Phase-Controlled-Frame-Input-Planning-v1-001 = GO`
- `Phase-Controlled-Frame-Input-DryRun-v1-001 = GO`
- 当前推荐下一阶段：`Phase-Controlled-Frame-Input-Post-DryRun-Review-v1-001`
