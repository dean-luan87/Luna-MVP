# Phase-Perception-001 — Navigation Perception Signal Contract v0（输出契约冻结）

**目的**：冻结感知输出 contract，要求输出结构化 signal，避免后续任务链直接消费不稳定原始视觉结果。  
**性质**：contract；允许 mock/fixture/replay 验证；不要求工业级性能。  

---

## 1) 总原则（写死）

- 输出必须结构化（JSON 可解析），不得只输出自然语言描述
- 允许 unknown/低置信度，但不得强行给高确定结论
- 每个 signal 都必须携带可追踪的 `timestamp_or_frame_id`（或等价字段）
- 每个 signal 都必须携带 `confidence`

---

## 2) Signal 类型（v0 写死 5 类）

### 2.1 object_stability_signal

字段：
- `object_id`
- `object_type`
- `frame_span`
- `stability_score`
- `tracking_status`
- `lost_or_reappeared`
- `confidence`
- `timestamp_or_frame_id`

### 2.2 ocr_navigation_signal

字段：
- `text`
- `text_type`（枚举，至少包含）  
  - `sign`
  - `doorplate`
  - `floor_number`
  - `direction_board`
  - `bus_line`
  - `metro_direction`
  - `traffic_light_countdown`
  - `hospital_department`
- `location_hint`
- `navigation_relevance`
- `confidence`
- `source_frame_id`

### 2.3 spatial_passability_signal

字段：
- `passable`
- `passability_score`
- `estimated_distance_level`（near/mid/far/unknown）
- `obstacle_direction`
- `width_or_clearance_hint`
- `confidence`
- `risk_reason`

### 2.4 dynamic_event_signal

字段：
- `event_type`（枚举，至少包含）  
  - `pedestrian_moving`
  - `vehicle_approaching`
  - `traffic_light_changed`
  - `elevator_door_open_close`
  - `crowd_flow_changed`
  - `object_approaching`
- `direction`
- `urgency_level`
- `confidence`
- `temporal_window`

### 2.5 risk_field_signal

字段：
- `risk_type`（枚举，至少包含）  
  - `obstacle`
  - `vehicle`
  - `crowd`
  - `step`
  - `edge`
  - `water`
  - `construction`
  - `unknown`
- `risk_zone`（immediate/near/mid/far）
- `risk_level`（low/medium/high/critical）
- `trigger_reason`
- `recommended_handling`（observe/warn/slow_down/stop/ask_for_help）
- `confidence`

---

## 3) 最小输出包络（建议统一封装）

建议 v0 统一封装为：
- `perception_signals_v0`：包含上述 5 类 signal 的列表/分组
- `source_id`：数据来源（mock/fixture/replay/real）
- `schema_version`：`perception_signal_contract_v0`

---

## 4) 明确声明

- 本 contract 不要求工业级性能/鲁棒性  
- 本 contract 只冻结结构化输出面，不引入任务链/地图融合  

