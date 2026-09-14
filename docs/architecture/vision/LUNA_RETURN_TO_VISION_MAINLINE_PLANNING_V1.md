# Luna — Return To Vision Mainline Planning v1

**Phase**：`Phase-Return-To-Vision-Mainline-Planning-v1-001`  
**性质**：formal planning / roadmap freeze / boundary freeze only  
**边界**：不实现 runtime，不接模型，不接相机，不接地图 API，不接 OCR provider，不接 tracking runtime，不写 `Memory` / `WorldModel` / `Fact`

## 目标

基于 `Return-To-Vision Mainline Preplan v1` 的审计与规划结果，把 Luna 视角强化主线从 preplan 草案正式冻结为工程路线图，并明确：

- 视角强化主线的正式目标
- 被采纳的主线原则
- 必须复用的既有模块
- 明确禁止新建的平行体系
- 第一批正式 phase 顺序
- 哪些能力属于 `P0 / P1 / P2`
- 哪些能力当前只允许 `policy / schema / dry-run`
- 哪些能力明确禁止 runtime
- 视觉、OCR、语音、中台、地图、记忆如何形成闭环
- 下一阶段正式进入哪个 policy phase

## 正式主线名称

Luna 视角强化主线正式名称冻结为：

- `Task-Aware Perception Orchestration`
- 任务感知型感知编排

正式主线目标冻结为：

- 中台统一编排视觉 / OCR / 地图 / 记忆 / 任务 / 安全信息
- 全链保持 `candidate-only / no-write / reuse-first`
- 先冻结治理边界与 phase 路线，再进入任何 policy / dry-run

## 采纳的 preplan 结论

本阶段正式采纳以下 preplan 结论：

1. `3x3` 固定画面切割不再是主线
2. 不做 `full-scene tracking`
3. 中台拥有感知编排权
4. `Safety Lane` always-on，但只出 candidate
5. `Task Lane` 只处理中台批准的 focus slots
6. OCR 只允许 `focus-triggered`，不允许 `full-frame OCR`，不允许真实 provider runtime
7. 地图 / 路线 / 位置 / 记忆只作为 `context hint`
8. 视觉观察允许归档，但过期候选不得作为当前行动依据
9. `World Observation Layer` 是后台低频候选层，不是实时行动模块
10. `WorldEntityFeatureCandidate` 只允许 candidate / handoff，不允许 fact write
11. `Resource Budget` 归中台
12. `Privacy Filtering` 归中台
13. 必须预留 `Information Correction / Reality Mismatch`
14. `Temporary / Mobile Social Facility` 必须 TTL 化
15. `Crossing Decision` 未来必须独立 safety governance
16. `Supervision / ByteTrack / OC-SORT / optical flow` 当前只允许 future adapter / evidence 候选
17. `WorldModel / Memory / Library` 深层治理全部 deferred；当前视觉主线只生成 handoff candidate / placeholder，不执行 entity fusion / fact admission / memory consolidation / library experience governance
18. `Reuse First, Extend Second, Create Last`

## 正式拒绝的模式

以下模式被正式标记为主线 rejected patterns：

- `3x3 grid as mainline`
- `full-scene tracking`
- `full-frame OCR`
- 地图 / 记忆作为行动权威
- 视觉直写 `WorldModel / Memory / Fact`
- 视觉私有 `ResourceBudget`
- 视觉私有 `PrivacyFiltering`
- 新建平行 `STC / TTL / source_chain`
- 新建平行 `Evidence Pack`
- 新建平行 `Task State`
- 新建平行 `Speech Gate / VOP`
- 新建平行 `Runtime Trial / Closure framework`
- 把 `Crossing Decision` 当成普通视觉子任务
- 把 `CrowdFlowFollowingCandidate` 当成直接导航指令

## 正式复用承诺

本阶段冻结以下复用承诺：

