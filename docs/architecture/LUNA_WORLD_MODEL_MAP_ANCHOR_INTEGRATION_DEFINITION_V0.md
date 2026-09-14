# LUNA — Map / GPS / POI Anchor Integration Definition v0

## Phase

- **Phase-WorldModel-MapAnchor-001**

## Purpose

本阶段只定义：Map / GPS / POI 如何成为 `observed_where` / `spatiotemporal_binding` 的**外部空间锚点来源**。

MapAnchor 层不是核心感知主链，也不是导航规划层；它属于 **空间挂载与强化信息层（Attachment / Space Anchor Layer）**。
参照分层原则：

- `docs/architecture/LUNA_INFORMATION_COLLECTION_PROCESS_ATTACHMENT_LAYERING_PRINCIPLE_V0.md`

它只解决：

1. 当前观测发生在什么地理位置（geo-location）
2. 当前视觉/文字/对象证据属于哪个空间范围（scope）
3. 当前证据是否可绑定到地图 POI / 建筑 / 道路 / 室内区域
4. 地图/GPS/POI 与视觉锚点冲突时如何处理（不强行融合）
5. 哪些空间锚点可用于 WorldContextEvidence / WriteReadiness / Commit Layer
6. 哪些锚点只能作为 weak anchor / provisional anchor

## Non-governance boundary（强制）

- 不实现 runtime
- 不接真实地图 API
- 不规划路线
- 不推荐地点
- 不触发导航动作
- 不写世界模型事实
- 不上传蜂巢
- 不接推荐系统
- 不真实播报
- 不进入 SceneTask/Fusion/Output
- 不伪造 GPS（无 gps 输入不得填 lat/lng）

## Inputs & relationships（分层）

- YOLO/OCR（现场证据）：提供“现场存在/内容”
- SceneDelta：提供变化/替换/移除/重复判断（不写世界模型）
- WorldContextEvidence：统一包装证据候选（candidate-only）
- WriteReadiness：准入治理（candidate ≠ fact；provisional-first）
- **MapAnchor（本阶段）**：提供外部空间锚点候选（candidate-only），提升 observed_where 的可定位性

## Hard rule（地图不等于现场事实）

- 地图说有店 ≠ 现场一定存在
- 地图说路通 ≠ 当前一定可通行
- POI 名称 ≠ 当前视觉证据确认
- GPS 在某建筑附近 ≠ 用户就在该店内
- 室内楼层未知时不得推断楼层
- 地图过旧必须 stale / requires_revalidation
- 用户纠正必须标注来源与上下文，不得无验证覆盖
- 地图与视觉冲突必须标记 contradicted，不得强行融合

