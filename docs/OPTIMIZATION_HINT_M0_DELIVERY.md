# Optimization Hint / Tree Improvement Suggestion M0（决策树优化建议层 M0）交付

## 1. 定位（写死）

本模块不是自动优化器；它只回答：
- 这次哪里效率低
- 为什么低
- 最该先改哪个模块
- 建议怎么改（可执行动作粒度）

它是“从诊断走向优化”的第一步：在已有 **结构树 + 指标 + issue + 白盒** 之上，输出可审计的规则版优化建议。

## 2. 交付件

- 实现：`decision_monitor/optimization_hint.py`
- 接入：`decision_monitor/schema.py` + `decision_monitor/builder.py`（字段 `optimization_hint`）
- Console：`tools/reasoning_console_aggregator.py` + `tools/reasoning_console_server.py`
- 单测：`tests/test_optimization_hint.py`
- smoke/JSONL：`tools/smoke_optimization_hint.py`

## 3. 数据结构：OptimizationHintResult

- optimization_hint_type
- optimization_hint_reason（必须含“为什么建议改这个模块、为什么不是别的模块”）
- suggested_optimization_module
- suggested_optimization_action
- priority_level（high/medium/low）
- trigger_issue_type / trigger_issue_reason
- supporting_metrics_summary / supporting_tree_summary
- suggested_followup_measure / suggested_validation_path（可选）
- excluded_alternative_modules（可选）
- optimization_hint_applied

## 4. 规则映射（M0）

优先基于 `reasoning_tree_metrics.possible_tree_issue_type`：

- high_dead_branch_ratio → reduce_dead_branches（优先 hypothesis_layer：收紧弱假设入口）
- tree_too_deep / long_resolution_path → shorten_resolution_path（优先 action_hint_copy：更早确认/收口）
- feedback_not_effective → improve_feedback_convergence（优先 confirmation_input_bridge：提升反馈驱动推进）
- too_many_branches → reduce_over_branching（优先 hypothesis_layer：限制备选分支）
- blocked_without_resolution → resolve_blocked_state（优先 recheck_planner：阻断恢复/收口策略）

## 5. 结论（M0）

优化建议层已建立并接入 frame + JSONL + Console；当前为规则版建议层，不自动更改系统行为，后续可在不破坏接口的前提下迭代覆盖面与精准度。

## 6. 下一层：Optimization Feedback Loop（M0）

建议层用于“指出先改哪里”，下一层 **Optimization Feedback Loop** 用于验证“建议是否有效、改善了哪些指标、是否值得沉淀”。  
参见：`docs/OPTIMIZATION_FEEDBACK_LOOP_M0_DELIVERY.md`。

