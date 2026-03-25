# Targeted Fix Sprint M1.0（Recheck Planner：意图-动作-任务错位 blocked 收口）

## §1 目标场景
本轮聚焦第七批真实场景（R35~R40）：
- `R35_intent_action_task_mismatch_real`
- `R36_confirmed_but_not_executed_real`
- `R37_executed_but_goal_shifted_real`
- `R38_subtask_return_semantic_loss_real`
- `R39_fact_feedback_stage_conflict_real`
- `R40_false_recovery_real`

### 触发语境（来自 ctx）
这些 case 的 `ctx_json` 命中 mismatch 标志位（例如 `intent_action_task_mismatch_expected` 等）。

## §2 目标问题
- `issue_type = blocked_without_resolution`
- `quality_grade = poor`
- `blocked = true`
- `resolved = false`

且出现机制：`recheck_planner.recheck_action` 在 blocked/unresolved 语境下偏向 `look_forward`，导致 governance 侧 blocked 无法降级为 watchlist，从而被 metrics 持续标记为 `blocked_without_resolution`。

## §3 调整内容（最小规则，只改 recheck_planner）
在 `decision_monitor/recheck_planner.py` 增加 M1.0 early override：

当 `ctx` 命中任一 mismatch 标志位（`*_expected` 对应意图-动作-任务错位语境）时，强制：
- `recheck_action = "ask_user_for_clarification"`
- `recheck_blocked = False`
- `recheck_applied = True`

目的：让 `reasoning_structure_tree` 的 actionable_fallback 逻辑生效，把 governance 的 blocked 降级为 watchlist，从而解除 `blocked_without_resolution` 度量条件。

## §4 before / after（关键对照）
baseline（before）：
- `logs/real_scenario_pack_m06.json`

本轮结果（after）：
- `logs/real_scenario_pack_m06_postfix_m10.json`

### R35
- Before：`issue_type=blocked_without_resolution, quality=poor, blocked=true, resolved=false`
- After ：`issue_type=None, quality=acceptable, blocked=false, resolved=false`

### R36
- Before：`issue_type=blocked_without_resolution, quality=poor, blocked=true, resolved=false`
- After ：`issue_type=None, quality=acceptable, blocked=false, resolved=false`

### R37
- Before：`issue_type=blocked_without_resolution, quality=poor, blocked=true, resolved=false`
- After ：`issue_type=None, quality=acceptable, blocked=false, resolved=false`

### R38
- Before：`issue_type=blocked_without_resolution, quality=poor, blocked=true, resolved=false`
- After ：`issue_type=None, quality=acceptable, blocked=false, resolved=false`

### R39
- Before：`issue_type=blocked_without_resolution, quality=poor, blocked=true, resolved=false`
- After ：`issue_type=None, quality=acceptable, blocked=false, resolved=false`

### R40
- Before：`issue_type=blocked_without_resolution, quality=poor, blocked=true, resolved=false`
- After ：`issue_type=None, quality=acceptable, blocked=false, resolved=false`

## §5 是否改善
是：`R35~R40` 的 `blocked_without_resolution` 在整包中全部消失，且 quality 从 `poor -> acceptable`。

补充（整包对照）：
- Before：`logs/real_scenario_pack_m06.json` → `passed_cases=34`，`issue_type_distribution` 含 `blocked_without_resolution=6`，triage 热点在 `recheck_planner`
- After ：`logs/real_scenario_pack_m06_postfix_m10.json` → `passed_cases=40`，`issue_type_distribution=none×40`，`ranked_modules=[]`、`ranked_issues=[]`

## §6 是否建议继续
建议继续：如果下一轮出现“新类错位导致的 blocked/unresolved”，优先在 `recheck_planner` 侧继续给出可行动 fallback（ask_user_for_clarification / hold_and_confirm）以维持 governance blocked 的可降级闭环。

