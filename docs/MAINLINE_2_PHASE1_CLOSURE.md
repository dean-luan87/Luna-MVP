# 主线 2 第一阶段收口（2.0–2.3）

**主线名称**：主线 2 — 目标驱动的时空状态内核（Goal-Driven Spatiotemporal State Core）  
**阶段**：第一阶段（LocalGoalState：局部时空状态核）  
**收口范围**：2.0 / 2.1 / 2.2 / 2.3  
**结论**：**通过并阶段性收口**。不再横向扩动作/优先级类别；下一步进入第二阶段（局部空间结构化）。

---

## 1. 交付物表（按版本阶段）

| 阶段 | 交付物 | 说明 | 状态 |
|------|--------|------|------|
| **2.0** | `LocalGoalState`（可见/可测/可解释） | 从 goal/state/view_guard/predictive_hold/runtime_domain_guard/scene_gate/consequence 汇聚为围绕目标的局部状态核 | ✅ 通过 |
| **2.1** | 轻量行为接入 | `next_best_action` 在无高优先级阻断时开始影响主循环（示例：hold_and_confirm → SPEAK→WAIT）；focus_region_hint/view_behavior_hint 回流 monitor/viewer | ✅ 通过 |
| **2.2** | recheck 最小执行入口 | recheck 从“提示”变为“可执行入口”：pending → 主循环 force_sample → executed → viewer 可见 → 一次性清理 | ✅ 通过 |
| **2.3** | 观察优先级接入 | 仅三类优先级（forward/close_range/confirm_zone），写入 runtime_ctx 与 task_state.view_priority；高优先级阻断规则保留 | ✅ 通过 |

---

## 2. 关键文件（单一真相链）

- **契约与数据结构**
  - `decision_monitor/schema.py`：`LocalGoalState`、`DecisionMonitorFrame.local_goal_state`、state 中 local_goal_* 行为字段
  - `decision_monitor/CONTRACT.md`：字段来源与边界

- **构建与汇聚**
  - `decision_monitor/local_goal_state_builder.py`：2.0 汇聚逻辑（3 类目标：observe_navigate / confirm_path / close_range_check）
  - `decision_monitor/builder.py`：将 local_goal_state 写入 frame；透传 local_goal_* applied/hint/recheck/view_priority 到 state

- **主循环消费（行为层）**
  - `main.py`：
    - 消费 `frame.local_goal_state` 写入 runtime_ctx（含 applied/hint）
    - 2.2：recheck pending→force_sample→executed 的一次性执行入口
    - 2.3：local_goal_view_priority 写入 runtime_ctx + task_state.view_priority 注入
  - `runtime/context.py`：LocalGoalState 行为接入运行字段

- **可视化与验收**
  - `tools/decision_monitor_viewer.py`：LocalGoalState 卡片展示（接管状态、recheck 责任链、view_priority）
  - `tests/test_decision_monitor.py`：LocalGoalState / applied 字段 / recheck 责任链 / view_priority 字段等单测

---

## 3. 已真实生效 vs 保守占位

### 已真实生效（第一阶段“有分量”的部分）

- **hold_and_confirm 真动作**：在主循环中发生 SPEAK→WAIT（LocalGoalState 参与行为选择）
- **recheck 最小执行**：pending→force_sample→executed，并一次性清理（可复盘、可解释）
- **观察优先级接管（轻量）**：写入 runtime_ctx 与 task_state.view_priority，影响语义路由/解释（不碰镜头硬控）
- **高优先级阻断规则**：minimum mode / scene suspended / human_check_pending / goal_progress_paused 时不接管，避免与治理层打架

### 保守占位（明确不做，避免开坑）

- `critical_objects`：仍为空/占位（不硬接 detector/OCR 细节）
- 真实镜头/云台控制闭环
- detector/OCR 主逻辑精细接管或复杂 planner
- 2.5D/3D、全局地图、长时记忆、复杂对象跟踪

---

## 4. 验收样本与测试（最小可验证链）

- **2.0**：LocalGoalState 每帧产出、不同 goal 产出不同 focus_region/next_best_action
- **2.1**：applied/hint 字段可回流到 state（Viewer 可见）；next_best_action 可触发最小行为改变（hold_and_confirm）
- **2.2**：recheck 责任链字段（mode/type/executed）可见；主循环具备一次性 force_sample 执行入口
- **2.3**：view_priority 字段可见且 applied 标记存在；task_state.view_priority 注入

---

## 5. 收口结论（写死边界）

主线 2 第一阶段（2.0–2.3）已成立：**局部状态 → 行为建议 → 最小复核执行 → 观察优先级**。  
本阶段收口后：**不再横向扩 next_best_action 或 view_priority 类别**；下一步进入 **主线 2 第二阶段：局部空间结构化**（只定义，不立刻实现）。

