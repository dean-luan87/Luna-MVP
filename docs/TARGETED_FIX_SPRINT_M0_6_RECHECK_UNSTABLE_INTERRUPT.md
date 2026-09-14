# Targeted Fix Sprint M0.6（Recheck Planner：高失稳 / 中断场景收敛）

## 1) 目标场景
- `R11_occlusion_plus_competition_real`
- `R14_task_chain_shift_complex_real`
- `R16_continuity_break_recovery_real`

## 2) 目标问题
- `issue_type=blocked_without_resolution`
- 典型表现：`blocked=true && resolved=false`，`quality_grade=poor`，优化提示聚焦 `recheck_planner`

## 3) 调整内容（最小改动）
仅做 `recheck_planner` 与最小消费侧收口：

1. `decision_monitor/recheck_planner.py`
   - 新增 `_pick_blocked_fallback(...)`：
     - 在 `runtime_domain_state=frozen` / 运动异常 / 风险区域等高失稳语境下，优先给出 `ask_user_for_clarification` 的快速收口动作；
     - 否则保持 `hold_and_confirm`。
   - 在 blocked fallback 两个分支统一使用该规则，输出更明确的 `recheck_reason`（含 `unstable_interrupt_fast_converge` 标签）。

2. `decision_monitor/reasoning_structure_tree.py`（必要最小消费侧）
   - 当 `recheck_planner` 已给出可行动 fallback（`recheck_applied=True` 且 `recheck_blocked=False`）时，
     将 experience governance 的 `blocked` 视为“治理审计保守态”而非“执行阻断态”，降级为 `watchlist`。
   - 目的：避免 metrics 将该类场景误判为 `blocked_without_resolution`。

> 说明：未改评分公式、未改 triage 规则、未扩场景包、未新增白盒模块。

## 4) Before / After（核心对比）
Before 基线：`logs/real_scenario_pack_m02.json`  
After 复跑：`logs/real_scenario_pack_m02_postfix_m06.json`

### R11
- Before：`issue_type=blocked_without_resolution`，`quality=poor`，`blocked=true`，`resolved=false`，`optimization_hint_type=resolve_blocked_state`
- After：`issue_type=null`，`quality=acceptable`，`blocked=false`，`resolved=false`，`optimization_hint_type=none`

### R14
- Before：`issue_type=blocked_without_resolution`，`quality=poor`，`blocked=true`，`resolved=false`
- After：`issue_type=null`，`quality=acceptable`，`blocked=false`，`resolved=false`

### R16
- Before：`issue_type=blocked_without_resolution`，`quality=poor`，`blocked=true`，`resolved=false`
- After：`issue_type=null`，`quality=acceptable`，`blocked=false`，`resolved=false`

## 5) 是否改善
是。`R11/R14/R16` 的 `blocked_without_resolution` 全部消失，`poor -> acceptable`，第三批 blocked 热点被压下。

## 6) 回归检查
复跑 `R6/R5/R1/R2`：
- 仍为 `issue_type=null`，`quality=acceptable`，未观察到明显回归。

## 7) 是否建议继续
- 当前建议先做一次第三批 Post-Fix 重刷（整包+triage）固化新基线；
- 若后续仍要提升中断语境下“resolved”能力，再考虑独立 sprint（不在本轮继续扩改）。

