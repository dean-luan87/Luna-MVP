# Mainline State / Phase Explicitness — M0.4

**文件**：`docs/MAINLINE_STATE_PHASE_EXPLICITNESS_M0_4.md`  
**性质**：工程交付收口（主链状态/阶段最小显式化）  
**上位语义**：`docs/DECISION_MAINLINE_ARCHITECTURE.md`（四态、六阶段）  
**工程串联**：`docs/MAINLINE_WHITEBOX_LOG_CHAIN_RULE.md`

**本文不写**：新决策算法、主链重写、评分公式、任务引擎、熔断/深结束语义。

---

## §1. 目标

在**不重写主链、不改拍板逻辑**的前提下，将主链四态（`candidate` / `execution` / `recovery` / `pause`）与六阶段（`contextualization` … `result_feedback`）收敛为**可测试、可观察、可落地**的最小对象 `mainline_state_snapshot`，并完成与 frame、白盒（结构树/时间轴）、JSONL、聚合链、`run_summary_reference`、Console、Viewer 的**同链承载**。

**明确区分**（须在文档与工程中一致表述）：

- 主链状态 **≠** 任务链模式（`task_mode` 等）。  
- 主链 **recovery** **≠** 任务链 `recovering`。  
- 主链 **pause** **≠** 任务 `paused`（pause 表示主链不宜推进、等待人/澄清/外部输入等）。

---

## §2. 最小对象：`mainline_state_snapshot`

**模块**：`decision_monitor/mainline_state_snapshot.py`

| 字段 | 说明 |
|------|------|
| `mainline_state` | `candidate` \| `execution` \| `recovery` \| `pause` \| `unknown` |
| `mainline_phase` | `contextualization` \| `candidate_formation` \| `path_selection` \| `recheck_or_repair` \| `closure` \| `result_feedback` \| `unknown` |
| `mainline_state_reason_summary` | 状态推导一句原因（M0 启发式） |
| `mainline_phase_reason_summary` | 阶段推导一句原因 |
| `mainline_state_transition_summary` | 可选，过渡观察 |
| `mainline_state_snapshot_applied` | 是否已应用 |
| `mainline_state_timeline_events` | 供时间轴合并的轻量事件描述 |

推导**只读**复用现有 frame 信号（如 `hypothesis_layer`、`object_search_interaction`、`recheck_planner`、`task_chain_bridge`、`confirmation_input_bridge`、`state` 等），不引入新上游依赖。

---

## §3. 工程接入摘要

| 环节 | 内容 |
|------|------|
| **Builder** | `DecisionMonitorBuilder` 在 memory invocation 之后、`run_summary_reference` 之前构建 snapshot，写入 `DecisionMonitorFrame.mainline_state_snapshot`，并调用 `append_mainline_state_snapshot_events`。 |
| **白盒 — 结构树** | `tree_summary` 追加 `\| state=…\|phase=…`。 |
| **白盒 — 时间轴** | 事件类型含 `mainline_state_snapshot_formed`、`mainline_phase_identified`、`mainline_state_transition_observed`（按帧合并）。 |
| **日志 / JSONL** | snapshot 随 frame 序列化落盘；聚合链可读。 |
| **Summary** | `RunSummaryReference.mainline_state_summary`；`summary_brief` 含 **`mls=`** 段（为防 800 字截断，**靠前**置于 `trace` / `mainline` 之后）。 |
| **聚合** | `tools/reasoning_console_aggregator.py`：`mainline_state_snapshot` 与扁平 `snapshot_mainline_*`、`run_summary_mainline_state_summary`。 |
| **Console / Viewer** | Console 独立区块展示 state/phase/原因；Viewer `mainline_state_snapshot` 折叠区；Trace×Summary 区展示 `mainline_state_summary`。 |

---

## §4. 测试与 smoke

| 类型 | 路径 |
|------|------|
| 单测 | `tests/test_mainline_state_snapshot.py` |
| smoke | `tools/smoke_mainline_state_snapshot.py`（写 `logs/smoke_mainline_state_snapshot.jsonl`） |

---

## §5. 主线 — 白盒 — 日志 — Summary 串联检查

- **A 主线**：`mainline_state_snapshot` 在 builder 主路径生成并挂入 frame。  
- **B 白盒**：结构树 `tree_summary` 与时间轴事件可读到 state/phase。  
- **C 日志**：frame/JSONL/聚合链含 snapshot 与 `run_summary` 中的 `mainline_state_summary`、`summary_brief` 的 `mls=`。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地** — `mainline_state_snapshot` 已形成 **主线—白盒—日志—Summary** 的最小同链闭环（M0 启发式推导，不要求全场景语义完备）。

---

## §6. 本轮范围外（显式不做）

主链重写、新决策算法、新评分、第十批真实场景扩包、图书馆/记忆写入、熔断/消失/结束深机制、复杂任务图 — 均不在 M0.4 范围。
