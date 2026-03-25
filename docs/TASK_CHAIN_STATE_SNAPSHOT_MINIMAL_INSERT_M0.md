# Task Chain State Snapshot 最小接入 Sprint M0 — 交付说明

**目标**：将 `task_chain_state_snapshot` 首次接入主路径，形成 **调度层 → 主链 → 白盒 → 日志 / Summary** 的最小同链闭环（见 `docs/TASKCHAIN_MAINLINE_INTEGRATION_ARCHITECTURE.md`）。

**上位约束**：`docs/MAINLINE_WHITEBOX_LOG_CHAIN_RULE.md`

---

## 交付物

| 类型 | 路径 |
|------|------|
| 快照模块 | `decision_monitor/task_chain_state_snapshot.py` |
| Frame 字段 | `DecisionMonitorFrame.task_chain_state_snapshot` |
| 调度层 | `ScheduledSourceState.task_state_presence_summary`；`participating_sources` 显式包含 `task_state`（快照 applied 时） |
| Builder | `decision_monitor/builder.py`：首帧后构建快照；`environment_task_context_reserve` 后精炼快照并 **刷新** `scheduled_source_state`；时间轴追加 `task_chain_state_snapshot_formed` / `task_mode_detected` / `task_resume_target_present` |
| 白盒 | `reasoning_structure_tree` root `task=stage/mode`；`reasoning_timeline_view` 事件 |
| Summary | `RunSummaryReference.task_chain_progress_summary`；`summary_brief` 含 `task=` 片段 |
| Runtime 占位 | `runtime/context.py`：`task_mode`、`task_resume_target`（与已有 `task_chain_stage` 并列） |
| 聚合 / UI | `tools/reasoning_console_aggregator.py`、`reasoning_console_server.py`、`decision_monitor_viewer.py` |
| 单测 | `tests/test_task_chain_state_snapshot.py` |
| Smoke | `tools/smoke_task_chain_state_snapshot.py` |

---

## 最小字段（`task_chain_state_snapshot`）

- `task_chain_id`、`task_chain_stage`、`primary_task_id`、`active_subtask_id`
- `task_mode`：`main` / `subtask` / `inserted` / `recovering` / `paused` / `unknown`
- `task_resume_target`、`task_success_criteria_summary`、`task_chain_context_summary`
- `task_chain_state_snapshot_applied`

数据来源：`task_chain_bridge`、`object_search_interaction`、`task_arbitration`、`goal`、`environment_task_context_reserve.task_chain_context`（若已生成）、`trace_anchor_id`。

---

## 边界（写死）

- **不**实现完整任务引擎、熔断/消失/归类/结束深机制。  
- **不**替代主链拍板；任务链为正式 **上下文源**，经调度层可见。

---

## 主线—白盒—日志—任务链 串联检查

| 维度 | 结论 |
|------|------|
| A 调度层 | `task_state` 参与源 + `task_state_presence_summary` 可读摘要。 |
| B 主链 | Frame 全链携带快照；主链决策逻辑未改。 |
| C 白盒 | 结构树 `task=`；时间轴任务链事件。 |
| D 日志 / Summary | JSONL 含快照；`run_summary_reference` 含 `task_chain_progress_summary`。 |
| **D 最终判断** | **主线通顺，白盒一致，日志已落地** — **`task_chain_state_snapshot` 已形成调度层 → 主链 → 白盒 → 日志/summary 的最小同链闭环**。 |

---

## 本轮是否通过

**通过**（以本仓库单测与 smoke 为准）。
