# Real Scenario Pack M0.4 / M3（第五批真实场景扩充）交付

## §1 目标
在前四批真实场景扩充 + 已修复收口基础上，本轮继续扩充第五批更高阶的行为级真实场景，目标是重新制造“有效 triage 压力源”，推动评测从单点问题走向更复杂的链路/背离/恢复失败语境。

## §2 本轮新增了哪些 case
本轮新增 6 个 `ctx_json` 真实场景：
- `R23_long_chain_recovery_fail_real`
- `R24_explicit_user_noncompliance_real`
- `R25_task_loss_after_insertion_real`
- `R26_memory_override_failure_real`
- `R27_multi_object_multi_feedback_real`
- `R28_continuity_second_recovery_real`

本批关键设计：保持 `search_terminal_status="blocked"`，并使用 **非 `unknown` 的 `confirmation_input_type`** 来重新制造 blocked 类 triage 可见性。

## §3 整包结果
本轮运行：
- `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m04.json`
- `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m04.json --out logs/benchmark_triage_board_m04.json`

整包统计（共 28 case）：
- `total_cases`: 28
- `passed_cases`: 22
- `quality_grade_distribution`: `acceptable=22`, `poor=6`
- `issue_type_distribution`: `none=22`, `blocked_without_resolution=6`

## §4 新 triage
- worst cases（top3）：
  - `R23_long_chain_recovery_fail_real`
  - `R24_explicit_user_noncompliance_real`
  - `R25_task_loss_after_insertion_real`
- top modules：
  - `recheck_planner`（相关 case=6，poor=6，issue_types=[`blocked_without_resolution`]）
- top issues：
  - `blocked_without_resolution`（case_count=6；related_modules=[`recheck_planner`]）

结论：本轮 triage 明确非空，且热点重新收敛到 `recheck_planner` 与 `blocked_without_resolution` 组合。

## §5 结论
第五批成功制造新的有效 triage：`blocked_without_resolution` 重新在整包中出现（6/28），且主要由 `recheck_planner` 侧触发/解释。

下一轮建议优先方向：
- 针对本批触发的 `blocked_without_resolution`，继续把最小收敛靶子落在 `recheck_planner` 的“blocked 语境下 fallback 选择与可执行性判定”。

## §6 M0.8 后基线固化（Post-Fix Rebaseline）
在 `docs/POST_FIX_REBASELINE_M0_4_M3.md` 中，已确认 M0.8 后第五批整包 `issue_type_distribution=none×28`，分诊再次清空。

## §7 本轮启动：第六批真实场景扩充（M0.5 / M4）
第六批扩充与分诊结果见 `docs/REAL_SCENARIO_PACK_M0_5_M4_DELIVERY.md`。

