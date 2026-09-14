# Real Scenario Pack M0.1（第二批真实场景扩充）交付

## §1 目标
第一批真实场景（R1~R6）在后续修复后，整包 `issue_type_distribution` 基本清空，导致主线缺少新的“有效 triage 压力源”。本轮进入第二批真实场景扩充（M0.1），通过新增更复杂的交互载体输入，重新制造可分诊的高优先级 issue 分布，为下一轮定点优化提供清晰目标。

本轮约束不变：复用 `ScenarioBenchmarkCase/ScenarioBenchmarkResult` 与 `real_scenario_pack.py + benchmark_triage_board.py` 统一结构；不引入新平台/新白盒模块。

## §2 本轮新增 case
本轮新增 4 个真实场景（均使用 `ctx_json` 输入载体）：
- `R7_occlusion_complex_real`（occlusion_search）
- `R8_multi_candidate_container_real`（container_search）
- `R9_feedback_conflict_real`（feedback_effective）
- `R10_partial_memory_vs_novel_real`（general_search）

注：为确保第二批能重新“暴露”有效 triage，`R7~R10` 的 ctx 都加入了 `detector_floor_due: true`，将目标推入 `hold_for_floor`，使 `fine_interaction` 主导并更容易触发多分支生成，从而让 triage 在本轮产生新的高优先级 issue。

## §3 整包结果
运行：`python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m01.json`

关键指标（整包 10/10 通过）：
- `total_cases`: 10
- `passed_cases`: 10
- `quality_grade_distribution`: `acceptable: 10`
- `issue_type_distribution`:
  - `none`: 8
  - `high_dead_branch_ratio`: 2

本轮 worst cases：
- `R8_multi_candidate_container_real`
- `R10_partial_memory_vs_novel_real`
- `R1_container_real`（作为基线对照，仍在最差 top3 内）

## §4 新 triage
运行：`python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m01.json --out logs/benchmark_triage_board_m01.json`

- worst cases：`R8_multi_candidate_container_real`, `R10_partial_memory_vs_novel_real`
- top modules：`hypothesis_layer`
- top issues：`high_dead_branch_ratio`（case_count=2）

三项指向一致：本轮的“有效 triage”主要集中在假设生成与剪枝/排除分支结构的质量差异上（`hypothesis_layer` 相关）。

## §5 结论
第二批真实场景扩充 M0.1 成功制造了新的有效 triage：本轮出现了明确的 `high_dead_branch_ratio`（2 cases），并且 top module/top issue 指向同一条链路（`hypothesis_layer` -> `high_dead_branch_ratio`）。

下一轮定点优化建议优先方向：
- 针对 `hold_for_floor`/`fine_interaction` 主导态下的多分支假设生成，收敛到更少但更高质量的候选（降低死分支、避免无效并行分支扩大）。

## §6 Post-Fix Rebaseline M0.1（M0.5 之后）

Targeted Fix Sprint M0.5 落地后，第二批 10-case 整包已再次重刷：`logs/real_scenario_pack_postfix_m01.json` + `logs/benchmark_triage_board_postfix_m01.json`。

**结论摘要**：`issue_type_distribution` 为 `none×10`；R8/R10 不再携带 `high_dead_branch_ratio`；分诊板无模块/issue 热点。详见 `docs/POST_FIX_REBASELINE_M0_1.md`。

## §7 第三批真实场景启动（M0.2 / M1）

第三批（R11~R16）已启动并完成整包重跑，新的 triage 热点已出现（`blocked_without_resolution` / `recheck_planner`），详见 `docs/REAL_SCENARIO_PACK_M0_2_M1_DELIVERY.md`。

