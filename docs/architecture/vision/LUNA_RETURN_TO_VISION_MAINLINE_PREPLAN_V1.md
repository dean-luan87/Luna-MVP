# Luna — Return To Vision Mainline Preplan v1

**性质**：preplan / reuse audit / architecture planning only  
**范围**：`return_to_vision_mainline_preplan_only`  
**边界**：不实现 runtime，不接真实相机，不接真实 OCR provider，不接地图 API，不写 `WorldModel` / `Memory` / `Fact`

## 背景

当前已完成并收口：

- `Phase-Minimal-Runtime-Integration-Closure-v1-001 = GO`
- `Phase-OCR-Mainline-Final-Closure-v1-001 = GO`

主线从 OCR / Minimal Runtime Integration 收口后，正式回到“视角强化”，但本次**不是**正式 phase 执行，而是回归前的规划与复用审计。

## 主线方向

不再采用 `3x3` 固定画面切割作为视觉主线。  
新的主线方向是：

- `Task-Aware Perception Orchestration`
- 中台负责感知编排和任务调度
- 视觉 / OCR / 地图 / 记忆都不是主脑

中台在当前时间窗和任务阶段内，决定：

- 当前应该看什么
- 是否需要激活 OCR
- 是否需要选择性追踪
- 是否需要参考地图 / 路线 / 位置上下文
- 是否需要参考历史记忆
- 是否应生成安全反馈 / 任务反馈 / 用户视角调整请求

## 复用优先原则

本阶段冻结以下原则：

- `Reuse First, Extend Second, Create Last`
- 不新建平行 `STC / TTL / freshness / source_chain / Evidence / Memory / Task / Speech` 模块
- 优先复用 OCR / MidPlatform 已有 candidate-only / no-write / handoff 机制
- 视觉候选默认 `fact_status=not_fact`
- 视觉候选默认 `write_allowed=false`
- `WorldModel / Memory / Library` 深层治理全部 deferred；当前视觉主线只负责生成候选材料、handoff 结构和 placeholder，不执行实体融合、事实准入、长期记忆固化或图书馆经验治理

## 现有关键模块结论

本次审计发现，以下模块应作为视觉主线的首选复用锚点：

- `LUNA_TASK_OBSERVATION_REQUEST_CONTRACT_V1.md`
  - 最接近未来 `MidPlatform Perception Work Order`
  - 已定义为什么观察、观察什么、可能在哪、需要 vision/OCR/地图/记忆参考、经哪些 gate
- `LUNA_TASK_MANAGER_CONTRACT_V1.md`
  - 已定义任务生命周期提交权、task context enrichment、候选提交与 no-write 边界
- `LUNA_SAFETY_TASK_ARBITRATION_POLICY_V1.md`
  - 可直接承接 `Safety Lane / Task Lane` 的统一仲裁
- `LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md`
  - 已冻结 STC 与 OCR/阅读引导的触发逻辑
  - 视觉主线不得平行新建另一套 STC
- `LUNA_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_V0.md`
  - 是未来 `World Observation Layer` 与 `ObjectWorldModelHandoffCandidate` 的直接治理锚点
- `LUNA_CONFIRMED_TEXT_EVIDENCE_MEMORY_GOVERNANCE_CONTRACT_V1.md`
  - 锁定 `Memory` 只能通过治理 handoff，不允许视觉侧越权写入
- `LUNA_VISION_FRAME_TRACE_STREAM_REGISTRY_V0.md`
  - 提供 `source_frame_ref` / `timestamp` / lineage / trace 基础
- `LUNA_VISION_FRAME_INPUT_GOVERNANCE_V0.md`
  - 提供视觉输入治理与 full-frame direct provider 禁止边界
- `LUNA_VISION_FRAME_ROI_PROPOSAL_AND_SEGMENTATION_STUB_V0.md`
  - 其 `vision_provider_input_pack_v0` 和 source-chain 机制可复用
  - 但固定 ROI 逻辑不能直接作为新的任务主线
- `LUNA_VISION_ROI_TO_OCR_REQUEST_BRIDGE_V0.md`
  - 是未来 focus-triggered OCR 的直接复用入口
- `LUNA_TEXT_REGION_TRACKLET_DRYRUN_V1.md`
  - 证明仓库已有 tracklet / multiframe 候选链，但仍是 candidate-only
- `LUNA_EXISTING_YOLO_INTEGRATION_INVENTORY_V0.md`
  - 明确 YOLO / DeepSORT 只能做历史参考或 future adapter candidate
- `LUNA_VISION_EXTERNAL_SUPERVISION_ADAPTER_EXPERIMENT_V0.md`
  - 明确 `Supervision / ByteTrack` 只允许做外部参考线，不得接管主线
