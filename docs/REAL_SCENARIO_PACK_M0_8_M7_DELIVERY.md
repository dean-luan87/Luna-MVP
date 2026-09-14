# Real Scenario Pack M0.8 / M7（第九批真实场景扩充）交付

## §1 目标

在第八批已完成「扩包 → M1.1 收口 → Post-Fix 基线 `none×46`」之后，进入**第九批**真实场景：聚焦**长期累积误差、多层约束漂移、伪一致性、慢性错位**等更隐蔽压力，重新制造可定位 triage。本轮只扩 `ctx_json` case 与整包重跑，不引入新平台或新评测体系。

## §2 本轮新增了哪些 case

本轮新增 **6** 个 `ctx_json` 场景（`tests/real_scenarios/ctx/`，`R47`–`R52`）：

| case_id | 轻量语义标志 |
|---------|----------------|
| `R47_gradual_goal_drift_real` | `gradual_goal_drift_expected` |
| `R48_local_recovery_global_mismatch_real` | `local_recovery_global_mismatch_expected` |
| `R49_multi_constraint_soft_shift_real` | `multi_constraint_soft_shift_expected` |
| `R50_feedback_fact_consistent_but_wrong_real` | `feedback_fact_consistent_but_wrong_expected` |
| `R51_task_semantic_crack_real` | `task_semantic_crack_expected` |
| `R52_slow_poisoning_real` | `slow_poisoning_expected` |

说明：上述标志**不在** M1.0 / M1.1 `recheck_planner` 收口白名单内（与第八批扩包期「新标志再暴露 triage」同一工程策略）。

## §3 整包结果

运行：

- `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m08.json`
- `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m08.json --out logs/benchmark_triage_board_m08.json`

统计（共 **52** case）：

- `total_cases`: **52**
- `passed_cases`: **46**
- `quality_grade_distribution`: **acceptable=46**, **poor=6**
- `issue_type_distribution`: **none=46**, **blocked_without_resolution=6**

## §4 新 triage

- **worst cases（poor）**：第九批 **6** 个 case 均为 `poor` 且均为 `blocked_without_resolution`：  
  `R47`–`R52`。
- **top modules**：**`recheck_planner`**（相关 case=6，poor=6，issue_types=[`blocked_without_resolution`]）。
- **top issues**：**`blocked_without_resolution`**（case_count=6；related_modules=[`recheck_planner`]）。

分诊摘要（`logs/benchmark_triage_board_m08.json`）：最差入口侧重 **R47、R48**；`next_focus_issue_types` 含 **`blocked_without_resolution`**。

## §5 结论

- **第九批是否成功制造新的有效 triage**：**是**。整包再次从「无 issue」出现 **6** 条 `blocked_without_resolution`，且全部来自新 case，热点收敛到 **`recheck_planner`**。
- **下一轮建议优先方向**：**Targeted Fix Sprint（建议 M1.2）**——仅对 `recheck_planner` 为 **R47–R52** 的新 `*_expected` 标志增加与 M1.1 同级的最小 actionable fallback 映射（**不改** benchmark/triage 规则），直至 Post-Fix 整包再回到 `none×52`。

## §6 可选单 case 验证

已对 **`R47_gradual_goal_drift_real`**、**`R51_task_semantic_crack_real`** 单独运行 `tools/real_scenario_pack.py --case_id`，确认可加载、可产出 summary。

## §7 M1.2 后收口（Recheck Planner）与基线固化

第九批 triage 驱动的定点收口见 **`docs/TARGETED_FIX_SPRINT_M1_2_RECHECK_M08_EXPECTED_BLOCKED.md`**。收口后整包 **`issue_type_distribution=none×52`**。

**正式固化基线（推荐文件名）：** `logs/real_scenario_pack_postfix_m08.json`、`logs/benchmark_triage_board_postfix_m08.json`。

**Post-Fix 重刷结论与 before/after：** **`docs/POST_FIX_REBASELINE_M0_8_M7.md`**（第九批修复后统一核验与下一轮决策落点）。
