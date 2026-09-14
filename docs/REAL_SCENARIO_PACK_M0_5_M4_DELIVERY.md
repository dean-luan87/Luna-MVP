# Real Scenario Pack M0.5 / M4（第六批真实场景扩充）交付

## §1 目标
在前五批真实场景扩充 + M0.8 后已将 `blocked_without_resolution` 再次收敛的基础上，本轮进入第六批真实场景扩充：目标是重新制造“复杂意图 × 执行分裂 × 多阶段扰动”的有效 triage 压力源，让分诊热点再次可观测并可用于下一轮定点优化。

## §2 本轮新增了哪些 case
本轮新增 6 个 `ctx_json` 真实场景：
- `R29_goal_drift_real`
- `R30_success_criteria_shift_real`
- `R31_multi_insertion_chain_real`
- `R32_feedback_action_divergence_real`
- `R33_memory_fast_environment_shift_real`
- `R34_recovery_under_second_disturbance_real`

## §3 整包结果
本轮运行：
- `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m05.json`
- `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m05.json --out logs/benchmark_triage_board_m05.json`

整包统计（共 34 case）：
- `total_cases`: 34
- `passed_cases`: 28
- `quality_grade_distribution`: `acceptable=28`, `poor=6`
- `issue_type_distribution`: `none=28`, `blocked_without_resolution=6`

## §4 新 triage
- worst cases（poor）：
  - `R29_goal_drift_real`
  - `R30_success_criteria_shift_real`
  - `R31_multi_insertion_chain_real`
  - `R32_feedback_action_divergence_real`
  - `R33_memory_fast_environment_shift_real`
  - `R34_recovery_under_second_disturbance_real`
- top modules：
  - `recheck_planner`（相关 case=6，poor=6，issue_types=[`blocked_without_resolution`]）
- top issues：
  - `blocked_without_resolution`（case_count=6；related_modules=[`recheck_planner`]）

## §5 结论
第六批成功再次制造新的有效 triage：`blocked_without_resolution` 重新在整包中出现（6/34），且热点模块清晰收敛到 `recheck_planner`。

下一轮建议优先方向：
- 继续围绕 `recheck_planner` 的“repeated_fallback / blocked 语境下的可执行 fallback 与 blocked 收口”做最小定点优化。

## §6 本轮下一步：第七批真实场景扩充（M0.6 / M5）
第七批扩充与分诊结果见 `docs/REAL_SCENARIO_PACK_M0_6_M5_DELIVERY.md`。

## §6 M0.9 后基线固化（Post-Fix Rebaseline）
在 `docs/POST_FIX_REBASELINE_M0_5_M4.md` 中，已确认 M0.9 后第六批整包：
- `passed_cases=34`
- `issue_type_distribution=none×34`
- triage 再次清空（`ranked_modules=[]`、`ranked_issues=[]`）