- `LUNA_WORLD_MODEL_MAP_ANCHOR_INTEGRATION_DEFINITION_V0.md`
  - 明确地图 / GPS / POI 只是空间锚点候选，不是事实也不是行动权威
- `LUNA_WORLD_CONTEXT_EVIDENCE_BOUNDARY_REGISTER_V0.md`
  - 明确 candidate-only / no fabricated GPS / no write / no navigation action
- `LUNA_MINIMAL_RUNTIME_INTEGRATION_CLOSURE_V1.md`
  - 固定后续规划继续保持 no-runtime / no-write / controlled-only 边界
- `LUNA_OCR_MAINLINE_FINAL_CLOSURE_V1.md`
  - 固定 OCR 只作为 future candidate/reference layer，不再扩主线

## Module Reuse Matrix 结论

### 直接复用

- `Task Observation Request Contract v1`
- `Safety Task Arbitration Policy v1`
- `Vision Frame Trace + Stream Registry v0`
- `Vision Frame Input Governance v0`
- `Static Readable Region Discovery Guidance Policy v1`
- `OCR Activation Governance Policy v1`
- `System Health Center Governance v0`

### 以 schema_extension 方式复用

- `Task Observation Request Contract v1` → 扩为 `MidPlatform Perception Work Order`
- `Vision ROI Proposal / Input Pack` → 扩为 `VisualFocusSlot` 的来源与 frame/ROI source refs
- `Vision Recognition Evidence Pack v0` → 扩为视觉 candidate 包，而不是新建平行 Evidence Pack
- `Text Region Tracklet DryRun v1` → 扩为选择性追踪候选治理，不直接变 runtime tracker
- `Navigation Perception Signal Contract v0` → 只吸收结构化 signal 形状，不直接沿用旧导航 contract

### 以 handoff_contract 方式复用

- `Task Manager Contract v1`
- `MidPlatform Task State Runtime DryRun v1`
- `WorldModel Unresolved Observation Slot Contract v0`
- `WorldModel Lookup for Reading Framework v1`
- `Confirmed Text Evidence Memory Governance Contract v1`
- `MapAnchorEvidence / MapAnchor Trust Policy`

### 只作参考，不进入当前主线

- `Unified Env Shadow` 系列文档
- 旧 `YOLO / DeepSORT` 历史路径
- `Supervision / ByteTrack` 实验线
- 旧 `vision_pipeline` 中未治理的 runtime 片段

## 重复风险结论

本次规划最需要避免的重复建设：

1. 视觉侧再建一套 `STC / freshness / TTL / stale / source_chain`
2. 视觉侧再建一套平行 `Evidence Pack`
3. 视觉侧私自定义 `Memory write / WorldModel write`
4. 视觉侧再建平行 `Task Context / Task State`
5. 视觉侧再建平行 `Speech / Output Gate`
6. 视觉侧再建平行 `Runtime Trial / Closure` 体系
7. `World Observation Layer` 被误实现成新的世界模型写入层
8. `ObjectFeatureCandidate` 被误描述成事实层

## 建议的视觉主线架构

### 1. MidPlatform Perception Work Order

建议基于 `TaskObservationRequestContract v1` + `TaskManager Contract v1` + `MidPlatformTaskState` 扩展，而不是新开平行模块。

职责：

- 接收任务阶段、场景上下文、地图/位置 hint、记忆 hint
- 生成当前时间窗内的视觉/OCR/追踪工作单
- 明确 focus targets、OCR allowed slots、tracking budget、freshness policy ref
- 保持 `runtime_action_allowed=false`
- 保持 `fact_write_allowed=false`

### 2. SceneSketchCandidate

用于压缩当前环境状态，只表达 candidate，不直接播报、不直接行动：

- `scene_type_candidate`
- `left/right/front/far_context`
- `walkable_area_hint`
- `human_density`
- `vehicle_presence`
- `signage_or_text_hint`
- `visibility_quality`
- `freshness_status`
- `fact_status=not_fact`

建议复用：

- `Vision Recognition Evidence Pack v0`
- `Navigation Perception Signal Contract v0`
- `Vision Frame Trace / Input Governance`

### 3. VisualFocusPlan / VisualFocusSlot

由任务、环境速写、地图/记忆 hint 决定当前该关注什么。

建议：

- `VisualFocusPlan` 由中台生成
- `VisualFocusSlot` 绑定 `task_relevance` / `safety_relevance` / `ocr_required` / `tracking_required`
- 默认 `ignored_by_default`
- 必须受 `budget_policy` 约束

### 4. SelectiveTrackingBudget

