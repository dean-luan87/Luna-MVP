# Phase-Fusion-001 — Map × Vision × Memory Fusion Signal Contract v0（融合输出契约冻结）

**目的**：冻结融合输出 contract，定义 `map_constraint_signal / vision_anchor_signal / memory_route_signal / fusion_decision_candidate` 的结构化字段，确保融合层输出可审计、可回放、且永不触发真实执行。  
**性质**：contract；candidate-only；不做世界模型。  

---

## 1) 总原则（写死）

- 输出必须结构化（JSON 可解析），不得只输出自然语言
- `fusion_decision_candidate.allows_execute_now` **必须恒为 false**
- 视角风险不得被地图或记忆覆盖（冲突策略由 conflict policy 写死）

---

## 2) signals（v0 写死 4 类）

### 2.1 map_constraint_signal

字段：
- `route_id`
- `macro_route_available`
- `route_segment_hint`
- `target_direction_hint`
- `distance_or_eta_hint`
- `map_confidence`
- `map_freshness`
- `map_limitation_reason`

### 2.2 vision_anchor_signal

字段：
- `local_scene_type`
- `passability_anchor`
- `risk_anchor`
- `ocr_anchor`
- `dynamic_event_anchor`
- `vision_confidence`
- `anchor_freshness`
- `anchor_reason`

### 2.3 memory_route_signal

字段：
- `memory_route_id`
- `matched_historical_route`
- `user_preference_hint`
- `historical_risk_hint`
- `repeated_task_match_score`
- `memory_confidence`
- `memory_freshness`
- `memory_limitation_reason`

### 2.4 fusion_decision_candidate

字段：
- `fusion_candidate_id`
- `active_scene_id`
- `active_task_id`
- `map_used`
- `vision_used`
- `memory_used`
- `conflict_detected`
- `conflict_type`（枚举）  
  - `map_vs_vision`
  - `memory_vs_vision`
  - `map_vs_memory`
  - `multi_source_conflict`
  - `none`
- `selected_basis`（枚举）  
  - `vision_anchor`
  - `map_macro_constraint`
  - `memory_optimizer`
  - `conservative_degraded`
  - `need_human_help`
- `candidate_action_type`（枚举）  
  - `continue`
  - `slow_down`
  - `stop`
  - `ask_for_help`
  - `reroute_candidate`
  - `orientation_check`
  - `wait`
- `confidence`
- `reason_codes`
- `allows_execute_now`（写死：false）

---

## 3) 最小封装建议（便于 trace/replay）

建议 v0 统一封装为：
- `fusion_signals_v0`：包含上述 4 类 signal
- `schema_version`：`fusion_signal_contract_v0`
- `source_attribution`：对 map/vision/memory 的来源与新鲜度摘要

