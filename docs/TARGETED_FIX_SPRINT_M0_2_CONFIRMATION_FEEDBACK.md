# Targeted Fix Sprint M0.2 — Confirmation Input Bridge（反馈收敛定点优化）

## 1. 目标场景

- 目标 case：`R5_feedback_ineffective_real`
- 目标模块：`confirmation_input_bridge`
- 目标问题：用户反馈存在但推进弱（反馈映射不稳 / next_effect 不明确）

## 2. 调整内容（最小规则）

仅对 `decision_monitor/confirmation_input_bridge.py` 做 1 组最小规则增强：

1) **提高“已检查”反馈映射命中**  
新增短语命中：`我已经看过了/我看过了/看过了` → `checked_and_not_found`

2) **提高 checked_and_not_found 的推进力度**  
在 `container_check_flow` 与 general flow 下：`checked_and_not_found` → `advance_to_recheck`  
（让“用户已检查”能更稳定推动下一步补证/推进，而不是停留在弱反馈）

## 3. before / after（R5 对比）

### before（基线）

来自：`logs/_tmp_R5_before.json`

- effective_feedback_count：**1**
- quality_grade：acceptable
- issue_type：high_dead_branch_ratio
- active_path_length：4

### after（优化后）

来自：`logs/_tmp_R5_after.json`

- effective_feedback_count：**2**（上升）
- quality_grade：acceptable（保持）
- issue_type：high_dead_branch_ratio（保持）
- active_path_length：4（保持）

**结论**：反馈推进有效性上升（至少一项核心指标改善），符合“定点优化、小改可回归”的目标。

## 4. 回归影响（轻回归）

使用同一 real_scenario_pack 回归：

- `R6_blocked_or_fallback_real`：保持 acceptable（且 effective_feedback_count=2）
- `R1_container_real`：保持 acceptable

未观察到明显回归。

## 5. 是否建议继续

下一轮仍按 triage 顺序推进：`R1_container_real` → `hypothesis_layer`，压 `high_dead_branch_ratio`。

