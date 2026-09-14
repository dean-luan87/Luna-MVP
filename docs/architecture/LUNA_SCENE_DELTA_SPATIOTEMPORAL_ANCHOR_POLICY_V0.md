# LUNA — Scene Delta Spatiotemporal Anchor Policy v0

## Phase

- **Phase-MidPlatform-SceneDelta-001**

## Purpose（本阶段只做定义）

将“时空锚点（Spatiotemporal Delta Anchor）”提升为 Scene Delta 的**主机制**：在同一个时空锚点上判断信息的重复、替换、消失、新增、过期、冲突。

没有时空间信息时，Scene Delta 只能做“文本去重”；有了时空间信息，才能表达“固定空间节点上的内容演替”，并支撑世界变化分析。

## Why spatiotemporal anchor is mandatory（写死）

Scene Delta 必须支持：

1. 同一空间位置上的内容变化
2. 同一对象在不同时间的状态变化
3. 同一文本在不同位置的重复出现
4. 同一位置上信息的新增、消失、替换、过期
5. 固定信息载体的长期变化轨迹（变化频率、复查建议）

典型对象（示例）：

- 海报栏/公告栏/电梯屏/地铁广告屏
- 商铺招牌/活动牌/菜单牌/价格牌
- 施工告示/招商围挡/临时路牌/导视牌

## SpatiotemporalDeltaAnchor（冻结 schema）

```json
{
  "spatiotemporal_anchor_id": "sta_001",
  "anchor_type": "fixed_surface | movable_object | storefront | signboard | screen | poster_board | notice_board | indoor_zone | outdoor_region | unknown",

  "spatial_scope": {
    "geo_location": { "lat": null, "lng": null, "accuracy_m": null },
    "place_hint": "unknown",
    "visual_landmark_ref": null,
    "relative_position": { "direction_hint": null, "distance_estimate_m": null },
    "region_bbox": null,
    "spatial_confidence": 0.0
  },

  "temporal_scope": {
    "first_seen_at": null,
    "last_seen_at": null,
    "observation_window_id": null,
    "seen_count": 1
  },

  "anchor_signature": {
    "spatial_signature": null,
    "carrier_signature": null,
    "layout_signature": null,
    "content_signature": null
  },

  "stability_profile": {
    "position_stability": "stable | drifting | unknown",
    "content_stability": "stable | changing | frequently_changing | unknown",
    "expected_update_frequency": "rare | daily | weekly | seasonal | unknown"
  }
}
```

## Carrier & content semantics（写死）

### 固定空间节点的内容演替（poster_board 示例）

同一个海报栏位置：

- 4/1：电影A
- 4/10：电影B
- 4/20：促销广告
- 4/30：招聘启事

这属于 **同一 anchor（same_place）上的内容替换（content_replaced）**，并非“OCR 结果变化”那么简单。

Scene Delta 必须能够产出：

- 这里是信息更新频繁的位置（frequently_changing_surface）
- 某条旧信息已下架（content_removed/expired）
- 某条新信息刚出现（new_content_same_place）
- 这个位置值得低频周期性复查（expected_update_frequency）

## Non-governance boundaries（硬边界）

- 不实现 runtime
- 不写真实世界模型事实
- 不接真实中台/不进下游
- 不执行导航动作/不真实播报

