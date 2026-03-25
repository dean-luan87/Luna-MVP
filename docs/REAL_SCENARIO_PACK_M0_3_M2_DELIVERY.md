# Real Scenario Pack M0.3 / M2（第四批真实场景扩充）交付

## §1 目标
在前三批真实场景扩充 + 已修复的 M0.6 收口基础上，本轮继续引入更高阶、更接近真实混乱交互的第四批 case，目标是重新制造“有效 triage”输入（而不是平台改造）。

## §2 本轮新增 case
本轮新增 6 个 `ctx_json` 真实场景（第四批）：
- `R17_multi_step_feedback_repair_real`
- `R18_user_system_divergence_real`
- `R19_task_insertion_interrupt_real`
- `R20_target_switch_real`
- `R21_memory_mislead_real`
- `R22_continuity_recovery_fail_real`

本轮关键实现：为保证在当前 M0.6 修复后仍能可见生成 triage，本批 ctx 统一将 `search_terminal_status="blocked"`，同时保持 `motion_instability` 较低以避免触发已收口的 frozen/hold_for_floor 阻断路径。

## §3 整包结果
运行：
- `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m03.json`
- `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m03.json --out logs/benchmark_triage_board_m03.json`

整包统计（22 case）：
- `total_cases`: 22
- `passed_cases`: 16
- `quality_grade_distribution`: `acceptable=16`, `poor=6`
- `issue_type_distribution`：
  - `none`: 16
  - `blocked_without_resolution`: 6

## §4 新 triage
`benchmark_triage_board_m03.json` 的结论：
- worst cases（top3）：
  - `R17_multi_step_feedback_repair_real`
  - `R18_user_system_divergence_real`
  - `R19_task_insertion_interrupt_real`
- top modules：`recheck_planner`
- top issues：`blocked_without_resolution`
- triage 是否清空：否（本轮产生明确问题热点）

## §5 结论
第四批场景成功制造新的有效 triage：热点回到 `blocked_without_resolution`，且主要集中在 `recheck_planner` 模块侧。

下一轮建议优先方向（用于定点优化的清晰起点）：
- 重点打 `R17~R22` 这类“terminal=blocked 但未进入已修复收口路径”的中断语境
- 优先在 `recheck_planner` 侧继续做最小收敛（目标是让 blocked_without_resolution 再次下降或消失）

## §6 M0.7 后基线固化（Post-Fix Rebaseline）
在 `docs/POST_FIX_REBASELINE_M0_3_M2.md` 中，已确认 M0.7 后第四批整包 `issue_type_distribution=none×22`、分诊再次清空。

## §7 本轮启动：第五批真实场景扩充（M0.4 / M3）
第五批扩充与重刷结果见 `docs/REAL_SCENARIO_PACK_M0_4_M3_DELIVERY.md`。

