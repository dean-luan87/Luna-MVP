# Scenario Benchmark & Evaluation Harness M0（场景基准包 + 评测支架 M0）交付

## 1. 定位（写死）

这是一套**统一场景评测支架**，不是“很多临时测试脚本”。后续真实场景验证应优先接入该支架，统一跑出可比较结果。

每个场景至少统一产出：

- Reasoning Structure Tree
- Reasoning Tree Metrics
- Reasoning Tree Quality Overlay（质量等级）
- issue（来自 metrics 的 possible_tree_issue_type）
- Optimization Hint
- Optimization Feedback Loop（如适用）

M0 不做：大规模 benchmark 平台、长周期统计、图书馆写回、多版本实验平台、自动回归/报表系统。

## 2. 交付件

- Harness：`tools/scenario_benchmark_harness.py`
  - `ScenarioBenchmarkCase` / `ScenarioBenchmarkResult`
  - 单 case / case 组运行
  - summary 输出（分布 + top problem cases + top optimization modules）
- 单测：`tests/test_scenario_benchmark_harness.py`
- smoke：`tools/smoke_scenario_benchmark_harness.py`（写 `logs/smoke_scenario_benchmark_harness_*.json`）

## 3. 最小场景集合（M0，写死少量）

当前内置 6 类标准场景：

- container_search
- occlusion_search
- general_search
- feedback_effective
- feedback_ineffective
- blocked_or_fallback

目标不是“场景多”，而是“类型清楚 + 输出统一 + 可比较 + 可扩展”。

## 4. 评测结果结构（统一）

`ScenarioBenchmarkResult` 包含：

- metrics 摘要：tree_depth / branch_count / dead_branch_count / resolution_path_length / effective_feedback_count / prune_rate（可选 active_path_length / blocked / resolved）
- quality：quality_grade / quality_summary
- issue：issue_type / issue_reason
- optimization：optimization_hint_type / optimization_hint_module / optimization_validation_result
- pass：scenario_passed / scenario_summary

## 5. 判定规则（M0 简单）

- 若 `expected_quality_floor` 存在：grade 不低于 floor → pass
- 否则若 `expected_issue_type` 存在：issue 命中 → pass
- 否则默认：quality != poor 且非 blocked_unresolved → pass

## 6. 与主线的关系（写死）

Harness **只消费主线输出**（frame 内字段），不另造平行逻辑：

- reasoning_structure_tree / reasoning_tree_metrics / reasoning_tree_quality_overlay
- optimization_hint / optimization_feedback_loop

## 7. 结论（M0）

场景评测支架已建立：可用统一方式跑少量标准场景，并输出可比较的“树 + 质量 + issue + 优化建议/验证”结果，为后续真实场景验证标准化打底。

## 8. Real Scenario Pack（真实场景包，M0）

真实场景第一版基线包见：`docs/REAL_SCENARIO_PACK_M0_DELIVERY.md`。  
原则：真实场景接入只扩输入层（image/trace/snapshot 载体），评测结果结构与判定规则不变。

补充：后续基于同一 harness 继续扩充第二批真实场景（M0.1）见 `docs/REAL_SCENARIO_PACK_M0_1_DELIVERY.md`，本轮整包可重新触发有效 triage。

继续补充：第三批真实场景扩充（M0.2 / M1）见 `docs/REAL_SCENARIO_PACK_M0_2_M1_DELIVERY.md`；仍沿用同一 `ScenarioBenchmarkCase/ScenarioBenchmarkResult` 与 triage 口径。

继续扩充：第四批真实场景扩充（M0.3 / M2）见 `docs/REAL_SCENARIO_PACK_M0_3_M2_DELIVERY.md`；本轮 triage 重新聚焦 `blocked_without_resolution/recheck_planner`。

继续扩充：第五批真实场景扩充（M0.4 / M3）见 `docs/REAL_SCENARIO_PACK_M0_4_M3_DELIVERY.md`；本轮再次制造 blocked 类有效 triage。

继续扩充：第六批真实场景扩充（M0.5 / M4）见 `docs/REAL_SCENARIO_PACK_M0_5_M4_DELIVERY.md`；本轮再次制造 blocked_without_resolution 可见 triage。
继续扩充：第七批真实场景扩充（M0.6 / M5）见 `docs/REAL_SCENARIO_PACK_M0_6_M5_DELIVERY.md`；本轮再次触发 recheck_planner 侧 blocked 语境问题可见性。
继续扩充：第八批真实场景扩充（M0.7 / M6）见 `docs/REAL_SCENARIO_PACK_M0_7_M6_DELIVERY.md`；引入 R41–R46 更高阶语义压力并重新生成整包 triage。
继续扩充：第九批真实场景扩充（M0.8 / M7）见 `docs/REAL_SCENARIO_PACK_M0_8_M7_DELIVERY.md`；引入 R47–R52 慢性错位与伪一致性类压力。

## 9. Benchmark Triage Board（分诊板，M0）

评测结果到研发优先级的转换见：`docs/BENCHMARK_TRIAGE_BOARD_M0_DELIVERY.md`。