追踪必须是**选择性**的，不允许 full-scene tracking。

建议：

- 追踪授权方：`MidPlatform Perception Work Order`
- 追踪预算由任务相关性、安全相关性、路线相关性共同约束
- 最大 active tracklets、最大持续时间、丢弃条件必须写死
- 所有 tracking 输出均为 candidate-only

### 5. VisualObservationCandidate / ExpiredVisualObservationCandidate

视觉候选生命周期建议采用：

- `active`
- `stale`
- `expired`
- `archived_candidate`
- `future_review`
- `rejected`
- `promoted_later`

但 promotion 仍然不能在视觉主线内直接写事实层。

### 6. Feedback Candidate

建议统一输出：

- `TaskFeedbackCandidate`
- `SafetyFeedbackCandidate`

要求：

- `requires_arbitration=true`
- `speech_allowed=false until Speech Gate`
- `action_allowed=false`
- `fact_status=not_fact`

## Safety Lane / Task Lane

### Safety Perception Lane

- `always_on=true`
- 低时延
- 关注近场障碍、车辆、行人、电动车、自行车、红绿灯、台阶、坑洞、可通行区域中断、突发动态风险
- 不可被任务禁用
- 输出 `SafetyObservationCandidate`
- 仍不直接行动

### Task Perception Lane

- 仅按 `MidPlatform Perception Work Order` 激活
- 预算受控
- 动态 focus
- 只处理已批准的 `focus_slots`
- 输出 `TaskObservationCandidate / VisualFocusCandidate`

### 仲裁

两条 lane 都进入：

- `SafetyTaskArbitration`
- 后续如需语音，仅能继续进入 `Speech Gate / VOP candidate path`

## OCR 复用计划

OCR 在新视觉主线中的角色：

- 不是主脑
- 不是默认全图扫读
- 不是新主线扩展点
- 只作为 `VisualFocusPlan` 触发的精读候选

必须复用：

- `OCR Activation Governance Policy v1`
- `STC Sampling Guidance Policy v1`
- `Static Readable Region Discovery`
- `Vision ROI to OCR Request Bridge v0`
- `OCRRequest gate`
- `OCR Evidence / Evidence Pack`
- `TTL / freshness / source_chain / no-write` 机制

不得：

- full-frame OCR
- 真实 OCR provider runtime
- 直接写 `WorldModel` / `Memory` / `Fact`

## 地图 / 路线 / 记忆上下文计划

地图、路线、位置、记忆在本阶段只作为 `context hint`：

- 判断是否接近目标
- 判断左/右/前方的关注侧
- 判断 target search / target confirmation 阶段
- 提示 OCR 是否应关注门牌、招牌、标识
- 提示视觉是否应关注路口、入口、站点、商铺

不得：

- 直接触发行动
- 直接播报为事实
- 覆盖实时安全视觉
- 写 `WorldModel` / `Memory` / `Fact`

## World Observation Layer

应提前在架构上预留 `World Observation Layer`，但本期只做规划：

- `candidate-only`
- 可低频后台运行
- 不直接播报
- 不直接导航
- 不直接写 `WorldModel` / `Memory` / `Fact`
- 必须携带 `timestamp / location / pose / task_context / source_chain`
- 必须复用既有 `freshness / TTL / stale / no-write / handoff` 机制

推荐产物：

- `WorldObservationCandidate`
- `WorldModelHandoffCandidate`

推荐复用：

- `WorldModel Unresolved Observation Slot Contract`
- `WorldContextEvidence Boundary Register`
- `MapAnchorEvidence`
- `Memory Governance`

`Unified Env Shadow` 只作为历史参考，不直接成为当前主线模块。

## World Entity Feature Candidate

建议把对象属性扩展为更一般的 `WorldEntityFeatureCandidate`，覆盖：

- `ObjectCandidate`
- `PlaceCandidate`
- `EventCandidate`
- `RelationCandidate`
- `FacilityCandidate`
- `SocialFacilityCandidate`
- `TemporaryFacilityCandidate`
- `RouteStructureCandidate`
- `EnvironmentalPatternCandidate`

属性层建议分为：

- `universal_attributes`
- `task_specific_attributes`
- `user_profiled_attributes`
- `social_context_attributes`
- `emotional_attributes`
- `operational_attributes`
- `uncertainty_and_conflict`

核心字段可包括：

- `entity_name_candidate`
- `entity_category_candidate`
- `shape_candidate`
- `size_estimate_candidate`
- `color_candidate`
- `material_candidate`
- `function_candidate`
- `affordance_candidate`
- `operating_time_candidate`
- `nickname_or_user_alias_candidate`
- `historical_interaction_ref`
- `emotional_attachment_candidate`
- `location_anchor_candidate`
- `task_relevance_history`
- `ocr_text_refs`
- `visual_refs`
- `memory_refs`
- `map_refs`

