# Summary × Post-Processing Boundary Contract — M0.5

**文件**：`docs/SUMMARY_POST_PROCESSING_BOUNDARY_CONTRACT_M0_5.md`  
**性质**：工程契约收口（Summary 进入后处理链的合法边界）  
**上位语义**：`docs/TRACE_LOGGING_AND_SUMMARY_PIPELINE.md`、`docs/LIBRARY_MEMORY_AND_GOVERNANCE_ARCHITECTURE.md`  
**工程串联**：`docs/MAINLINE_WHITEBOX_LOG_CHAIN_RULE.md`

**本文不写**：后处理分类算法、图书馆/记忆写入、污染抵抗深实现、主链重构。

---

## §1. 目标

将 **Summary-first 且非 Summary-only** 写成可序列化、可审计的工程契约：后处理链消费 **`post_processing_summary_entry`**（由 `run_summary_reference` 只读派生），明确：

- 哪些摘要字段可作为**归类/路由入口**；  
- 哪些字段**仅提示**、不得单独定因；  
- 何时必须**回溯** Raw Trace / Structured Event / 白盒；  
- 图书馆 / 记忆 / 治理的**越权禁止**边界。

---

## §2. 最小对象：`post_processing_summary_entry`

**模块**：`decision_monitor/post_processing_summary_contract.py`  
**构建**：`build_post_processing_summary_entry(frame)`，仅在 `run_summary_reference.summary_reference_applied` 为真时生效。

| 分组 | 字段 | 含义 |
|------|------|------|
| 标识 | `entry_id`、`trace_anchor_id`、`summary_id` | 与 trace/summary 对齐 |
| 可直接用于入口的摘要 | `mainline_summary`、`mainline_state_summary`、`memory_usage_summary`、`source_scheduling_summary`、`task_chain_progress_summary`、`issue_or_risk_summary` | 来自 `run_summary_reference`，可做初步分类/路由/优先级（**非因果证据本体**） |
| 边界写死 | `summary_brief_hint_only`、`summary_not_substitute_for_raw_trace`、`library_default_reads_summary_entry_not_raw_trace`、`memory_write_forbidden_from_summary_only` | 契约常量（M0.5） |
| 回溯提示 | `requires_trace_backfill`、`requires_event_backfill`、`requires_whitebox_backfill`、`backfill_reason_summary` | 启发式 M0 标志，提示是否下钻 |

**刻意不包含**：`raw_trace_layer_snapshot` / `structured_event_layer_snapshot` 全文 —— 回溯须从 **frame / JSONL** 读取原层，而非塞进契约对象替代黑匣子。

---

## §3. 三类 Summary 用法（写死）

### A. 可直接用于归类入口的字段

`mainline_state_summary`、`task_chain_progress_summary`、`source_scheduling_summary`、`memory_usage_summary`、`issue_or_risk_summary`、`mainline_summary` 等 —— 允许作为**初步**分类、路由、优先级排序的输入。

### B. 仅提示、不能独立定因

`summary_brief` 及各类「可读一串字」—— **仅提示**后续要看哪一层；**不得**单独作为沉淀或因果结论依据。

### C. 必须回溯原始层

冲突、污染、记忆/观察张力、主导源异常、伪恢复等语义敏感场景 —— 必须结合 **Raw Trace / Structured Event / 白盒**；契约通过 `requires_*_backfill` 与 `backfill_reason_summary` 提示，**不替代**下钻。

---

## §4. 工程接入

| 环节 | 内容 |
|------|------|
| **Builder** | 在 `run_summary_reference` 之后构建 `post_processing_summary_entry`，写入 frame；并回填 `post_processing_intelligence_reserve.summary_post_processing_entry_id`。 |
| **日志 / JSONL** | 契约随 `DecisionMonitorFrame` 落地。 |
| **聚合** | `reasoning_console_aggregator` 暴露 `post_processing_summary_entry` 与扁平回溯字段。 |
| **Console / Viewer** | 独立区块展示契约与 backfill 标志。 |

---

## §5. 图书馆 / 记忆 / 治理（边界提示）

- **图书馆**：默认消费 **`post_processing_summary_entry`** 作为 summary-first 入口；**不**以 Raw Trace 作为默认唯一入口（与 `TRACE_LOGGING_AND_SUMMARY_PIPELINE` 一致）。  
- **记忆**：**禁止**仅凭 Summary/Entry 直接写入；须经后处理链筛选与策略。  
- **治理**：未来可对 Entry 执行 observe / watch / defer / block —— **本轮仅占位**。

---

## §6. 主线 — 白盒 — 日志 — Summary — 后处理 串联检查

- **A Summary**：`run_summary_reference` 仍为唯一 Summary 源；契约**派生**、**不反写** Summary。  
- **B 后处理边界**：入口结构化、字段分级、回溯提示可审计。  
- **C 日志**：`post_processing_summary_entry` 进入 frame/JSONL/聚合链。  
- **D 结论**：**Summary 与后处理链已形成最小边界契约闭环**（M0.5 启发式 backfill，非完整分类引擎）。

---

## §7. 本轮不做

真实后处理分类、图书馆接入、记忆写入、污染深实现、扩包、评分模型、主链重构。
