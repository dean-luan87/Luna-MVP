# Real Scenario Pack M0.2 / M1（第三批真实场景扩充）交付

## §1 目标
在前两批场景已基本打干净（第二批 Post-Fix 后 `issue_type_distribution = none×10`）的前提下，第三批目标是引入更乱、更接近真实干扰语境的 case，重新制造高价值 triage 输入，而非扩平台。

## §2 本轮新增 case
新增 6 个 `ctx_json` 真实场景：
- `R11_occlusion_plus_competition_real`
- `R12_feedback_ambiguous_real`
- `R13_feedback_conflict_loop_real`
- `R14_task_chain_shift_complex_real`
- `R15_memory_novel_conflict_real`
- `R16_continuity_break_recovery_real`

其中 `R11/R14/R16` 引入高运动失稳（`motion_instability >= 0.9`）以构造更真实的中断/阻断压力。

## §3 整包结果
运行：
- `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m02.json`
- `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m02.json --out logs/benchmark_triage_board_m02.json`

结果摘要：
- `total_cases`: 16
- `passed_cases`: 13
- `quality_grade_distribution`: `acceptable: 13`, `poor: 3`
- `issue_type_distribution`:
  - `none`: 13
  - `blocked_without_resolution`: 3

## §4 新 triage
- worst cases：
  - `R11_occlusion_plus_competition_real`
  - `R14_task_chain_shift_complex_real`
  - `R16_continuity_break_recovery_real`
- top modules：`recheck_planner`
- top issues：`blocked_without_resolution`

## §5 结论
第三批场景成功重新制造有效 triage：问题焦点已从第二批的 `high_dead_branch_ratio/hypothesis_layer` 迁移为 `blocked_without_resolution/recheck_planner`。

下一轮建议优先方向：
- 定点优化 `recheck_planner` 在高失稳/中断语境下的 blocked 收敛路径（优先 R11/R14/R16），避免 `blocked=true 且 resolved=false` 持续留存。

## §6 Post-Fix Rebaseline（M0.2 / M1）
M0.6 定点优化后已完成第三批整包重刷：
- `logs/real_scenario_pack_postfix_m02.json`
- `logs/benchmark_triage_board_postfix_m02.json`

结果：`passed_cases=16/16`，`issue_type_distribution=none×16`，`R11/R14/R16` 的 `blocked_without_resolution` 已消失。详见 `docs/POST_FIX_REBASELINE_M0_2_M1.md`。

## §7 第四批场景启动（M0.3 / M2）
第四批 `R17~R22` 已启动并扩充到整包（见：`docs/REAL_SCENARIO_PACK_M0_3_M2_DELIVERY.md`）。
本轮重新制造了有效 triage：`blocked_without_resolution=6` 且热点模块为 `recheck_planner`。