关键边界：

- 这些都只是 candidate
- 不直接写事实
- 用户画像/兴趣/昵称/情感挂载等字段应标记授权与长期确认要求
- 多次观察、冲突检测、人工确认后才允许进入更高层 handoff

## Road / Vehicle / Pedestrian / Crowd Flow Tracking

不采用 full-scene tracking。  
优先追踪任务/安全相关对象：

- `road_surface_candidate`
- `walkable_path_candidate`
- `route_direction_candidate`
- `lane_or_sidewalk_boundary_candidate`
- `crossing_candidate`
- `traffic_light_candidate`
- `safety_sign_candidate`
- `obstacle_candidate`
- `pedestrian_candidate`
- `vehicle_candidate`
- `bike_or_e_scooter_candidate`
- `crowd_flow_candidate`
- `vehicle_flow_candidate`

特别规则：

- 导航优先锁定路面 / 可行走路径 / 路线走向
- 路面候选不稳定时，可退到 `crowd_flow_follow_candidate`
- 但 crowd flow 不是自动跟随指令
- 追踪结果只进入 candidate / arbitration，不直接行动

## Optical Flow / Motion Reuse Review

审计结果：

- 当前仓库存在可复用的 `frame_diff / motion_score / ego_motion / path_instability / branch_load` 基础
- `vision_pipeline/b2/v03/gate/stability_evaluator.py` 存在 `optical_flow_magnitude` 占位式稳定性计算
- `vision_pipeline/pipeline_controller.py` 会计算 `frame_diff_score`、`motion_score`、`path_instability`、`branch_load`
- `vision_pipeline/c1` 与 `b2` 分支已有 `frame_diff` / `dynamic_objects` / continuity 相关逻辑
- `Text Region Tracklet DryRun v1` 与 multiframe 链表明仓库已有 candidate-only 时序链
- 旧 `optical_flow.py` / `optical_flow_estimator.py` 仅在 `_architecture_scan` 中出现，更像历史参考痕迹
- `DeepSORT / ByteTrack / Supervision` 目前只应被视作历史或外部 adapter candidate

因此建议：

- 光流 / motion 先进入 `MotionEvidenceCandidate / FlowObservationCandidate / TrackletSupportCandidate`
- 不直接触发导航动作
- 不直接写事实
- 当前阶段先做 policy / schema / dry-run review，**不**直接接真实算法

## MidPlatform Resource Budget

资源预算应明确归属中台，而不是视觉模块私有。

建议定义：

- `MidPlatformResourceBudgetPolicy`

核心字段：

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
- `degradation_policy`
- `preemption_policy`

可复用资产：

- `Hardware Profile Capability Registry v1`
- `System Health Center Governance v0`
- `Resource Sufficiency Gate v0 Baseline`
- `Safety-Task Arbitration`

## MidPlatform Privacy Filtering

隐私不应在采集阶段被过早粗暴阻断，而应在中台统一过滤与分层使用。

建议分层：

1. `Raw Observation Candidate`
2. `Privacy-Filtered Candidate`
3. `Restricted Use Candidate`
4. `Long-Term Eligible Candidate`

建议标签：

- `human_identity_sensitive`
- `face_visible`
- `license_plate_visible`
- `private_space_candidate`
- `medical_context_candidate`
- `school_or_child_context_candidate`
- `home_context_candidate`
- `workplace_context_candidate`
- `personal_item_candidate`
- `bystander_presence_candidate`

原则：

- 采集不等于可用
- 可用不等于可存
- 可存不等于可写 `WorldModel`
- 可写候选不等于事实

## Information Correction / Reality Mismatch

需要预留：

- `PerceptionCorrectionCandidate`
- `RealityMismatchCandidate`
- `WorldModelCorrectionHandoffCandidate`

冲突来源包括：

- `visual_vs_ocr`
- `visual_vs_map`
- `visual_vs_memory`
- `visual_vs_user_feedback`
- `signboard_vs_business_function`
- `map_poi_vs_current_scene`
- `historical_observation_vs_current_observation`
- `temporary_facility_vs_static_poi`

原则：

- 发现冲突不等于自动修正事实
- 用户反馈也先是 correction candidate
- 多次观察一致后才可进入 WorldModel correction handoff

## Temporary / Mobile Social Facility

需要单独规划：

- `TemporaryFacilityCandidate`
- `MobileFacilityCandidate`
- `TransientSceneStructureCandidate`

典型对象：

