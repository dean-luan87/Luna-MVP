# Trace × Summary Separation Engineering Sprint M0.2 — 交付说明

**目标**：在 `TRACE_LOGGING_AND_SUMMARY_PIPELINE.md` M0 定稿与既有主链/白盒/日志同链基础上，将 **Raw Trace / Structured Event / Summary Reference** 在工程上进一步分层，形成最小 **运行总结入口**（`run_summary_reference`），避免「总结与黑匣子混读」。

**上位约束**：`docs/MAINLINE_WHITEBOX_LOG_CHAIN_RULE.md`

---

## 交付物

| 类型 | 路径 |
|------|------|
| 运行总结构建模块 | `decision_monitor/run_summary_builder.py` |
| Frame 字段 | `DecisionMonitorFrame.run_summary_reference` |
| Builder 接入 | `decision_monitor/builder.py`（post-processing 之后） |
| Runtime 占位 | `runtime/context.py`：`run_summary_brief`、`run_summary_issue_hint` |
| 聚合链 | `tools/reasoning_console_aggregator.py`：三层 one-liner + `run_summary_*` 扁平字段 |
| Console / Viewer | `tools/reasoning_console_server.py`、`tools/decision_monitor_viewer.py` |
| 单测 | `tests/test_trace_summary_separation.py` |
| Smoke | `tools/smoke_trace_summary_separation.py` |

---

## 三层语义（工程对象）

1. **Raw Trace（`raw_trace_layer_snapshot` + `raw_trace_layer_one_liner`）**  
   从 `goal` / `inputs` / `state` / `decision` / `outputs` / `consequence` 抽取的最小事实切片；**非**自由生成叙述。

2. **Structured Event（`structured_event_layer_snapshot` + `structured_event_layer_one_liner`）**  
   从 `reasoning_timeline_view` 抽取事件计数与类型列表；**仍属日志链语义**，非后处理结论。

3. **Summary Reference（`run_summary_reference`）**  
   聚合 `mainline_integration`、`memory_novel_information_channel`、`scheduled_source_state`、风险/质量/阻断等**已有字段**的轻摘要；`summary_feed_note` 标明 **Derived from Trace, not substitute**。

---

## 边界（写死）

- **不**以 summary 反推主链事实；**不**替代 JSONL 中的完整 frame。  
- **不**实现图书馆写入、后处理真实算法、新评分模型。

---

## 主线—白盒—日志 串联检查

| 维度 | 结论 |
|------|------|
| A 主线 | 主链事实仍由 6 层与既有模块写入 frame；summary 仅后置于完整 frame。 |
| B 白盒 | 白盒解释来源未改；summary 可引用白盒间接产物（timeline/metrics 等），不单独编造。 |
| C 日志 | `run_summary_reference` 进入 `to_dict()` / JSONL / 聚合；与 raw/event 字段可区分。 |
| D **最终判断** | **主线通顺，白盒一致，日志已落地**（三层语义在 frame/聚合/Console/Viewer 可区分）。 |

---

## 本轮是否通过

**通过**（以本仓库单测与 smoke 脚本为准）。
