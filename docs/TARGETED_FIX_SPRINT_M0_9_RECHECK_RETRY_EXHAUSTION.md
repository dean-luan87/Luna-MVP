# Targeted Fix Sprint M0.9（Recheck Planner：Repeated Fallback / Retry Exhaustion 收口）

## §1 目标场景
本轮聚焦第六批真实场景中的 `blocked_without_resolution`：
- `R29_goal_drift_real`
- `R30_success_criteria_shift_real`
- `R31_multi_insertion_chain_real`
- `R32_feedback_action_divergence_real`
- `R33_memory_fast_environment_shift_real`
- `R34_recovery_under_second_disturbance_real`

触发语境（来自 ctx）：
- `object_search_retry_count >= 3`（对应 repeated fallback / retry exhaustion）
- 仍处于 `blocked_without_resolution`（blocked=true 且 resolved=false）

## §2 目标问题
- `issue_type = blocked_without_resolution`
- `quality_grade = poor`
- `blocked = true`
- `resolved = false`

## §3 调整内容（最小规则）
在 `decision_monitor/recheck_planner.py` 增加 M0.9 早期强制收口：
当 `ctx["object_search_retry_count"] >= 3` 时：
- 若 `confirmation_input_type` / `search_confirmation_input_type` 为明确类型（非 `unknown`）：
  - 强制 `recheck_action="ask_user_for_clarification"`
- 否则：
  - 强制 `recheck_action="hold_and_confirm"`
- 同时保持：
  - `recheck_blocked=False`
  - `recheck_applied=True`

目的：让 `reasoning_structure_tree` 的 governance 侧 actionable_fallback 逻辑生效，把 governance 的 blocked 降级为 watchlist，从而解除 `blocked_without_resolution` 的度量条件。

## §4 before / after（关键对照）
基线对照：`logs/real_scenario_pack_m05.json`（before）
本轮结果：`logs/real_scenario_pack_m05_postfix_m09.json`（after）

### R29 / R30
- Before：
  - `issue_type=blocked_without_resolution`
  - `quality_grade=poor`
  - `blocked=true`
  - `resolved=false`
- After：
  - `issue_type=None`
  - `quality_grade=acceptable`
  - `blocked=false`
  - `resolved=false`

### R31 / R32 / R33 / R34
- Before：
  - `issue_type=blocked_without_resolution`
  - `quality_grade=poor`
  - `blocked=true`
  - `resolved=false`
- After：
  - `issue_type=None`
  - `quality_grade=acceptable`
  - `blocked=false`
  - `resolved=false`

### 整包结果变化
- `issue_type_distribution`：
  - Before：`none=28, blocked_without_resolution=6`
  - After：`none=34`
- `quality_grade_distribution`：
  - Before：`acceptable=28, poor=6`
  - After：`acceptable=34`

## §5 是否改善
是：`R29~R34` 的 `blocked_without_resolution` 在本轮收口后全部消失，并且 quality 从 `poor` 回到 `acceptable`。

## §6 是否存在回归（最小回归集）
抽查保持不变（无新增问题）：
- `R23/R24/R25`
- `R17/R18/R19`
- `R11/R14/R16`
- `R6`

## §7 是否建议继续
建议继续：本轮已经把 repeated fallback / retry exhaustion 的收口闭环打通；下一轮可继续把剩余（若有）卡点问题锁定到 `recheck_planner` 的最小动作收口规则上，避免再次出现 blocked 未收口的度量结果。