- 临时摊位
- 流动商贩
- 临时施工围挡
- 临时排队点
- 临时服务台
- 临时路障
- 临时公告
- 夜市 / 临时市场 / 人群聚集

原则：

- 默认短 TTL
- 可用于当前任务/安全候选
- 不默认写长期 `WorldModel`
- 多次在同一位置/时间窗出现后，可升级为 recurring temporary pattern candidate

## Active View Adjustment

若当前视角看不到关键证据，应只生成引导候选：

- `ActiveViewAdjustmentCandidate`

例如：

- 稍微向右转一点
- 抬高一点
- 先停稳
- 靠近一点
- 看向右侧门头
- 对准桌面

它只能是候选，最终仍需经过 `Speech Gate / VOP`。

## View Quality Gate

视觉也需要类似 OCR readability 的质量门，但应优先复用现有 OCR / MidPlatform 机制。

建议定义：

- `ViewQualityCandidate`

评估维度：

- 模糊
- 过暗 / 过曝
- 遮挡
- 视角过偏
- 抖动
- 目标太远
- 动态过快
- 人流遮挡
- 雨雾 / 反光
- 帧稳定性

它决定：

- 是否允许生成 `SceneSketch`
- 是否允许激活 OCR
- 是否允许追踪
- 是否需要 `hold_still`
- 是否需要降级到 `safety-only`

## Perception Conflict Governance

需要统一治理：

- `PerceptionConflictCandidate`

冲突类型至少包括：

- `visual_vs_map`
- `visual_vs_memory`
- `ocr_vs_visual`
- `route_vs_scene`
- `task_goal_vs_current_view`
- `fresh_vs_stale_conflict`
- `temporary_facility_vs_static_poi`

处理方式：

- 请求重新观察
- 请求用户确认
- 降级为疑似
- 延迟反馈
- 进入 review queue
- 进入 correction candidate

## Visual Observation Lifecycle

建议分四层：

1. `Live Visual Candidate`
2. `Stale Visual Candidate`
3. `Archived Visual Observation Candidate`
4. `WorldModel Handoff Candidate`

淘汰与保留规则：

- 低价值背景噪声丢弃
- 重复低置信候选压缩
- 高价值位置/对象/路线信息保留
- 涉及隐私的人脸/私人空间做特殊治理
- 临时设施按 TTL 过期
- 多次重复出现可成为 recurring pattern candidate

## Task Phase Perception Policy

中台感知编排必须知道任务阶段。

导航任务阶段建议：

- `ROUTE_START`
- `ROUTE_WALKING`
- `APPROACHING_CROSSING`
- `CROSSING_DECISION`
- `APPROACHING_TARGET`
- `TARGET_SEARCH`
- `TARGET_CONFIRMATION`
- `ARRIVED_CANDIDATE`
- `SAFETY_HOLD`

不同 phase 下，`VisualFocusPlan`、OCR 激活、tracking budget、地图/记忆 hint 的使用都不同。

## User Visual Feedback

用户反馈会改变视觉策略，需要预留：

- `UserVisualFeedbackCandidate`

示例：

- 不是这个
- 我看不到
- 再靠近一点
- 右边那个
- 我已经过马路了
- 这里人太多

它可影响：

- focus slot 调整
- tracking target 替换
- OCR 目标变化
- 地图 / 记忆 hint 降权
- Scene Sketch 重新采样
- correction candidate
- task phase 转换

## Evaluation Metrics

视觉主线应提前规划评测指标，而不是实现后再补。

至少包括：

- 任务相关候选命中率
- 无意义追踪压制率
- 安全焦点保留率
- OCR 触发准确性
- 地图/视觉冲突识别率
- stale 候选误用率
- `source_chain` 完整率
- 候选数量预算命中率
- 低质量视角降级率
- 用户反馈修正链路完整率
- 临时设施 TTL 正确性
- 信息修正候选覆盖率
- 资源预算降级正确率
- 隐私过滤命中率
- `WorldModel` handoff candidate 合规率

## MidPlatform Governance Expansion Risk

新增视觉主线时，还需额外防止以下治理扩展风险：

- `resource budget` 被视觉模块私有化
- 隐私在采集层粗暴阻断导致生活理解缺失
- 隐私未过滤就进入长期存储
- 世界实体属性过度推断用户职业/兴趣
- 情感挂载误写为事实
- 门牌/实际功能冲突被错误合并
- 临时设施被错误写成固定 POI
- 全量追踪导致日志/资源爆炸
- 地图/记忆覆盖实时视觉
- 过期视觉信息被当作当前事实
- 新建重复 `STC / TTL / Memory / WorldModel` 模块
- `crowd_flow` 被误当作可直接跟随指令
- 光流被误用于直接导航动作

