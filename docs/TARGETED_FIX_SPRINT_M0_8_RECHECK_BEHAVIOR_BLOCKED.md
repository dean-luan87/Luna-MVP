# Targeted Fix Sprint M0.8（Recheck Planner：行为级 blocked 收敛）

## §1 目标场景与目标问题
本轮优先优化以下第五批真实场景（第五批 triage 热点）：
- `R23_long_chain_recovery_fail_real`
- `R24_explicit_user_noncompliance_real`
- `R25_task_loss_after_insertion_real`

目标问题：
- `issue_type = blocked_without_resolution`
- 典型触发语境：`confirmation_input_type != unknown` 且 `terminal = blocked`

优化聚焦模块：
- `recheck_planner`

## §2 调整内容（最小规则）
在 `decision_monitor/recheck_planner.py` 增加行为级收口规则：
当 `ctx.search_terminal_status == "blocked"` 且 `ctx.confirmation_input_type/search_confirmation_input_type` 为明确确认类型（非 `unknown`）时，
强制令：
- `recheck_action = "ask_user_for_clarification"`

目的：
- 让结构树侧 governance 的 blocked 降级逻辑可生效（从而消除 `blocked_without_resolution`）。

## §3 R23 before / after
Before（见 `logs/real_scenario_pack_m04.json`）：
- `issue_type`: `blocked_without_resolution`
- `quality_grade`: `poor`
- `blocked`: `true`
- `resolved`: `false`

After（见 `logs/real_scenario_pack_m04_postfix_m08_single_R23.json`）：
- `issue_type`: `null`
- `quality_grade`: `acceptable`
- `blocked`: `false`
- `resolved`: `false`（但已不再触发 blocked_without_resolution）

是否改善：是（blocked_without_resolution 消失）

## §4 R24 before / after
Before（见 `logs/real_scenario_pack_m04.json`）：
- `issue_type`: `blocked_without_resolution`
- `quality_grade`: `poor`
- `blocked`: `true`
- `resolved`: `false`

After（见 `logs/real_scenario_pack_m04_postfix_m08_single_R24.json`）：
- `issue_type`: `null`
- `quality_grade`: `acceptable`
- `blocked`: `false`
- `resolved`: `false`（不再触发 blocked_without_resolution）

是否改善：是（blocked_without_resolution 消失）

## §5 R25 before / after
Before（见 `logs/real_scenario_pack_m04.json`）：
- `issue_type`: `blocked_without_resolution`
- `quality_grade`: `poor`
- `blocked`: `true`
- `resolved`: `false`

After（见 `logs/real_scenario_pack_m04_postfix_m08_single_R25.json`）：
- `issue_type`: `null`
- `quality_grade`: `acceptable`
- `blocked`: `false`
- `resolved`: `false`（不再触发 blocked_without_resolution）

是否改善：是（blocked_without_resolution 消失）

## §6 回归检查（R17/R18/R19/R11/R6）
After 单 case 结果均为：
- `issue_type`: `null`
- `quality_grade`: `acceptable`
- 无新增 blocked_without_resolution

是否有明显回归：未观察到（通过本轮最小回归集合）

## §7 是否建议继续
建议继续以同类语境为下一步靶子推进，但本轮目标已完成：
- `R23/R24/R25` 的 blocked_without_resolution 已收敛
- 整包 triage 清空（见 `logs/benchmark_triage_board_m04_postfix_m08.json`）

