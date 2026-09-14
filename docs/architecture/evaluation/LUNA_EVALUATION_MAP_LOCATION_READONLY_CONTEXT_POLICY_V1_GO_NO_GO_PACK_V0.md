# Luna Evaluation — Map / Location Read-Only Context Policy v1 GO / NO-GO Pack

对应 phase：`Phase-Map-Location-ReadOnly-Context-Policy-v1-001`

## GO Conditions

- required roots 全部成功加载
- `MapLocationReadOnlyContextPolicy` 已定义
- `MapLocationContextCandidate` schema 已定义
- `RouteStageHintCandidate` schema 已定义
- `TargetProximityHintCandidate` schema 已定义
- `SideAndOrientationHintCandidate` schema 已定义
- `EntranceIntersectionHintCandidate` schema 已定义
- `MapVisualMemoryConflictPolicy` 已定义
- `MapLocationToVisualFocusBindingPolicy` 已定义
- `MapLocationToOCRActivationHintPolicy` 已定义
- `MapLocationFeedbackPolicy` 已定义
- scenario matrix 已生成且 `scenario_count>=10`
- `map / location / route / POI = readonly_hint`
- `map_is_fact_authority=false`
- `map_is_navigation_authority=false`
- `map_is_safety_authority=false`
- `map_can_trigger_action=false`
- `map_can_prove_arrival=false`
- `map_can_grant_crossing_permission=false`
- `map_can_write_worldmodel=false`
- `map_can_write_memory=false`
- `map_can_write_fact=false`
- `ocr_activation_from_map_requires_visual_focus=true`
- `tracking_request_from_map_requires_visual_focus=true`
- 不存在 runtime / write / action / speech 越权
- 最终推荐阶段固定为 `Phase-Controlled-Frame-Input-Planning-v1-001`

## NO_GO Conditions

- 任一 required root 缺失
- 任一 required policy / schema 产物缺失
- `scenario_count<10`
- 缺少指定 10 个场景中的任意一个
- `map_context_role` 不是 `readonly_hint`
- `location_context_role` 不是 `readonly_hint`
- `route_context_role` 不是 `readonly_hint`
- `poi_context_role` 不是 `readonly_hint`
- 地图被表述为事实权威
- 地图被表述为导航权威
- 地图被表述为安全权威
- 地图可以直接触发 action
- 地图可以证明 arrival
- 地图可以授予 crossing permission
- 地图可以写 `WorldModel / Memory / Fact`
- 允许 full runtime map / GPS / route planning
- 允许 camera / OCR provider / tracking runtime
- 允许 `Navigation Action`
- 允许 `Task State commit`
- 允许 speech 输出
- 允许 `arrival_fact_written=true`
- 允许 `crossing_action_instruction_allowed=true`
- next phase 不明确

## GO Meaning

本阶段 `GO` 的语义仅表示：

- Luna 中台里的 `Map / Location / Route / POI` 只读上下文合同已正式冻结
- 这些信息只能作为 context hint 进入 perception / focus / OCR activation / tracking request / navigation guidance candidate
- 下一阶段可以进入 `Controlled Frame Input Planning`

本阶段 `GO` 不表示：

- 真实地图 API 已接入
- 高德 API 已接入
- GPS runtime 已接入
- live navigation 已可用
- `Navigation Action` 已开放
- `WorldModel / Memory / Fact / Library` 已开放写入

## Next Phase

本阶段通过后，只允许推荐：

- `Phase-Controlled-Frame-Input-Planning-v1-001`

这表示下一步应继续定义受控真实帧输入治理，但仍不直接接 `live camera`。
