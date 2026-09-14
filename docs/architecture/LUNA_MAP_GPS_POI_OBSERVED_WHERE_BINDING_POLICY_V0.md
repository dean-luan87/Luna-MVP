# LUNA — Map/GPS/POI → ObservedWhere Binding Policy v0

## Phase

- **Phase-WorldModel-MapAnchor-001**

## Purpose

定义 Map/GPS/POI 进入 `WorldContextEvidence.observed_where` 与 `spatiotemporal_binding.observed_where` 的绑定规则（只定义，不接真实地图 API）。

## ObservedWhere source priority（v0）

1. **gps_precise_anchor**
   - 条件：`accuracy_m` 足够小、时间新鲜、且未与视觉冲突
   - 结果：`spatial_anchor_type=gps`，`anchor_status=bound`

2. **map_poi_anchor**
   - 条件：POI 与 GPS/视觉/用户任务一致
   - 结果：`spatial_anchor_type=map_poi`，`anchor_status=bound | weakly_bound`

3. **indoor_map_anchor**
   - 条件：室内地图、楼层、区域可靠（不推断未知楼层）
   - 结果：`spatial_anchor_type=indoor_scene`（或未来扩展 indoor_zone），并记录 `floor_level/indoor_zone_id`

4. **visual_map_alignment_anchor**
   - 条件：视觉地标与地图 POI 可对齐（hybrid）
   - 结果：`spatial_anchor_type=visual_landmark + map_poi hybrid`（v0 可用 observed_where_source 描述）

5. **user_corrected_location_anchor**
   - 条件：用户明确纠正位置
   - 结果：必须标注 `source_type=user_corrected_location`，并进入 Human Interaction Validation Layer（truth-type + 审计），不得无验证覆盖

6. **unknown / weak anchor**
   - 条件：GPS 漂移、POI 不确定、冲突未解
   - 结果：`anchor_status=weakly_bound | unresolved`，`requires_revalidation=true`

## Binding outputs（写入 observed_where 的字段）

绑定时应生成/填充：

- `observed_where.geo_location`（仅当真实 gps 输入存在）
- `observed_where.place_hint`（可空；不得伪造）
- `observed_where.spatial_anchor_type`（gps/map_poi/indoor_scene/unknown）
- `observed_where.relative_position`（可空）
- `spatiotemporal_anchor_ref`（若有 SceneDelta/视觉锚点则与 map anchor 交叉引用；MapAnchor 本身不伪造 scene anchor）
- `spatial_scope`（point/region/route_segment/indoor_zone/storefront/building）
- `observed_where_source`（gps_precise_anchor/map_poi_anchor/...）
- `spatial_anchor_confidence`（占位允许）

## Hard rules（强制）

- 不得把 POI/地图当作现场事实
- 不得伪造 GPS（无输入不填 lat/lng）
- 地图/视觉冲突时必须标记 `contradicted` 并 `requires_revalidation=true`

