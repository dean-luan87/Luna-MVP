# LUNA — World Change Observation Policy v0

## Phase

- Phase-WorldModel-ContextEvidence-001

## Purpose

定义：当世界在时间推移中发生变化（拆迁/施工/开业/关店/道路可通行/人流变化/服务可用性变化等）时，
世界证据层如何记录 `WorldChangeEvent` 与其对后续证据的影响（占位）。

本合同强调：
1) 变化是可观测事件链，不是静态地图；
2) 每个事件都必须绑定时空锚点与信任度；
3) 变化事件可以“影响任务规划/推荐”（占位），但本阶段只定义合同，不做推荐实现。

## Non-governance boundary

- 不实现 runtime。
- 不接任务执行/导航动作/推荐系统。

## WorldChangeEvent（主结构）

```json
{
  "change_type": "demolition | construction | opening | closing | renovation | road_available | road_blocked | crowd_increase | service_available",

  "previous_state_ref": "world_state_ref_prev",
  "current_state_ref": "world_state_ref_curr",

  "observed_at": {
    "timestamp_ms": 0,
    "time_source": "midplatform_clock",
    "date_confidence": "system_confirmed"
  },

  "observed_where": {
    "spatial_anchor_type": "gps | map_poi | visual_landmark | indoor_scene | unknown",
    "place_hint": "某商场一楼",
    "geo_location": { "lat": null, "lng": null, "accuracy_m": null }
  },

  "confidence": 0.0,
  "impact_on_navigation": "none | weak | medium | strong",
  "impact_on_recommendation": "none | weak | medium | strong"
}
```

## Evidence_status 与变化链（占位规则）

在同一空间锚点（或其合理邻域）上观察到变化时：
- 将旧证据标记为 `superseded/expired`
- 将新证据标记为 `active`
- 若观测冲突：标记 `contradicted` 并要求后续复核（requires_revalidation=true）

变化链示例（只作为语义占位）：
- 拆迁 -> 空地 -> 施工 -> 招商围挡 -> 店铺装修 -> 新店开业 -> 人流出现 -> 用户评价积累 -> 任务推荐路径改变

