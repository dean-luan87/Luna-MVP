# Phase-SceneTask-001 — Core Scene State Machine v0（状态机冻结）

**目的**：冻结核心场景状态机（4 场景 + uncertain/degraded），以及统一 `scene_state` 字段集合，供任务链桥接与回放审计使用。  
**性质**：state machine definition；只输出 candidate；不得触发真实执行。  

---

## 1) 统一 scene_state（字段写死）

每次状态机输出必须包含至少以下字段：
- `scene_id`
- `scene_type`
- `scene_confidence`
- `scene_phase`
- `active_task_id`
- `task_status`
- `inserted_task_present`
- `recovery_possible`
- `deviation_detected`
- `degraded_mode`
- `required_perception_signals`
- `last_transition_reason`

---

## 2) Scene Types（写死）

- `sidewalk_navigation`
- `road_crossing`
- `metro_navigation`
- `hospital_navigation`
- `uncertain_scene`
- `degraded_scene`

---

## 3) Sidewalk — sidewalk_navigation phases（建议最小集合）

- `observing_path`
- `moving_forward`
- `obstacle_detected`
- `passability_uncertain`
- `slow_down_or_stop`
- `recover_to_moving`

---

## 4) Road Crossing — road_crossing phases（candidate-only）

注意：本阶段只输出 candidate，不做真实放权通行判断。

- `approaching_crossing`
- `waiting`
- `crossing_allowed_candidate`
- `crossing_in_progress`（仍是“任务链候选阶段”，不代表真实执行）
- `crossing_blocked_or_unsafe`
- `completed`

---

## 5) Metro — metro_navigation phases（candidate-only）

- `station_entry`
- `sign_reading`
- `direction_candidate`
- `platform_candidate`
- `transfer_candidate`
- `exit_candidate`
- `uncertain_or_need_help`

---

## 6) Hospital — hospital_navigation phases（candidate-only）

- `hospital_entry`
- `registration_or_consultation_candidate`
- `department_direction_candidate`
- `floor_or_room_candidate`
- `waiting_area_candidate`
- `uncertain_or_need_help`

---

## 7) Uncertain/Degraded（写死语义）

### uncertain_scene
- 场景分类不确定或信号不足
- 允许输出 “need_human_help_candidate / observe / ask_for_help” 类候选

### degraded_scene
- 低置信度或风险高时进入
- 必须保持保守（不强行动作）

