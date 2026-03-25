# Targeted Fix Sprint M0.1 — Recheck Planner（Blocked/Fallback 定点优化）

## 1. 目标场景

- 目标 case：`R6_blocked_or_fallback_real`
- 目标模块：`recheck_planner`
- 目标问题：优先打掉 `blocked_without_resolution`，缩短 blocked/fallback 的无解停留

## 2. 调整内容（最小规则）

在 `decision_monitor/recheck_planner.py` 增加 **Blocked 时的 fallback 收口**（M0.1）：

- 当判定 blocked 时，不再仅输出 `recheck_blocked=true & recheck_applied=false`
- 改为输出一个 **安全且可行动的 fallback**：
  - `hold_and_confirm`（或兜底 `ask_user_for_clarification`）
  - `recheck_priority=high`
  - `recheck_applied=true`
  - 并将 `recheck_blocked` 置为 false（避免长期卡在 blocked 无解态）

## 3. before / after（R6 对比）

### before（基线）

来自：`logs/_tmp_R6_before.json`

- issue_type：`blocked_without_resolution`
- quality_grade：`poor`
- blocked/resolved：blocked=true, resolved=false
- tree_depth：6
- active_path_length：5
- dead_branch_count：2

### after（优化后）

来自：`logs/_tmp_R6_after_ctx.json`（R6 使用 ctx_json 驱动，确保能反映代码改动）

- issue_type：`high_dead_branch_ratio`（blocked_without_resolution 消失）
- quality_grade：`acceptable`
- blocked/resolved：blocked=false, resolved=false
- tree_depth：5（下降）
- active_path_length：4（下降）
- effective_feedback_count：1（上升）

**结论**：blocked/fallback 的“卡住出不来”已被收口为可行动 fallback；R6 从 poor 提升到 acceptable。

## 4. 回归影响（轻回归）

- `R5_feedback_ineffective_real`：仍为 poor（未在本轮范围内修复，符合预期）
- `R1_container_real`：保持 acceptable（无明显回归）

## 5. 是否建议继续

建议继续下一轮定点优化顺序不变：

1. `R5_feedback_ineffective_real` → `confirmation_input_bridge`（提升 feedback convergence）
2. `R1_container_real` → `hypothesis_layer`（压 high_dead_branch_ratio）

本轮不扩平台、不改 metrics/树模型，仅对 `recheck_planner` 做最小可验证改动，已达到阶段目标。

