# Memory Invocation Explanation — M0.3

**文件**：`docs/MEMORY_INVOCATION_EXPLANATION_M0_3.md`  
**版本**：M0.3（记忆调用解释增强；非记忆系统本体）  
**前置**：`memory_novel_information_channel`、`scheduled_source_state`、`task_chain_state_snapshot`、Trace×Summary M0.2 等已接入。  
**同链规则**：`docs/MAINLINE_WHITEBOX_LOG_CHAIN_RULE.md`

**本文不写**：记忆库写入、筛选算法、污染抵抗实现、新评分模型、主链大重构。

---

## 1. 目标

在**不重构记忆引擎**的前提下，把「记忆是否参与、为何参与、用了什么、对主链是帮助还是风险」打成 **同一帧** 的 `memory_invocation_explanation`，进入 **主链 frame → 白盒/时间轴 → JSONL/聚合 → Summary**。

---

## 2. 最小结构 `memory_invocation_explanation`

| 字段 | 含义 |
|------|------|
| `memory_invoked` | 是否有记忆源参与（通道计数或调度 dominant=`memory_recall`） |
| `memory_type_summary` | 类型级标签（如 `spatial_memory+task_memory+…`） |
| `memory_invocation_reason_summary` | 轻量原因（调度主导、任务阶段、熟悉场景等） |
| `memory_invocation_used_content_summary` | 从 `memory_derived` 通道摘要等抽取 |
| `memory_invocation_effect_summary` | `supports_mainline` / `neutral_reference` / `memory_overweight_risk` / `memory_vs_observation_conflict` / `memory_vs_task_risk` / `unknown` |
| `memory_invocation_alternative_summary` | 可选：参与源中的非 memory 候选 |
| `memory_invocation_timeline_events` | 注入时间轴的最小事件列表 |
| `memory_invocation_explanation_applied` | 本帧已生成解释对象 |

**工程模块**：`decision_monitor/memory_invocation_explanation.py`  
**Builder**：在 `run_summary_reference` 之前写入 frame，并调用 `append_memory_invocation_explanation_events`。  
**Summary**：`run_summary_reference.memory_usage_summary` 由 `build_memory_usage_summary_line` 合并通道与解释；`summary_brief` 含 `; mem=` 段。

---

## 3. 测试与 Smoke

- 单测：`tests/test_memory_invocation_explanation.py`
- Smoke：`tools/smoke_memory_invocation_explanation.py` → `logs/smoke_memory_invocation_explanation.jsonl`

---

## 4. 主线—白盒—日志—Summary 串联检查

- **A 主线**：不改拍板；仅增加只读解释对象。  
- **B 白盒**：结构树 `mem=inv|type|eff`；时间轴 `memory_invocation_*` 事件。  
- **C 日志**：`DecisionMonitorFrame` 顶层字段；JSONL/聚合可读。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地** — 记忆调用已在工程链上形成**最小同链解释闭环**（解释层仍允许「记忆被调用但仍存在风险」）。

---

## 5. 本轮是否通过

**通过**：记忆调用已在主链—白盒—日志—Summary 中形成最小同链解释闭环。
