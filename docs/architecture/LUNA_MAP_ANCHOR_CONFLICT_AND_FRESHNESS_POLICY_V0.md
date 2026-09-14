# LUNA — MapAnchor Conflict & Freshness Policy v0

## Phase

- **Phase-WorldModel-MapAnchor-001**

## Purpose

定义 MapAnchor 的冲突处理与 freshness/TTL 规则：

- Map/GPS/POI 与视觉锚点冲突时不强融
- 锚点也会过期（GPS 秒级；POI 天/周/月级；室内图版本化）

## MapAnchorConflict（v0）

```json
{
  "map_anchor_conflict_id": "map_conflict_001",
  "conflict_type": "gps_vs_map | map_vs_visual | poi_vs_ocr | user_vs_map | indoor_floor_conflict | stale_map_data",
  "source_refs": [],
  "conflict_status": "detected | under_review | resolved | unresolved",
  "preferred_source_policy": "vision_first_for_current_scene | map_for_static_geo | user_correction_requires_validation | hold_uncertain",
  "decision": "hold_uncertain | weak_bind | use_visual_anchor | use_map_anchor | require_revalidation",
  "navigation_action": null,
  "world_model_write_invoked": false
}
```

## Default priority（v0）

- 当前现场安全/通行：**vision first**
- 静态地理位置锚点：map/GPS 可作为 anchor
- 店铺是否营业/存在：必须依赖现场证据 + 时间复核（地图不等于现场事实）
- 用户纠正：高价值，但必须标注来源与上下文，且可进入 human validation

## Freshness / TTL（v0）

- GPS fix：秒级/分钟级（`gps_short`）
- POI 静态信息：天/周/月级（`poi_medium`，按类别）
- 店铺营业/促销：短 TTL（short_ttl + revalidation）
- 室内地图：版本化（`indoor_map_versioned`）
- 用户纠正：必须带时间戳与来源（`user_correction_requires_validation`）

## Hard rules

- 冲突未解：不得强行融合；必须 `hold_uncertain` 或 `require_revalidation`
- stale：必须标记 `stale` 并触发 revalidation，不得当作当前事实

