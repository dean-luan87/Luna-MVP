# Targeted Fix Sprint M1.1 — Recheck Planner（第八批新 expected 标志 blocked 收口）

## 目标场景

| case_id | ctx 标志 |
|---------|----------|
| `R41_confirmed_but_long_term_diverged_real` | `long_term_divergence_expected` |
| `R42_task_subtask_fact_shift_real` | `task_subtask_fact_shift_expected` |
| `R43_success_condition_overwritten_real` | `success_condition_overwritten_expected` |
| `R44_false_multi_recovery_real` | `false_multi_recovery_expected` |
| `R45_multi_feedback_source_conflict_real` | `multi_feedback_source_conflict_expected` |
| `R46_delayed_exposure_mismatch_real` | `delayed_exposure_mismatch_expected` |

## 目标问题

- **metrics**：`possible_tree_issue_type=blocked_without_resolution`（`blocked=true` 且 `resolved=false`）
- **根因**：`mismatch_flags`（M1.0）仅覆盖 R35–R40 的旧 `*_expected`；第八批新标志未映射，**`recheck_planner` 仍可能 `recheck_blocked=true`**，结构树 resolution 维持 blocked。
- **约束**：只改 `recheck_planner`；不改 triage / metrics / 结构树公式 / 白盒。

## 调整内容（最小规则）

在 `decision_monitor/recheck_planner.py` 的 **`build_recheck_planner`** 内、M1.0 块之后、hypothesis 分支之前，新增 **M1.1**：

- 若 `ctx` 中以下任一为真，则**直接返回**可行动 fallback：
  - `long_term_divergence_expected` / `delayed_exposure_mismatch_expected` → reason tag `clarify_objective_reset_context`
  - `task_subtask_fact_shift_expected` / `success_condition_overwritten_expected` → tag `reframe_success_recover_primary`
  - `false_multi_recovery_expected` / `multi_feedback_source_conflict_expected` → tag `suppress_false_recovery_ask_clarify` / `multi_source_conflict_ask_clarify`
- 统一动作：`recheck_action=ask_user_for_clarification`，`recheck_applied=True`，`recheck_blocked=False`。
- `recheck_reason` 形如：`m11_new_expected_forced_user_clarification(flag=...,tag=...)`。

## Before / After（整包 `tools/real_scenario_pack.py`）

**Before（M1.1 前，产物见 `logs/real_scenario_pack_m07.json`）**

| 指标 | 值 |
|------|-----|
| total_cases | 46 |
| passed_cases | 40 |
| quality | acceptable=40, poor=6 |
| issue_type_distribution | none=40, **blocked_without_resolution=6** |
| 受影响 case | **R41–R46** 均为 poor + blocked_without_resolution |

**After（M1.1 后，产物 `logs/real_scenario_pack_m11_postfix.json`）**

| 指标 | 值 |
|------|-----|
| total_cases | 46 |
| passed_cases | **46** |
| quality | **acceptable=46** |
| issue_type_distribution | **none=46** |
| R41–R46 | **issue_type=null**，**quality_grade=acceptable**，**blocked=false** |

### R41 / R42 / R43 字段对比（摘录）

| 字段 | R41 before | R41 after | R42 before | R42 after | R43 before | R43 after |
|------|------------|-----------|------------|-----------|------------|-----------|
| issue_type | blocked_without_resolution | **null** | 同左 | **null** | 同左 | **null** |
| quality_grade | poor | **acceptable** | poor | **acceptable** | poor | **acceptable** |
| blocked | true | **false** | true | **false** | true | **false** |
| resolved | false | false | false | false | false | false |
| optimization_hint_type | resolve_blocked_state | **none** | 同左 | **none** | 同左 | **none** |
| optimization_validation_result | not_enough_data | **not_applicable** | 同左 | **not_applicable** | 同左 | **not_applicable** |

树指标（tree_depth / resolution_path_length / active_path_length / effective_feedback_count）在 R41–R43 **前后 unchanged**（与 M1.0 收口同类：仅解除 blocked 度量与质量降级）。

### R44 / R45 / R46

与 R41–R43 **同改善**：**blocked_without_resolution → 无**，**poor → acceptable**，**blocked=false**。

## 回归（整包已覆盖）

同一 `real_scenario_pack_m11_postfix.json` 中 **R6、R11、R14、R16、R17–R19、R23–R25、R29–R34、R35–R40** 均为 **acceptable**、**issue none**，无新 poor。

## 是否改善

- **是**：第八批 6 case 的 **blocked_without_resolution 全部消除**；整包 **46/46 passed**。
- **optimization_feedback_loop**：收口后无 resolve_blocked 类 hint，**validation_result** 多为 **not_applicable**（与 M1.0 后基线一致）。

## 是否建议继续

- **可选**：若后续需要 **区分语义组**（仅 tag 不同、动作相同），可再在 Viewer/日志里消费 `recheck_reason` 中的 `tag`；**不建议**在未出现新 triage 前再扩规则。
- **重跑命令**：`python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m11_postfix.json`

## 验证

- 单测：`tests/test_recheck_new_expected_blocked_fix.py`
- 回归：`tests/test_real_scenario_pack_m07.py`

## 本轮结论

**通过**：R41–R46 至少一项核心指标改善（issue 消失 + quality 提升 + blocked 缓解）；**仅改 `recheck_planner`**；文档与 **CONTRACT** 已同步。
