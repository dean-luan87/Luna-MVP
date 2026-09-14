# Targeted Fix Sprint M0.5 — Hypothesis Layer（Hold-for-floor / Fine-interaction 分支收敛）

## 1. 目标场景

- `R8_multi_candidate_container_real`
- `R10_partial_memory_vs_novel_real`

（输入均为 `ctx_json`，且含 `detector_floor_due: true`，使 `goal_resolver` 进入 `hold_for_floor`，`skeleton_mix` 常为 `fine_interaction` 主导。）

## 2. 目标问题

- `issue_type`: `high_dead_branch_ratio`
- 表征：`prune_rate=0.667`，`branch_count=3`，`dead_branch_count=2`（见整包产物 `logs/real_scenario_pack_m01.json` 中 R8/R10 条目标签）

根因（实现层面，最小归纳）：`container_hint` 已将 `max_hypotheses` 收紧为 1，但 `interaction_target_candidate` 仍通过 `len(hypotheses) < max_hypotheses + 1` 塞入第二条假设，并在其后将 `max_hypotheses` 放宽为 2，使结构树仍产生「双假设 → pruned alternative」类死分支噪声。

## 3. 调整内容（仅 `hypothesis_layer` + builder 传参）

- `build_hypothesis_layer(..., goal=None)`：新增可选 `goal`（默认 `None` 保持兼容）。
- `decision_monitor/builder.py`：构建假设层时传入 `goal=goal`。
- **M0.5 规则**：当 `goal.goal_type == "hold_for_floor"` 且 `mix.dominant_skeleton == "fine_interaction"` 时，**不追加** `interaction_target_candidate`，并从而在 `hypothesis_reason_summary` 后缀标记 `m05_hold_floor_fine_no_parallel_interaction_target`。

未修改：结构树、metrics/quality 公式、triage、真实场景包、confirmation/recheck 主逻辑。

## 4. Before / After（核心字段）

数据来源：

- **Before**：`logs/real_scenario_pack_m01.json`（M0.1 第二批整包，修复前）
- **After**：本轮本地复跑 `run_real_cases(case_id)`（修复后）

| case_id | 指标 | Before | After |
|--------|------|--------|-------|
| R8 | issue_type | `high_dead_branch_ratio` | `null` |
| R8 | prune_rate | 0.667 | 0.5 |
| R8 | branch_count | 3 | 2 |
| R8 | dead_branch_count | 2 | 1 |
| R10 | issue_type | `high_dead_branch_ratio` | `null` |
| R10 | prune_rate | 0.667 | 0.5 |
| R10 | branch_count | 3 | 2 |
| R10 | dead_branch_count | 2 | 1 |

`quality_grade`：前后均为 `acceptable`；`optimization_hint_type`：R8/R10 由 `reduce_dead_branches` 变为 `none`；`optimization_validation_result`：仍为 `not_applicable`（hint 未再触发 loop 对比路径）。

## 5. 回归（R1 / R2 / R5 / R6）

本轮复跑上述 case_id，**未观察到 issue / prune / branch / dead 相对既有基线恶化**（仍为 `issue=null`，`prune=0.5`，`branch=2`，`dead=1`）。

## 6. 是否改善

是：`high_dead_branch_ratio` 在 R8、R10 上消除；`prune_rate`、`branch_count`、`dead_branch_count` 均下降。

## 7. 是否建议继续

- 若第二批整包 triage 中已不再出现 R8/R10 类 `high_dead_branch_ratio`，可重刷 `real_scenario_pack_m01.json` + `benchmark_triage_board_m01.json` 确认全包分布。
- 若仍有个案在**非 hold_for_floor** 路径上出现类似并行假设噪声，再开独立 sprint（勿在本轮继续堆规则）。
