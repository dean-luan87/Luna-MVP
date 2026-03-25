# Strategy Injection Shadow M0（策略注入影子验证 M0）交付

## 1. 定位（写死）

本模块是“影子验证层”，不是注入执行层。当前只输出：

- 如果未来把策略从图书馆/知识层注入进来，**可能影响哪个模块**
- **可能改善什么指标/缓解什么 issue**
- **风险等级大概如何**
- **下一步建议是什么**

明确不做：真实注入、规则替换、权重改写、复杂模拟器、多轮评估、图书馆接入与自动执行。

## 2. 交付件

- 实现：`decision_monitor/strategy_injection_shadow.py`
- 接入：`decision_monitor/schema.py` + `decision_monitor/builder.py`（字段 `strategy_injection_shadow`）
- Console：`tools/reasoning_console_aggregator.py` + `tools/reasoning_console_server.py`
- 单测：`tests/test_strategy_injection_shadow.py`
- smoke/JSONL：`tools/smoke_strategy_injection_shadow.py`

## 3. 数据结构：StrategyInjectionShadowResult

- injection_target_module / injection_mode
- expected_tree_change / expected_metric_change / expected_issue_relief
- expected_risk_level（low/medium/high/unknown）
- shadow_reason / recommended_next_step
- library_integration_ready（占位）/ shadow_reserved_for_library
- shadow_applied

## 4. 最小规则（M0）

- 若 `knowledge_dual_channel_interface.injection_slot.injection_slot_reserved=true` → 生成 shadow
- target/mode 取自 injection slot
- expected_tree/metric/issue_relief 使用粗映射（按 target + issue_type）
- risk_level 仅按 mode 映射：
  - weight_patch→high，rule_patch→medium，strategy_hint/validation_template→low

## 5. CONTRACT 强约束（写死）

图书馆策略未来正式接入前，优先先经过 Strategy Injection Shadow 影子验证层；不得直接跳过 shadow 层执行真实策略注入。

## 6. 结论（M0）

影子验证层已接入 frame/JSONL/Console，并可给出可审计的“假设注入影响预估”；后续与图书馆整合时应优先复用本层。

