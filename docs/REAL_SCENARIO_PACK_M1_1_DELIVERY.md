# Real Scenario Pack M1.1 Delivery（第十一批真实场景扩包）

**文件**：`docs/REAL_SCENARIO_PACK_M1_1_DELIVERY.md`  
**本轮定位**：`M0.6` 冻结基线通过首轮验证（M1.0 + M1.0.x）后的下一批扩包压测。  
**冻结基线依据**：`docs/MAINLINE_ENGINEERING_BASELINE_FREEZE_M0_6.md`

**硬约束声明**：

- 本轮判断继续服从 M0.6 冻结口径；  
- 新问题继续分类为 `baseline_covered_defect` / `baseline_excluded_requirement` / `reserve_only_finding`；  
- 不允许因单一新场景重解释 M0.6 边界。

---

## §1. 本轮定位

本轮目标不是再证明基线存在，而是在冻结基线稳定前提下继续扩包，主动压测：

1. 长链任务连续性升级  
2. 源调度切换升级  
3. 个性化语义偏差边界  
4. Summary × backfill 边界强化  
5. 主链 state/phase 显式化压力

---

## §2. 新增 case 清单

新增 `R59`–`R64`，全部为 `ctx_json` 场景：

1. `R59_multi_inserted_recovery_but_main_not_progressed_real`（A）  
2. `R60_recovery_declared_but_resume_chain_fragile_real`（A/E）  
3. `R61_memory_bias_accumulated_under_familiar_context_real`（C）  
4. `R62_source_shift_twice_but_mainline_lagged_real`（B）  
5. `R63_summary_readable_ok_but_backfill_mandatory_real`（D）  
6. `R64_phase_correct_but_closure_semantics_misaligned_real`（E）

五类方向（A/B/C/D/E）均已覆盖。

---

## §3. 整包结果摘要

运行命令：

1. `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m11.json`  
2. `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m11.json --out logs/benchmark_triage_board_m11.json`

结果（`logs/real_scenario_pack_m11.json`）：

- 总 case：64  
- passed：61  
- failed：3  
- quality：`acceptable=61`，`poor=3`  
- issue 分布：`none=61`，`blocked_without_resolution=3`

第十一批新增 case 结果：

- 通过：`R59`、`R62`、`R63`  
- 失败：`R60`、`R61`、`R64`（均为 `blocked_without_resolution`）

---

## §4. triage 摘要

来自 `logs/benchmark_triage_board_m11.json`：

- top modules：`recheck_planner`  
- top issues：`blocked_without_resolution`  
- 本轮最差 case（按 pack 摘要）：`R60`、`R61`、`R64`

结论：M1.1 新压力主要把问题重新集中到 `recheck_planner` 的 blocked 收口路径。

---

## §5. 问题分类（按冻结口径）

### A. `baseline_covered_defect`

本轮新暴露基线内缺陷：

- `R60_recovery_declared_but_resume_chain_fragile_real`  
- `R61_memory_bias_accumulated_under_familiar_context_real`  
- `R64_phase_correct_but_closure_semantics_misaligned_real`

归类理由：三者均落在 M0.6 已冻结能力域（recheck 收口、记忆解释与风险语义、mainline state/phase 与 closure 对齐）内，表现为 `blocked_without_resolution`。

### B. `baseline_excluded_requirement`

本轮未出现可判定为“基线外正式失败”的主问题。  
图书馆正式接入、记忆写入、污染治理深实现等仍属冻结外能力。

### C. `reserve_only_finding`

本轮存在 reserve 可见信号，但未构成主失败因（如 post-processing reserve/污染 guard reserve 仍为观察层）。  
统一记为 future gap，不计入本轮失败。

---

## §6. 六项验收重点判断

1. **主导源是否讲得清**：`R62` 通过，说明二次切换语境下仍可维持可接受解释。  
2. **任务位置是否讲得清**：`R59` 通过，但 `R60` 暴露“恢复声明→主任务恢复链脆弱”缺口。  
3. **记忆调用/个性化语义偏差是否讲得清**：`R61` 暴露偏差累积语境下收敛不足。  
4. **主链状态/阶段是否讲得清**：`R64` 显示 phase 可读但 closure 语义可能错位。  
5. **Summary 与白盒是否同口径**：`R63` 通过，说明 summary-backfill 边界在该压力下仍可守住。  
6. **后处理入口边界是否守住**：未出现 entry 越权替代证据本体的信号，边界总体守住。

---

## §7. 当前是否需要开 fix sprint

**需要**，建议开启小型 `M1.1.x` 定点修复，目标仅限：

- 收敛 `R60/R61/R64` 的 `blocked_without_resolution`；  
- 优先修复 `recheck_planner` 在恢复链脆弱、记忆偏差累积、phase-closure 错位语境下的收口策略；  
- 不改 benchmark/triage 规则，不扩系统边界。

---

## §8. 本轮是否通过

**结论：有条件通过（Expansion Pass with New Defect Findings）。**

理由：

- M1.1 扩包目标已完成（新增 6 case，覆盖 5 类方向）；  
- 压出 3 个新的基线内缺陷，且集中明确；  
- 分类边界保持稳定，未出现将 reserve/边界外需求误算为正式失败。

因此 M1.1 可作为“冻结基线后的有效扩压轮次”，并进入 M1.1.x 定点修复阶段。
