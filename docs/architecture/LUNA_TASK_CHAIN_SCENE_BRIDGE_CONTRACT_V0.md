# Phase-SceneTask-001 — Task Chain × Scene Bridge Contract v0（桥接契约冻结）

**目的**：定义 perception signals → scene_state → task chain candidates 的桥接契约，写死“只产生候选，不得直接执行”。  
**性质**：contract；不做地图融合；不做模型放权；不触发真实执行。  

---

## 1) 硬约束（写死）

1. perception signal **只能形成** scene/task **candidate**  
2. perception signal **不得直接触发**真实 execute / retry / reopen / release  
3. scene transition 必须可审计（必须输出 `last_transition_reason` 与证据摘要）  
4. task status 必须可回放（状态变化必须可记录）  
5. inserted task 不得覆盖主任务，除非显式替换（v0 默认不允许覆盖）  
6. pause/resume/cancel/recover 必须统一状态机语义（见任务状态）  
7. deviation detection 只产生纠偏 candidate，不得强制执行  

---

## 2) 任务状态（v0 写死）

task status 枚举至少包含：
- `inactive`
- `active`
- `paused`
- `interrupted`
- `inserted`
- `recovering`
- `completed`
- `cancelled`
- `lost`
- `degraded`

transition reason 枚举至少包含：
- `perception_signal_update`
- `user_interruption`
- `user_resume`
- `deviation_detected`
- `low_confidence`
- `risk_signal_detected`
- `inserted_task_started`
- `inserted_task_completed`
- `scene_uncertain`
- `need_human_help`

---

## 3) 消费输入（perception signals）

桥接输入仅允许消费 Perception-001 contract 冻结的 5 类 signals（结构化）：
- `object_stability_signal`
- `ocr_navigation_signal`
- `spatial_passability_signal`
- `dynamic_event_signal`
- `risk_field_signal`

禁止输入：
- 原始执行控制字段
- 任何可导致 default-on 或 side effects 放权的控制位

---

## 4) 桥接输出（candidate-only）

桥接输出必须包含：
- `scene_state`（符合 `LUNA_CORE_SCENE_STATE_MACHINE_V0.md` 字段）
- `task_candidates`（候选动作集合；不得含 execute 语义）
- `audit_trace`（transition reason + 输入摘要引用）

禁止输出：
- 任何可被解释为 execute/release/retry/reopen 的命令字段
- 任何 default path enablement 意图

