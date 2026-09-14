# Optimization Feedback Loop M0（优化建议验证闭环 M0）交付

## 1. 定位（写死）

本模块是“建议验证层”，不是自动优化器。它只负责：
- 记录优化建议
- 对比 baseline vs current 指标
- 生成最小验证结论（improved/unchanged/regressed/not_enough_data/not_applicable）
- 输出下一步建议与是否值得进入图书馆候选（占位）

验证对象聚焦结构树质量：tree metrics + issue 变化。

## 2. 交付件

- 实现：`decision_monitor/optimization_feedback_loop.py`
- 接入：`decision_monitor/schema.py` + `decision_monitor/builder.py`（字段 `optimization_feedback_loop`）
- Console：`tools/reasoning_console_aggregator.py` + `tools/reasoning_console_server.py`
- 单测：`tests/test_optimization_feedback_loop.py`
- smoke/JSONL：`tools/smoke_optimization_feedback_loop.py`

## 3. 数据结构：OptimizationFeedbackLoopResult

- baseline/current 摘要：baseline_metrics_summary / current_metrics_summary
- issue 对照：baseline_issue_type / current_issue_type
- delta 指标：depth/branch/dead/resolution_len/eff_fb/prune_rate
- validation_result + validation_reason
- improvement_detected / regression_detected
- suggested_next_step（keep_observing / validate_with_more_samples / prioritize_module_tuning / reject_current_hint / persist_to_library_candidate）
- worth_persisting_to_library（占位布尔）

## 4. 验证规则（M0）

- improved：depth/dead/resolution/prune_rate 下降 或 eff_fb 上升 或 issue 消失/减弱
- regressed：depth/dead/resolution/prune_rate 上升 或 eff_fb 下降 或出现更严重 issue
- unchanged：信号混合或变化不明显
- not_enough_data：无 baseline
- not_applicable：无有效 optimization_hint

## 5. Baseline 输入（M0 最小）

M0 baseline 支持通过 `DecisionMonitorBuilder` ctx 注入：
- `optimization_baseline_metrics`（dict）

后续可扩展为从上一轮 snapshot/历史样本自动对照，但本轮不做趋势系统。

## 6. 结论（M0）

优化建议验证闭环已建立并接入 frame + JSONL + Console；当前为规则版验证，不自动应用优化，不做图书馆写回，仅提供沉淀候选标记与下一步建议。

