# LUNA — MapAnchor Integration Go/No-Go Pack v0

## Phase

- **Phase-WorldModel-MapAnchor-001**

## GO conditions（必须）

- `MapAnchorEvidence` schema 完整（candidate-only + governance 禁止项）
- observed_where binding policy 完整（source priority + 输出字段）
- “地图/GPS/POI 不等于现场事实”的硬规则明确
- conflict policy 完整（不强融 + require_revalidation）
- freshness/TTL 完整（gps_short/poi_medium/indoor_map_versioned/user_correction_requires_validation）
- spatial anchor grade 完整（A–E）
- observability requirements 完整（trace/replay/whitebox）
- 明确不实现 runtime、不接真实地图 API、不导航、不写世界模型、不蜂巢、不推荐、不播报

## CONDITIONAL_GO

- 某些 source_type（如 indoor_map / visual_map_alignment）仅定义占位，不影响合同闭合

## NO_GO（任意一条）

- 把地图 POI 当作现场事实
- 伪造 GPS（无输入仍填 lat/lng）
- 缺 freshness
- 缺 conflict policy
- 冲突时强行融合为 bound
- GPS/POI 直接触发导航动作
- 本阶段接真实地图 API
- 本阶段写世界模型/上传蜂巢/触发推荐或播报