- `Task Observation Request Contract v1`
- `Task Manager / Task State`
- `Safety-Task Arbitration`
- `STC Sampling Guidance`
- `OCR Activation / OCRRequest / readable region / Evidence / TTL / source_chain`
- `Vision Frame / ROI / Evidence Pack`
- `WorldModel unresolved observation slot / lookup`
- `Memory governance`
- `MapAnchor`
- `System Health`
- `Hardware Profile / Resource Gate`
- `Minimal Runtime Integration patterns`
- `OCR Closure boundary patterns`
- `Speech Gate / VOP output boundary`

## Duplicate Module Ban List

以下平行体系被正式禁止新建：

- `new STC`
- `new TTL / freshness`
- `new source_chain`
- `new Evidence Pack`
- `new Memory write path`
- `new WorldModel write path`
- `new Fact write path`
- `new Task State`
- `new Speech Gate / VOP`
- `new Runtime Trial / Closure framework`
- `new standalone resource budget outside MidPlatform`
- `new standalone privacy filtering outside MidPlatform`

## Governance Boundary Matrix

本阶段冻结以下 runtime / write 边界：

- `camera runtime allowed=false`
- `OCR provider runtime allowed=false`
- `tracking runtime allowed=false`
- `optical flow runtime allowed=false`
- `map API allowed=false`
- `memory write allowed=false`
- `worldmodel write allowed=false`
- `fact write allowed=false`
- `scene delta allowed=false`
- `navigation action allowed=false`
- `task commit allowed=false`
- `full-frame OCR allowed=false`
- `full-scene tracking allowed=false`

## Vision Mainline Roadmap

### P0 capability group

- `MidPlatformPerceptionWorkOrder`
- `TaskPhasePerceptionPolicy`
- `SceneSketchCandidate`
- `VisualFocusPlan / VisualFocusSlot`
- `MidPlatformResourceBudgetPolicy`
- `VisualObservationLifecycle`
- `ViewQualityGate`
- `PerceptionConflict / Correction`

### P1 capability group

- `SelectiveTrackingPolicy`
- `OCRFocusActivation`
- `WorldObservationLayer`
- `Temporary / Mobile Social Facility`
- `UserVisualFeedbackCandidate`
- `MidPlatformPrivacyFilteringPolicy`

### P2 capability group

- `WorldEntityFeatureCandidate`
- `ObjectIdentityOverTime`
- `EmotionalAttachmentCandidate`
- `OpticalFlow / MotionEvidence`
- `CrowdFlowFollowingCandidate`
- `EvaluationMetrics`

## First Batch Phase Definitions

### A. `Phase-MidPlatform-Perception-Orchestration-Policy-v1-001`

冻结中台感知编排总原则，定义 `MidPlatformPerceptionWorkOrder`、`TaskPhasePerceptionPolicy`、`Safety Lane / Task Lane`、`ResourceBudget` 与 `PrivacyFiltering` 的中台归属。

### B. `Phase-Task-Aware-Visual-Focus-Policy-v1-001`

定义 `SceneSketchCandidate`、`VisualFocusPlan`、`VisualFocusSlot`、`ActiveViewAdjustmentCandidate`、`ViewQualityGate`、`VisualFocus lifecycle`。

### C. `Phase-World-Observation-and-Entity-Feature-Policy-v1-001`

定义 `World Observation Layer`、`WorldEntityFeatureCandidate`、`Object/Place/Event/Relation/Facility/TemporaryFacility` 属性框架、`WorldModel handoff candidate`。

### D. `Phase-Selective-Tracking-Adapter-Policy-v1-001`

定义选择性追踪策略，限制 `full-scene tracking`，规划 `road / pedestrian / vehicle / crowd flow tracking`，并把 `Supervision / ByteTrack / OC-SORT` 限定为 future adapter candidates。

### E. `Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001`

用模拟任务验证视觉 / OCR / 地图 / 记忆 / 任务信息如何生成 `TaskFeedbackCandidate / SafetyFeedbackCandidate`。

### F. `Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001`

把视觉候选、OCR 候选、地图 / 任务上下文接入基础导航闭环 dry-run，仍不进入真实 runtime。

## Deferred Capability Register

明确暂缓：

