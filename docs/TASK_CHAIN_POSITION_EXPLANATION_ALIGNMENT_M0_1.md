# Task Chain Position Explanation Alignment — M0.1

**文件**：`docs/TASK_CHAIN_POSITION_EXPLANATION_ALIGNMENT_M0_1.md`  
**版本**：M0.1（任务链位置解释增强；非任务引擎重构）  
**前置**：`docs/TASKCHAIN_MAINLINE_INTEGRATION_ARCHITECTURE.md`、`docs/TASK_CHAIN_STATE_SNAPSHOT_MINIMAL_INSERT_M0.md` — `task_chain_state_snapshot` 已接入主链与日志/总结链。  
**同链规则**：`docs/MAINLINE_WHITEBOX_LOG_CHAIN_RULE.md`

**本文不写**：熔断/消失/归类/结束深机制、完整任务链引擎、任务图、图书馆真接入、扩包、新评分模型。

---

## 1. 目标

在 **最小快照** 已存在的前提下，将任务链从「状态可见」提升为 **白盒与 Summary 中可解释的位置上下文**：

- 区分主任务推进 vs 子任务局部处理（仅解释，不拍板）。
- 插入 / 恢复 / 暂停 / 主链语义更可读。
- `resume_target` 是待恢复提示还是已带终端语义，**轻量**标出。
- 成功标准偏主任务级还是节点级，**轻量**标出。
- 局部成功但主任务未必推进、伪恢复风险等 **告警级语义** 进入快照与 summary。

---

## 2. 工程落地（代码）

| 模块 | 作用 |
|------|------|
| `decision_monitor/task_chain_state_snapshot.py` | `TaskChainStateSnapshot` 增加 `task_position_reason_summary`
、`task_position_event_summaries`、`task_position_warning_summary`、`task_position_timeline_events`；`build_task_chain_*` 轻量派生；`build_task_chain_progress_summary` 增强 |
| `decision_monitor/reasoning_timeline_view.py` | `append_task_chain_position_explanation_events`：将 `task_position_timeline_events` 写入时间轴 |
| `decision_monitor/builder.py` | 在 `append_task_chain_snapshot_event` 之后调用 `append_task_chain_position_explanation_events`，保证事件进入 **同一帧** `reasoning_timeline_view` |
| `decision_monitor/reasoning_structure_tree.py` | `tree_summary` 中 `task_pos=stage/mode|sub|resume|crit|warn` |
| `decision_monitor/run_summary_builder.py` | `summary_brief` 中 `task=` 片段加长以容纳增强后的 `task_chain_progress_summary` |
| `tools/reasoning_console_aggregator.py` | `snapshot_task_position_*`、`snapshot_task_position_readable` |
| `tools/reasoning_console_server.py` / `tools/decision_monitor_viewer.py` | 展示 M0.1 字段 |

**时间轴事件类型（示例）**：`task_chain_position_interpreted`、`task_subtask_relationship_observed`、`task_resume_target_active`、`task_partial_progress_detected`、`task_local_success_without_main_progress`、`task_recovery_path_visible`（按帧条件子集出现，非全量每帧）。

---

## 3. 测试与 Smoke

- 单测：`tests/test_task_chain_position_explanation_alignment.py`
- Smoke：`tools/smoke_task_chain_position_explanation_alignment.py`（写 `logs/smoke_task_chain_position_explanation_alignment.jsonl`）

---

## 4. 主线—白盒—日志—任务链 串联检查（本轮）

- **A 主线**：`task_chain_state_snapshot` 仍由 `build_task_chain_state_snapshot` 从主链已有字段构建，**未**改变主链拍板逻辑。
- **B 白盒**：结构树 `tree_summary` 与时间轴事件解释 **同一快照** `task_chain_state_snapshot.to_dict()`。
- **C 日志**：增强字段与事件随 `DecisionMonitorFrame` / JSONL 序列化；聚合器可消费 `snapshot_task_position_readable` 与 `run_summary_task_chain_progress_summary`。
- **D 最终判断**：**主线通顺，白盒一致，日志已落地** — 任务链位置解释在 **白盒 + Summary + 时间轴** 上形成更强同链表达；**未**引入任务引擎复杂度。

---

## 5. 本轮是否通过

**通过**：任务链位置已在白盒与 summary 中形成更强同链解释闭环（仍属轻解释层，非深归因）。
