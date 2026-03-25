# Real Scenario Pack M0.7 / M6（第八批真实场景扩充）交付

## §1 目标

在第七批已完成扩包与 M1.0 后基线（整包 `issue_type_distribution=none×40`、分诊暂时清空）的前提下，进入**第八批**更高阶真实场景：聚焦**社会性扰动 / 长链语义漂移 / 多方约束冲突**，用新语义载体重新制造**可定位 triage**，为下一轮定点优化提供靶子。本轮只做真实 case 扩充与整包重跑，不引入新平台或新评测体系。

## §2 本轮新增了哪些 case

本轮新增 **6** 个 `ctx_json` 真实场景（均在 `tests/real_scenarios/ctx/`，主键 `R41`–`R46`）：

- `R41_confirmed_but_long_term_diverged_real` — `long_term_divergence_expected`
- `R42_task_subtask_fact_shift_real` — `task_subtask_fact_shift_expected`
- `R43_success_condition_overwritten_real` — `success_condition_overwritten_expected`
- `R44_false_multi_recovery_real` — `false_multi_recovery_expected`
- `R45_multi_feedback_source_conflict_real` — `multi_feedback_source_conflict_expected`
- `R46_delayed_exposure_mismatch_real` — `delayed_exposure_mismatch_expected`

说明：上述 `*_expected` 字段**不在** `recheck_planner` 的 M1.0「错位语境」收口白名单内，因此可再次暴露 `blocked_without_resolution` 类度量与分诊（与 R35–R40 已收口字段区分）。

## §3 整包结果

本轮运行：

- `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m07.json`
- `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m07.json --out logs/benchmark_triage_board_m07.json`

整包统计（共 **46** case）：

- `total_cases`: 46
- `passed_cases`: 40
- `quality_grade_distribution`: `acceptable=40`, `poor=6`
- `issue_type_distribution`: `none=40`, `blocked_without_resolution=6`

## §4 新 triage

- **worst cases（poor）**：本轮新增 6 个 case **全部**为 `poor`，且均带 `blocked_without_resolution`：
  - `R41_confirmed_but_long_term_diverged_real`
  - `R42_task_subtask_fact_shift_real`
  - `R43_success_condition_overwritten_real`
  - `R44_false_multi_recovery_real`
  - `R45_multi_feedback_source_conflict_real`
  - `R46_delayed_exposure_mismatch_real`
- **top modules**：`recheck_planner`（相关 case=6，poor=6，issue_types=[`blocked_without_resolution`]）
- **top issues**：`blocked_without_resolution`（case_count=6；related_modules=[`recheck_planner`]）

分诊板摘要（`logs/benchmark_triage_board_m07.json`）：优先关注 `R41`–`R43` 作为最差队列入口；`next_focus_issue_types` 含 `blocked_without_resolution`。

## §5 结论

- **第八批是否成功制造新的有效 triage**：是。整包从「无 issue」回到 **6** 条 `blocked_without_resolution`，且全部来自新一批更高阶语义场景，热点模块清晰收敛到 **`recheck_planner`**。
- **下一轮建议优先打什么**：在**不破坏 M1.0 已对 R35–R40 错位语境收口**的前提下，为 **R41–R46** 增加**独立、最小**的 planner/树度量收口路径（例如将本批 `*_expected` 纳入与 R35–R40 同级的“强制澄清/可行动 fallback”分支，或调整结构树 blocked 判定与 experience governance 交互），使整包重新趋向 `none×46` 或可控弱告警。

## §6 可选单 case 验证

曾对至少 2 个新增 case 单独运行 `tools/real_scenario_pack.py --case_id <id>`，确认可加载、可产出 summary。

## §7 M1.1 后收口（Recheck Planner）与基线固化

第八批 triage 驱动的定点收口见 **`docs/TARGETED_FIX_SPRINT_M1_1_RECHECK_NEW_EXPECTED_BLOCKED.md`**。收口后整包可重跑为 **`issue_type_distribution=none×46`**。

**正式固化基线（推荐文件名）：** `logs/real_scenario_pack_postfix_m07.json`、`logs/benchmark_triage_board_postfix_m07.json`；before/after 与 triage 清空结论见 **`docs/POST_FIX_REBASELINE_M0_7_M6.md`**（历史跑数亦可能见 `logs/real_scenario_pack_m11_postfix.json`）。

## §8 第九批启动（M0.8 / M7）

更高阶「累积误差 / 慢性错位 / 伪一致性」真实场景见 **`docs/REAL_SCENARIO_PACK_M0_8_M7_DELIVERY.md`**（整包产物示例：`logs/real_scenario_pack_m08.json`、`logs/benchmark_triage_board_m08.json`）。
