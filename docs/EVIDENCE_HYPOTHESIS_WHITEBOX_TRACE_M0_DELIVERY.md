# Evidence / Hypothesis Whitebox Trace M0（证据 × 假设白盒轨迹 M0）交付

## 1. 定位（写死）

本模块用于**解释**（不改写）：
- `evidence_ledger`：为什么形成这条 evidence
- `hypothesis_layer`：为什么主假设是这个、为何排除其它
- `confirmation_input_bridge`：用户反馈如何影响假设权重/有效性

输出遵循统一白盒五块骨架，并提供用户可见解释层；同时要求可挂接到 Reasoning Structure Tree。

## 2. 交付件

- 实现：`decision_monitor/evidence_hypothesis_whitebox_trace.py`
- 接入：`decision_monitor/builder.py` + `decision_monitor/schema.py`
- 单测：`tests/test_evidence_hypothesis_whitebox_trace.py`

## 3. 白盒结构（统一五块骨架）

- reasoning_steps
- weight_allocation（规则版：base_confidence + alignment/feedback/penalty）
- exclusion_log（至少 1 条）
- interaction_trace（有反馈时）
- result_summary：`whitebox_summary / whitebox_applied`

并提供：
- user_visible_explanation（用户可见解释层）

## 4. 关键解释口径

- **evidence 形成原因**：从 ledger claim/support/missing 提取摘要
- **hypothesis 选择原因**：对候选 hypothesis 做规则权重拆解（不做学习权重）
- **排除**：对未采用的 hypothesis 给出 exclusion
- **反馈影响**：将 `confirmation_input_type/raw_text` 映射为 bonus/penalty 组件（规则版）

## 5. 接入结构树（要求）

结构树层面至少可见：
- evidence 节点（来自 ledger）
- hypothesis 节点（来自 layer）
- exclusion 节点（来自白盒 exclusion）
- feedback-driven 标记（有反馈时）

## 6. 结论（M0）

Evidence / Hypothesis 白盒轨迹已形成可审计输出（骨架+用户可见解释），并能被结构树与 Reasoning Console 消费。

