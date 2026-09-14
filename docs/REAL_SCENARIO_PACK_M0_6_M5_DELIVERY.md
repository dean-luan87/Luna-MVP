# Real Scenario Pack M0.6 / M5（第七批真实场景扩充）交付

## §1 目标
在前六批真实场景已完成“扩包 → triage → 定点修复 → 重刷基线”收口之后，本轮进入第七批真实场景扩充：引入更高阶的意图链 / 动作链 / 任务链错位语境，重新制造新的有效 triage 压力源，为下一轮定点优化提供可定位靶子。

## §2 本轮新增了哪些 case
本轮新增 6 个 `ctx_json` 真实场景：
- `R35_intent_action_task_mismatch_real`
- `R36_confirmed_but_not_executed_real`
- `R37_executed_but_goal_shifted_real`
- `R38_subtask_return_semantic_loss_real`
- `R39_fact_feedback_stage_conflict_real`
- `R40_false_recovery_real`

## §3 整包结果
本轮运行：
- `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m06.json`
- `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m06.json --out logs/benchmark_triage_board_m06.json`

整包统计（共 40 case）：
- `total_cases`: 40
- `passed_cases`: 34
- `quality_grade_distribution`: `acceptable=34`, `poor=6`
- `issue_type_distribution`: `none=34`, `blocked_without_resolution=6`

## §4 新 triage
- worst cases（poor）：
  - `R35_intent_action_task_mismatch_real`
  - `R36_confirmed_but_not_executed_real`
  - `R37_executed_but_goal_shifted_real`
  - `R38_subtask_return_semantic_loss_real`
  - `R39_fact_feedback_stage_conflict_real`
  - `R40_false_recovery_real`
- top modules：
  - `recheck_planner`（相关 case=6，poor=6，issue_types=[`blocked_without_resolution`]）
- top issues：
  - `blocked_without_resolution`（case_count=6；related_modules=[`recheck_planner`]）

## §5 结论
第七批成功制造新的有效 triage：本轮新增的 6 个 case 再次触发 `blocked_without_resolution`，热点模块清晰收敛到 `recheck_planner`。

下一轮建议优先方向：
- 针对这批场景触发的 `blocked_without_resolution`，在 `recheck_planner` 侧继续做最小收口（避免再次陷入 blocked/unresolved），并围绕这批“意图-动作-任务错位语境”的差异做定点增强。

## §6 M1.0 后基线固化（Post-Fix Rebaseline）
在 `docs/POST_FIX_REBASELINE_M0_6_M5.md` 中，已确认 M1.0 后第七批整包 `issue_type_distribution=none×40`，分诊再次清空。

## §7 第八批启动（M0.7 / M6）
更高阶真实场景（社会性扰动 / 长链语义漂移 / 多方约束冲突）见 **`docs/REAL_SCENARIO_PACK_M0_7_M6_DELIVERY.md`**（整包产物：`logs/real_scenario_pack_m07.json`、`logs/benchmark_triage_board_m07.json`）。