## P0 / P1 / P2 能力分层

根据系统模拟后的补充要求，后续能力优先级建议分为三层。

### P0

这些不先补齐，视觉主线会失去统一治理基础：

1. `MidPlatformPerceptionWorkOrder`
2. `TaskPhasePerceptionPolicy`
3. `SceneSketchCandidate`
4. `VisualFocusPlan / VisualFocusSlot`
5. `MidPlatformResourceBudgetPolicy`
6. `VisualObservationLifecycle`
7. `ViewQualityGate`
8. `PerceptionConflict / Correction`

### P1

这些非常重要，但可在 P0 收口后再做：

1. `SelectiveTrackingPolicy`
2. `OCRFocusActivation`
3. `WorldObservationLayer`
4. `Temporary / Mobile Social Facility`
5. `UserVisualFeedbackCandidate`
6. `MidPlatformPrivacyFilteringPolicy`

### P2

这些是长期能力，但当前就要预留边界：

1. `WorldEntityFeatureCandidate`
2. `ObjectIdentityOverTime`
3. `EmotionalAttachmentCandidate`
4. `OpticalFlow / MotionEvidence`
5. `CrowdFlowFollowingCandidate`
6. `EvaluationMetrics`

特别注意：

- `CrowdFlowFollowingCandidate` 只是一种遮挡场景下的保守候选，不是导航指令
- `ObjectIdentityOverTime` 只做候选，不得用单次观察写长期身份事实
- `EmotionalAttachmentCandidate` 只做候选，不得写成用户情感事实

## 系统运行场景复盘

本轮 preplan 新增四个高价值系统场景，用来提前暴露真实运行时会遇到的问题。

### 1. 导航去商场

重点不是“识别商场”，而是：

- 地图 / 位置 hint 如何进入中台
- 中台如何生成导航感知工作单
- 如何形成 `route_path_focus` / `safety_focus` / `destination_landmark_focus`
- OCR 如何只在接近目标时关注商场招牌 / 入口 / 门牌
- 如何避免直接说“已经到达”
- 如何只形成“疑似接近目标，请向右观察”之类保守候选
- 过马路如何切换到安全优先治理

### 2. 在家找东西

重点不是直接认出物体，而是：

- 记忆 hint 如何参与搜索
- 视觉如何优先关注桌面、柜台、货架、地面、包等支持面
- 如何处理“小金属物体可能是钥匙”这类候选
- 用户说“不是这个”后如何调整 focus slot
- 家庭隐私如何进入中台过滤
- 为什么不能直接写家庭物品事实

### 3. 在家互动 / 熟悉物体认知

重点是保守地形成长期对象候选：

- 当前视角中心物体如何生成 `WorldEntityFeatureCandidate`
- 如何关联历史记忆、昵称、熟悉度、情感挂载候选
- 为什么用户确认前不能写事实
- 如何形成“看起来像你之前常用的蓝色杯子”这类保守表达
- `ObjectIdentityOverTime` 为什么只能是 candidate

### 4. 带 Luna 出去玩 / 后台构建世界模型

重点是后台世界观察如何低频运行而不滑向全量记录：

- 无明确任务时如何进入 `LOW_PRIORITY_WORLD_OBSERVATION`
- 如何记录道路、河边、公园、临时摊位、场景变化等高价值候选
- 临时设施如何 TTL 化
- 如何避免全量记录和隐私泄漏
- 如何形成未来的 `WorldModelHandoffCandidate`

场景复盘得到的直接结论是：`crossing`、`household/private space`、`world observation value filtering`、`feedback-to-focus adaptation` 都不能留到实现时再补。

## Crossing Decision Governance 预留

系统模拟暴露出一个关键事实：红绿灯 / 过马路不是普通视觉任务，也不是普通 OCR 任务。

因此应预留独立的 `CrossingDecisionGovernance` 占位，并写死以下边界：

- 过街相关观察必须进入 P0/P1 安全链
- 红绿灯候选不能单独决定“可以通行”
- OCR 倒计时不能单独决定“可以通行”
- 人流通过不能单独决定“可以通行”
- 地图路口提示不能单独决定“可以通行”
- 车辆 / 人流 / 灯态 / 用户位置 / 朝向 / 路口结构必须综合判断
- 一期不得输出“可以过马路”这类强行动指令

一期只允许保守提示，例如：

- “前方疑似路口，请先停稳观察”
- “检测到红绿灯区域，但当前不能确认安全通行”
- “当前人流开始通过，但请继续注意车辆”

结论上，`Crossing Decision Governance` 应后续拆成独立 `safety governance phase`。

