# 主线 2 第二阶段 M1.5：局部空间标尺层交付说明

**依据**：`docs/LOCAL_SPATIAL_SCALE_CONSTITUTION.md` v1.0（冻结）  
**范围**：仅标尺层落地，不做关系化、3D、全局地图、语义拓扑实现。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/local_goal_spatial_map.py` | BASE_SECTORS（去掉 near_front）、DISTANCE_BANDS/OFFSET_BANDS/SPEED_BANDS/SCENE_PROFILES；SpatialRegion 新增 relative_bearing_deg、distance_cm、staleness_ms、distance_band、offset_band；LocalGoalSpatialMap 新增 scene_profile |
| `decision_monitor/local_goal_spatial_map_builder.py` | 仅用 BASE_SECTORS；近场用 front + distance_band=immediate/near；_mk 写入精确/派生标尺；_scene_profile_from_state、_build_spatial_scale、build_spatial_scale；所有 region 写入 bearing/distance/distance_band/offset_band |
| `decision_monitor/schema.py` | 新增 SpatialScaleContext；DecisionMonitorFrame 新增 spatial_scale |
| `decision_monitor/builder.py` | 调用 build_spatial_scale，将 spatial_scale 写入 frame |
| `runtime/context.py` | 新增 effective_body_width_cm、effective_body_height_cm、clearance_required_cm、forward_speed_cm_s、speed_band、reaction_horizon_ms |
| `main.py` | monitor_ctx 增加上述 6 个标尺字段（从 runtime_ctx 读取，未设则 builder 用默认） |
| `tools/decision_monitor_viewer.py` | regionLine 展示 relative_bearing_deg、distance_cm、distance_band、offset_band；新增标尺层卡片；sections 增加 spatial_scale |
| `decision_monitor/CONTRACT.md` | M1.5 字段与预留说明 |
| `tests/test_decision_monitor.py` | sector 合规改为 BASE_SECTORS；近场断言改为 front + distance_band=immediate；新增 test_m15_no_near_front_as_base_sector、test_m15_spatial_scale_present_and_defaults |

---

## 2. M1.5 落地字段清单

### 2.1 SpatialRegion（每区域）

| 字段 | 宪法对应 | 说明 |
|------|----------|------|
| relative_bearing_deg | 3.1 | 相对当前行动前向，度 |
| distance_cm | 3.2 | 厘米 |
| ttl_ms | 3.4 | 已有，对齐宪法 |
| staleness_ms | 3.4 | 陈旧度 |
| stability_score | 3.5 | 已有，对齐宪法 |
| distance_band | 4.2 | immediate / near / mid / far |
| offset_band | 4.3 | aligned / slight_offset / moderate_offset / strong_offset |
| sector | 4.1 | 仅 BASE_SECTORS：front / front_left / front_right / left / right / rear |

### 2.2 LocalGoalSpatialMap

| 字段 | 说明 |
|------|------|
| scene_profile | outdoor / indoor |

### 2.3 SpatialScaleContext（frame.spatial_scale）

| 字段 | 宪法对应 | 说明 |
|------|----------|------|
| scene_profile | 5 节双 Profile | outdoor / indoor |
| effective_body_width_cm | 4.7 / 7 节 | 默认 70 |
| effective_body_height_cm | 4.7 / 7 节 | 默认 profile 170 |
| clearance_required_cm | 4.7 / 7 节 | 宽度+余量 |
| forward_speed_cm_s | 3.6 | 当前占位，优先平滑速度原则已写入文档 |
| speed_band | 4.6 | stopped / slow / normal / fast |
| reaction_horizon_ms | 4.6 | 规则型派生 |

---

## 3. scene_profile 最小规则说明

- **来源**：`state.scene_type` 与 ctx。`close_range` / `stationary` → **indoor**；`normal_walk` / `cautious` → **outdoor**；缺省 **outdoor**；ctx 可传 `scene_profile` 覆盖。
- **使用**：LocalGoalSpatialMap.scene_profile 与 SpatialScaleContext.scene_profile 一致；室外优先依据 relative_bearing_deg 做方向性表达，室内保守、强调大方向与区域覆盖（逻辑预留，未在本轮实现偏航/解释差异）。

---

## 4. 用户物理包络最小接入说明

- **写入链**：runtime_ctx（effective_body_width_cm、effective_body_height_cm、clearance_required_cm）→ monitor_ctx → builder → SpatialScaleContext。
- **默认**：未设时 effective_body_width_cm=70（宪法 default_effective_body_width_cm）；effective_body_height_cm=170；clearance_required_cm=effective_body_width_cm+20。
- **展示**：Viewer 标尺层卡片与 sections 中 spatial_scale 可见；不要求本轮个体化学习，仅形成可引用链路。

---

## 5. 速度接入说明

- **写入链**：runtime_ctx（forward_speed_cm_s、speed_band、reaction_horizon_ms）→ monitor_ctx → builder → SpatialScaleContext。
- **默认**：未设时 forward_speed_cm_s=0，speed_band=stopped，reaction_horizon_ms=200；非 stopped 时 reaction_horizon_ms=500。
- **原则**：宪法“优先使用平滑后的有效推进速度”已在 CONTRACT/宪法中体现；当前无平滑速度实现，为占位；可选预留 raw_forward_speed_cm_s / smoothed_forward_speed_cm_s 未在本轮接入主链。

---

## 6. 样本运行结果（测试）

```text
tests/test_decision_monitor.py::test_local_goal_spatial_map_present_and_sectors_valid PASSED
tests/test_decision_monitor.py::test_local_goal_spatial_map_changes_by_goal PASSED
tests/test_decision_monitor.py::test_m15_no_near_front_as_base_sector PASSED
tests/test_decision_monitor.py::test_m15_spatial_scale_present_and_defaults PASSED
```

- 所有区域 sector ∈ BASE_SECTORS，无 near_front。
- 近场（detector_floor_due）→ focus sector=front，distance_band=immediate。
- frame.spatial_scale 存在，effective_body_width_cm=70，speed_band ∈ {stopped, slow, normal, fast}，scene_profile ∈ {outdoor, indoor}。

---

## 7. 宪法字段：已落地 vs 预留

| 宪法条款 | 已落地 | 预留 |
|----------|--------|------|
| 3.1 方向主单位 | relative_bearing_deg 写入区域 | heading_deg_360 未入 region（仅路径反演用） |
| 3.2 距离主单位 | distance_cm | — |
| 3.4 时间 | ttl_ms、staleness_ms | — |
| 3.5 质量 | confidence、stability_score | — |
| 3.6 速度 | forward_speed_cm_s、speed_band、reaction_horizon_ms | raw/smoothed 双字段未接入 |
| 3.7 路径增量 | — | delta_heading_deg、delta_distance_cm、path_segment_id、turn_type、anchor_point_id |
| 4.1 方向扇区 | sector 仅 BASE_SECTORS | — |
| 4.2 距离带 | distance_band | — |
| 4.3 偏移带 | offset_band | — |
| 4.6 速度派生 | speed_band、reaction_horizon_ms | — |
| 4.7 有效通过 | effective_body_*、clearance_required_cm | clearance_cm、safety_margin_cm 未接入 |
| 4.8 动态 | — | relative_velocity_cm_s、ttc_ms |
| 4.9 质量修正 | — | effective_spatial_resolution_cm |
| 5 节 双 Profile | scene_profile 最小接入 | 偏航/解释策略未实现 |

---

## 8. 本轮是否通过

- **是**。验收满足：  
  1）宪法最小精确标尺字段已进入 SpatialRegion / state（通过 frame.local_goal_spatial_map 与 frame.spatial_scale）及 Viewer；  
  2）最小派生标尺 sector / distance_band / offset_band 可生成且合规（仅 BASE_SECTORS，无 near_front）；  
  3）scene_profile 已最小接入并区分 indoor/outdoor；  
  4）用户物理包络最小字段已进入链路并可显示；  
  5）速度最小字段已进入链路并可显示；  
  6）未破坏主线 A、主线 2 第一阶段、M0、M1 既有链路（相关单测通过）。