- `real camera runtime`
- `real OCR provider`
- `real tracking runtime`
- `Supervision runtime integration`
- `ByteTrack / OC-SORT runtime`
- `optical flow runtime`
- `map API / 高德 API`
- `Entity Resolution runtime`
- `Object Identity Over Time runtime confirmation`
- `WorldModel Fact Admission`
- `WorldModel write`
- `WorldModel Query Runtime`
- `Memory Consolidation`
- `Memory write`
- `User Preference Fact Write`
- `Emotional Attachment Fact Write`
- `Library Experience Governance`
- `Experience Reuse Admission`
- `Long-term Route Experience Commit`
- `Social Facility Fact Commit`
- `Temporary Facility Long-term Promotion`
- `Fact write`
- `Scene Delta commit`
- `real TTS / audio`
- `face recognition`
- `voiceprint`
- `facial expression / audio emotion`
- `full background recording`
- `crossing action instruction`

## Vision Mainline Non-Claims

本阶段必须明确：

- planning 不等于 runtime
- `Task-Aware Perception Orchestration` 不等于模型已接入
- `Perception Work Order` 不等于真实视觉调度已执行
- `Scene Sketch` 不等于环境事实
- `VisualFocusPlan` 不等于已经真实切割画面
- `SelectiveTrackingPolicy` 不等于追踪 runtime
- `World Observation` 不等于 `WorldModel` 写入
- `WorldEntityFeatureCandidate` 不等于实体事实
- `TemporaryFacilityCandidate` 不等于固定 POI
- `CrowdFlowFollowingCandidate` 不等于导航指令
- `CrossingCandidate` 不等于允许过马路
- `Map / Memory hint` 不等于现实事实
- `OCR focus-triggered` 不等于 OCR provider runtime
- `text-only / candidate` 输出不等于真实用户听见
- `WorldModelHandoffCandidate` 不等于已经写入 `WorldModel`
- `MemoryHandoffCandidate` 不等于已经写入 `Memory`
- `LibraryHandoffPlaceholder` 不等于图书馆经验已生效
- `ObjectIdentityCandidate` 不等于长期对象身份事实
- `EmotionalAttachmentCandidate` 不等于用户情感事实
- `ExperienceCandidatePlaceholder` 不等于经验已复用准入

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

## Formal Readiness Gate

GO 条件：

- preplan loaded
- OCR closure loaded
- Minimal Runtime Integration closure loaded
- adopted principles generated
- roadmap generated
- reuse commitment generated
- duplicate ban list generated
- boundary matrix generated
- first batch phase definitions generated
- deferred capability register generated
- deferred worldmodel memory library boundary generated
- worldmodel memory library placeholder plan generated
- non-claims generated
- entity resolution deferred
- fact admission deferred
- memory consolidation deferred
- library experience governance deferred
- no runtime executed
- no write occurred
- next phase fixed

NO-GO 条件：

- 未加载 preplan / OCR closure / Minimal Runtime Integration closure
- 建议直接 runtime
- 建议全量 tracking
- 建议全图 OCR
- 建议直接接地图 API
- 建议直接写 `WorldModel / Memory / Fact`
- 建议在视觉主线内执行 `Entity Resolution / Fact Admission / Memory Consolidation / Library Experience Commit`
- 建议新建重复 `STC / TTL / Evidence / Memory / Task / Speech / runtime framework`
- 未明确下一阶段

## 最终结论

`Return-To-Vision Mainline Planning v1` 完成后，Luna 从“前置规划”正式进入“视觉主线规划冻结”。

本阶段的最终决定应为：

- `RETURN_TO_VISION_MAINLINE_PLANNING_READY_FOR_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY`

推荐下一阶段固定为：

- `Phase-MidPlatform-Perception-Orchestration-Policy-v1-001`

注意：下一阶段仍然是 `policy`，不是 runtime。第一刀切中台，不切视觉算法。

后续状态更新：

- `Phase-MidPlatform-Perception-Orchestration-Policy-v1-001 = GO`
- `Phase-Task-Aware-Visual-Focus-Policy-v1-001 = GO`
- 当前推荐下一阶段：`Phase-World-Observation-and-Entity-Feature-Policy-v1-001`