## World Observation Value Filtering

后台世界观察不能变成“什么都存”。  
必须先做价值筛选，再考虑 archive 或 future handoff。

高价值候选：

- 路线结构
- 常走路径
- 出入口
- 公共设施
- 商铺 / 门头 / 站点
- 临时设施
- 场景变化
- 安全风险点
- 用户反复询问 / 互动对象
- 用户确认过的重要地点 / 物品
- OCR / 地图 / 记忆冲突点

低价值候选：

- 无任务关系的背景行人
- 一次性低置信噪声
- 无法定位的短暂背景物
- 远处无关车辆
- 重复低价值画面
- 隐私高风险且无任务价值内容

因此 `World Observation Layer` 不是 full background recording，而是 low-frequency + value-filtered candidate pipeline。

## Household / Private Space Handling

家庭场景必须额外治理。  
在家找东西和家里互动会触发大量私人空间信息。

需要写死：

- 家庭空间观察默认进入 `privacy-sensitive context`
- 家庭观察可用于当前任务，但长期保存门槛更高
- 家庭物品可作为用户相关对象候选，但不直接写事实
- 陌生人、人脸、私人文件、屏幕内容、药品、证件、家庭成员相关信息需要更高限制
- 用户确认只能提升长期候选资格，仍需经过 `Memory / WorldModel governance`

这意味着家庭场景不是普通 world observation 的一个小分支，而是必须有自己的隐私门槛。

## Object Identity Over Time

Luna 后续需要识别“同一个杯子、同一个包、同一个门、同一家店”，但当前只能做规划。

必须冻结：

- `object_identity_candidate` 不是事实
- 需要多次视觉一致性
- 需要位置 / 上下文一致性
- 可结合 OCR、用户命名、历史互动、记忆
- 家庭物品需要隐私治理
- 店铺 / 公共设施需要信息修正机制
- 用户确认可提升置信度
- 单次视觉识别不得直接写长期身份

它应当依附于 `WorldEntityFeatureCandidate` 与现有 handoff / memory / correction 结构，而不是独立造一个 identity runtime。

## Feedback-to-Focus Adaptation

用户反馈不是普通聊天，而是会改变视觉策略的控制信号。

诸如：

- “不是这个”
- “右边那个”
- “我看不到”
- “已经过马路了”
- “这里人太多”

都应能影响：

- `VisualFocusPlan`
- `VisualFocusSlot`
- tracking targets
- OCR targets
- map / memory hint weight
- task phase
- correction candidate
- scene sketch resampling

这也是为什么 `UserVisualFeedbackCandidate` 和 `FeedbackToFocusAdaptation` 都应纳入 preplan，而不是留到语音实现阶段再补。

## Strong Non-Claims

为了防止后续 phase 被误读，本 preplan 还需要一份更硬的非主张清单：

- 视角强化规划不等于视觉 runtime
- `Task-Aware Perception Orchestration` 不等于模型已接入
- `SceneSketch` 不等于环境事实
- `VisualFocusPlan` 不等于已经切割画面
- `SelectiveTrackingPolicy` 不等于 tracking runtime
- `Supervision / ByteTrack / OC-SORT` 仅候选，不等于已接入
- `WorldObservationLayer` 不等于世界模型写入
- `WorldEntityFeatureCandidate` 不等于对象事实
- 临时设施候选不等于固定 POI
- 人流跟随候选不等于导航指令
- crossing candidate 不等于允许过马路
- 文本 / OCR / 视觉候选不等于用户已经听见或看见
- 地图 / 记忆 hint 不等于现实事实
- 过期视觉观察不等于当前行动依据

## Preplan Readiness Gate

在这轮补充之后，preplan 的 readiness gate 应至少满足：

- existing module inventory 完成
- module reuse matrix 完成
- duplicate risk register 完成
- proposed architecture 完成
- P0 / P1 / P2 capability priority 完成
- scenario review 完成
- `resource budget` 归中台
- `privacy filtering` 归中台
- `correction / temporary facility / lifecycle / view quality / active perception` 均规划
- optical flow review 完成
- no runtime executed
- no new capability implemented
- no write occurred

同时必须继续保持以下 NO-GO 边界：

- 未做模块复用审计就建议新增模块
- 建议新建重复 `STC / TTL / Evidence / Memory / WorldModel`
- 建议直接接 tracking runtime
- 建议直接接地图 API
- 建议全量追踪
- 建议全图 OCR
- 建议直接写 `WorldModel / Memory / Fact`
- 建议把人流跟随作为导航指令
- 建议把 crossing candidate 作为过马路指令

## 推荐阶段顺序

