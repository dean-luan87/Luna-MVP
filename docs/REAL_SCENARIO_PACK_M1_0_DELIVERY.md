# Real Scenario Pack M1.0 Delivery（第十批真实场景回归）

**文件**：`docs/REAL_SCENARIO_PACK_M1_0_DELIVERY.md`  
**本轮定位**：`Mainline Engineering Baseline M0.6` 冻结后的首次真实场景回归压测。  
**冻结基线依据**：`docs/MAINLINE_ENGINEERING_BASELINE_FREEZE_M0_6.md`

**硬约束声明**：

- 本轮判断服从 M0.6 冻结口径；  
- 新问题必须归入 `baseline_covered_defect` / `baseline_excluded_requirement` / `reserve_only_finding`；  
- 不允许用单个场景结果直接推翻冻结口径。

---

## §1. 本轮定位

本轮是“冻结基线压测”，不是“边测边改骨架”。  
执行内容仅包括：新增第十批场景、整包重跑、triage 分诊、按冻结口径归类。

---

## §2. 新增 case 清单

本轮新增 `R53`–`R58`（`tests/real_scenarios/ctx`）：

1. `R53_main_task_resumed_but_not_progressed_real`（A 长链任务一致性）  
2. `R54_inserted_task_exit_ambiguous_real`（A 长链任务一致性）  
3. `R55_memory_supported_but_observation_conflicted_real`（C 记忆调用风险）  
4. `R56_dynamic_source_shift_but_mainline_static_real`（B 调度层×主链一致性，兼顾 D 状态/阶段稳定）  
5. `R57_summary_looks_ok_but_requires_backfill_real`（E Summary×后处理边界）  
6. `R58_local_success_masked_global_failure_real`（A 任务一致性，兼顾 D 状态/阶段稳定）

五类方向（A/B/C/D/E）均已触达。

---

## §3. 整包结果摘要

运行命令：

1. `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m10.json`  
2. `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m10.json --out logs/benchmark_triage_board_m10.json`

结果（来自 `logs/real_scenario_pack_m10.json`）：

- 总 case：58  
- passed：54  
- failed：4  
- quality：`acceptable=54`，`poor=4`  
- issue 分布：`none=54`，`blocked_without_resolution=4`

第十批新增 case 结果：

- 失败：`R53`、`R54`、`R55`、`R56`（均为 `blocked_without_resolution`）  
- 通过：`R57`、`R58`

---

## §4. triage 摘要

来自 `logs/benchmark_triage_board_m10.json`：

- worst cases：`R53`、`R54`、`R55`（前 3）  
- top modules：`recheck_planner`  
- top issues：`blocked_without_resolution`  
- triage summary：最差场景集中在 R53/R54；优先模块 `recheck_planner`；突出 issue 为 `blocked_without_resolution`。

---

## §5. 问题分类（按冻结口径）

### A. `baseline_covered_defect`

本轮确认的基线内缺陷（4 条）：

- `R53_main_task_resumed_but_not_progressed_real`  
- `R54_inserted_task_exit_ambiguous_real`  
- `R55_memory_supported_but_observation_conflicted_real`  
- `R56_dynamic_source_shift_but_mainline_static_real`

归类理由：上述问题均落在 M0.6 已纳入能力域（任务位置解释、调度×主链一致性、记忆解释、主链状态/阶段与收口叙事）内，且表现为 `blocked_without_resolution`。

### B. `baseline_excluded_requirement`

本轮**未发现**需要判为 baseline 外需求的主要失败项。  
与图书馆正式接入、记忆写入、污染深实现、治理宪法等相关能力，仍按冻结文档边界维持“非本轮失败判断域”。

### C. `reserve_only_finding`

本轮存在 reserve 暴露信号（非主失败因）：

- `post_processing_intelligence_reserve` 与 `decision_contamination_guard_reserve` 在复杂 case 中可见但未形成强判定/强分类行为。  

归类为 `reserve_only_finding`，不计入本轮基线失败。

---

## §6. 六项验收重点判断

1. **主导源是否讲得清**：整体可讲清；`R56` 暴露“源切换叙事与主链收口不同步”缺陷。  
2. **任务位置是否讲得清**：大部分可解释；`R53/R54` 显示“恢复/退出语义→主任务推进”链路仍有缺口。  
3. **记忆调用是否讲得清**：解释链路存在；`R55` 暴露“supports 与 observation 冲突”时的收敛不足。  
4. **主链状态/阶段是否讲得清**：常规场景可读；复杂冲突场景仍可能落入 `blocked_without_resolution`。  
5. **Summary 与白盒是否同口径**：总体一致，`R57` 证明“summary 可读但需回溯”边界可被守住。  
6. **后处理入口边界是否守住**：`post_processing_summary_entry` 未越权，backfill 语义在 E 类场景可成立。

---

## §7. 当前是否需要开 fix sprint

**已执行并完成 M1.0.x 定点修复**（见 `docs/TARGETED_FIX_SPRINT_M1_0_X.md`）。

post-fix 复跑：

1. `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m10_postfix_m10x.json`  
2. `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m10_postfix_m10x.json --out logs/benchmark_triage_board_m10_postfix_m10x.json`

post-fix 结果：

- `R53/R54/R55/R56` 全部从 `blocked_without_resolution + poor` 变为 `none + acceptable`；  
- 整包变为 `58/58` 通过，`issue_type_distribution=none×58`；  
- triage 中 `recheck_planner` 与 `blocked_without_resolution` 热点清零。

---

## §8. 本轮是否通过

**结论：通过（Baseline Regression Pass + M1.0.x Defect Closure）。**

理由：

- 冻结口径已被实际执行（新增场景压测 + 固定规则分诊 + 三类问题分类）；  
- 发现并闭环了 4 个基线内缺陷（M1.0.x）；  
- post-fix 同口径复测达成 `58/58` 通过；  
- 未出现“以 reserve/边界外需求冒充基线失败”的误判。

因此，M1.0 已形成“冻结基线回归 + 定点缺陷闭环”的完整交付闭环。
