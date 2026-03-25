# Targeted Fix Sprint M1.2 — Recheck Planner（第九批新 expected 标志 blocked 收口）

## 目标场景

| case_id | ctx 标志 |
|---------|----------|
| `R47_gradual_goal_drift_real` | `gradual_goal_drift_expected` |
| `R48_local_recovery_global_mismatch_real` | `local_recovery_global_mismatch_expected` |
| `R49_multi_constraint_soft_shift_real` | `multi_constraint_soft_shift_expected` |
| `R50_feedback_fact_consistent_but_wrong_real` | `feedback_fact_consistent_but_wrong_expected` |
| `R51_task_semantic_crack_real` | `task_semantic_crack_expected` |
| `R52_slow_poisoning_real` | `slow_poisoning_expected` |

## 目标问题

- **metrics**：`blocked_without_resolution`（结构树 `blocked` 且未 `resolved`）
- **根因**：M1.0 / M1.1 白名单**未**包含第九批上述标志；`recheck_planner` 仍可能停在 **recheck_blocked** 语境。
- **约束**：只改 `recheck_planner`；不改 triage / metrics / 结构树公式。

## 调整内容（最小规则）

在 `decision_monitor/recheck_planner.py` 的 **`build_recheck_planner`** 内、**M1.1 之后**、hypothesis 分支之前，新增 **M1.2**：

- `m12_flag_tags` 映射 6 个标志 → 语义 tag（`recheck_reason` 仅作区分，**动作为 `ask_user_for_clarification`**，与 M1.1 一致）：
  - `gradual_goal_drift_expected` → `clarify_objective_drift`
  - `local_recovery_global_mismatch_expected` → `clarify_local_vs_global_objective`
  - `multi_constraint_soft_shift_expected` → `reframe_success_under_soft_shift`
  - `feedback_fact_consistent_but_wrong_expected` → `challenge_surface_consistency_reframe_goal`
  - `task_semantic_crack_expected` → `clarify_task_semantics_rebuild`
  - `slow_poisoning_expected` → `clarify_slow_drift_resistance`
- 统一：`recheck_applied=True`，`recheck_blocked=False`。

## Before / After（整包 `tools/real_scenario_pack.py`）

**Before（M1.2 前，扩包产物 `logs/real_scenario_pack_m08.json`）**

| 指标 | 值 |
|------|-----|
| total_cases | 52 |
| passed_cases | 46 |
| quality | acceptable=46, poor=6 |
| issue_type_distribution | none=46, **blocked_without_resolution=6** |
| 受影响 | **R47–R52** 均为 poor + blocked_without_resolution |

**After（M1.2 后，`logs/real_scenario_pack_postfix_m08.json`）**

| 指标 | 值 |
|------|-----|
| total_cases | 52 |
| passed_cases | **52** |
| quality | **acceptable=52** |
| issue_type_distribution | **none=52** |
| triage | `ranked_modules=[]`，`ranked_issues=[]` |

### R47 / R48 / R49 字段对比（摘录）

| 字段 | R47–R49 before | R47–R49 after |
|------|----------------|---------------|
| issue_type | blocked_without_resolution | **null** |
| quality_grade | poor | **acceptable** |
| blocked | true | **false** |
| optimization_hint_type | resolve_blocked_state | **none** |
| optimization_validation_result | not_enough_data | **not_applicable** |

树结构指标（depth / path length / effective_feedback_count）前后一致。

### R50 / R51 / R52

与 R47–R49 **同模式改善**（issue 清零、acceptable、blocked=false）。

## 回归

整包 **52/52 passed**；**R6、R11、R14、R16、R17–R19、R23–R25、R29–R34、R35–R46** 均为 acceptable、无 issue 回归。

## 是否改善

**是**：`blocked_without_resolution` **整包清零**；第九批 6 case 全部 **pass**。

## 是否建议继续

- **可选**：若再扩第十批，为新 `*_expected` 重复 **M1.x 映射** 模式即可。
- **重跑命令**：

```bash
python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_postfix_m08.json
python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_postfix_m08.json --out logs/benchmark_triage_board_postfix_m08.json
```

## 验证

- 单测：`tests/test_recheck_m08_expected_blocked_fix.py`

## 结论

**通过**：R47–R52 核心指标改善；**仅改 `recheck_planner`**；**CONTRACT** 已补充 M1.2 说明。