1. `Phase-Return-To-Vision-Mainline-Planning-v1-001`
2. `Phase-MidPlatform-Perception-Orchestration-Policy-v1-001`
3. `Phase-Task-Aware-Visual-Focus-Policy-v1-001`
4. `Phase-World-Observation-and-Entity-Feature-Policy-v1-001`
5. `Phase-Selective-Tracking-Adapter-Policy-v1-001`
6. `Phase-Crossing-Decision-Safety-Governance-Policy-v1-001`
7. `Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001`
8. `Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001`

额外说明：

- `World Observation Layer` / `WorldEntityFeatureCandidate` 适合先做 policy，再决定是否进入独立 dry-run
- `Selective Tracking` 仍建议先 policy，不直接进入 tracking runtime
- `Crossing Decision Governance` 应独立成安全治理 phase，不应混入普通视觉对象 phase
- 当前不建议跳过 planning 直接进实现

## 当前 blocker 判断

无硬 blocker，但有几类前置澄清：

1. `TaskObservationRequest` 是扩展命名还是保持原名并新增 alias  
2. 当前 `vision_pipeline` 中 motion 逻辑哪些属于历史分支、哪些仍被视为可继承资产  
3. `World Observation Layer` 第一轮是否只保留 schema，不引入后台调度 dry-run  
4. `ResourceBudget` / `PrivacyFiltering` / `Correction` / `TemporaryFacility` 是否全部先收口到中台 policy 层  
5. `WorldEntityFeatureCandidate` 中哪些字段需要明确用户授权门槛  
6. `Crossing Decision Governance` 是否在正式 planning 后立即拆为单独 safety phase  
7. 家庭 / 私人空间中哪些对象可在用户确认后进入长期 candidate  
8. `ObjectIdentityOverTime` 第一轮是否只覆盖家庭物品和公共设施

## Deferred WorldModel / Memory / Library Boundary

当前视角强化主线不执行 `WorldModel / Memory / Library` 的深层治理。视觉主线只负责把候选材料采集干净、标注清楚、保留 `source_chain`、`TTL`、`freshness`、`location/pose/task context`、`privacy tags`、`confidence`、`uncertainty`、`conflict_refs` 和 `handoff route`。

当前只允许生成：

- `WorldObservationCandidate`
- `VisualObservationCandidate`
- `ExpiredVisualObservationCandidate`
- `WorldEntityFeatureCandidate`
- `ObjectIdentityCandidate`
- `TemporaryFacilityCandidate`
- `PerceptionCorrectionCandidate`
- `WorldModelHandoffCandidate`
- `MemoryHandoffCandidate`
- `LibraryHandoffPlaceholder`
- `ExperienceCandidatePlaceholder`

以下能力当前全部只允许 `placeholder / handoff / deferred`：

- `Entity Resolution / 实体融合`
- `Object Identity Over Time runtime / 长期对象身份确认 runtime`
- `WorldModel Fact Admission / 世界模型事实准入`
- `WorldModel Runtime Write / 世界模型真实写入`
- `Memory Consolidation / 长期记忆固化`
- `User Preference Fact Write / 用户偏好事实写入`
- `Emotional Attachment Fact Write / 情感挂载事实写入`
- `Library Experience Governance / 图书馆经验治理`
- `Experience Reuse Admission / 经验复用准入`
- `Long-term Route Experience Commit / 长期路线经验固化`
- `Social Facility Fact Commit / 社会设施事实提交`
- `Temporary Facility Long-term Promotion / 临时设施长期升级`

以下能力后续在 `Memory / WorldModel / Library` 专项中处理：

1. `Entity Fusion`
2. `Fact Admission`
3. `Long-term Memory Consolidation`
4. `Library Experience Governance`
5. `User Preference / Emotional Attachment Confirmation`
6. `Object Identity Over Time Confirmation`
7. `Temporary Facility Recurrence Promotion`
8. `Route Experience Formalization`
9. `WorldModel Query Runtime`

## 结论

本 preplan 已由正式 planning phase 接棒并冻结：

- `Phase-Return-To-Vision-Mainline-Planning-v1-001 = GO`

建议下一阶段更新为：

- `Phase-MidPlatform-Perception-Orchestration-Policy-v1-001`

不建议现在直接进入：

- 真实视觉 runtime
- 真实 tracking runtime
- 真实 OCR provider runtime
- 地图 API 接入
- 相机接入
- WorldModel / Memory / Fact 写入

本 preplan 的核心结论是：Luna 已经有足够多的中台/OCR/治理资产可以复用，下一阶段应该先把这些资产统一成 `Task-Aware Perception Orchestration` 的架构，而不是为视觉重新平行造一套系统。
