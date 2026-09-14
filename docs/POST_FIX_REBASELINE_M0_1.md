# Post-Fix Rebaseline M0.1（第二批真实场景修复后基线重刷）

## §1 目标

在 **Real Scenario Pack M0.1（R7~R10）** 与 **Targeted Fix Sprint M0.5（R8/R10 `high_dead_branch_ratio` 定点收敛）** 完成之后，对同一套 **10-case 真实场景整包** 做一次统一重刷，产物作为「第二批修复后」权威基线。

- 整包：`python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_postfix_m01.json`
- 分诊：`python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_postfix_m01.json --out logs/benchmark_triage_board_postfix_m01.json`

**Before 对照**：修复前第二批 triage 仍含 R8/R10 的 `high_dead_branch_ratio`，以仓库内历史产物 `logs/real_scenario_pack_m01.json`（M0.1 扩充后、M0.5 前）的 `summary` 为准。

---

## §2 Before vs After 总结

### 场景层

| 项 | Before（`real_scenario_pack_m01.json`） | After（`real_scenario_pack_postfix_m01.json`） |
|----|----------------------------------------|------------------------------------------------|
| total_cases | 10 | 10 |
| passed_cases | 10 | 10 |
| quality_grade_distribution | acceptable×10 | acceptable×10 |
| worst_real_case_ids | R8, R10, R1 | **R1, R2, R4**（R8/R10 已退出 worst top3） |

### Issue 层

| 项 | Before | After |
|----|--------|-------|
| issue_type_distribution | none×8，**high_dead_branch_ratio×2** | **none×10** |
| high_dead_branch_ratio | 2 | **0** |
| 新 issue 类型 | — | **无**（仍为全 null） |

### Module 层

| 项 | Before | After |
|----|--------|-------|
| top_priority_optimization_modules | `["hypothesis_layer"]` | **`[]`** |
| triage 热点模块 | hypothesis_layer | **无（分诊板模块榜为空）** |

---

## §3 重点场景变化（R8 / R10）

| 指标 | Before（`real_scenario_pack_m01.json` 单条） | After（`real_scenario_pack_postfix_m01.json`） |
|------|---------------------------------------------|------------------------------------------------|
| **R8** issue_type | `high_dead_branch_ratio` | `null` |
| **R8** prune_rate / branch / dead | 0.667 / 3 / 2 | **0.5 / 2 / 1** |
| **R8** optimization_hint | reduce_dead_branches / hypothesis_layer | **none** |
| **R10** issue_type | `high_dead_branch_ratio` | `null` |
| **R10** prune_rate / branch / dead | 0.667 / 3 / 2 | **0.5 / 2 / 1** |
| **R10** optimization_hint | reduce_dead_branches / hypothesis_layer | **none** |

结论：**M0.5 在整包基线中完全体现** — R8/R10 已退出「问题 case」与 worst top3，指标与第一批多数 case 对齐（`prune_rate=0.5` 等）。

---

## §4 新 triage 结果（`benchmark_triage_board_postfix_m01.json`）

- **当前最差场景（排序靠前，并列低分）**：`R1_container_real`, `R2_occlusion_real`（摘要口径与 `next_focus_case_ids` 前三一致）
- **当前 top modules**：**无**（`ranked_modules`: `[]`）
- **当前 top issues**：**无**（`ranked_issues`: `[]`）
- **triage 是否清空**：**是** — 无非空 `issue_type` / 无可聚合热点模块与 issue；仅余 `quality=acceptable` 下的均匀低优先级排序

`triage_summary`：`最差场景：R1_container_real, R2_occlusion_real；优先模块：—；突出 issue：—。`

---

## §5 结论

1. **M0.5 有效**：整包 `high_dead_branch_ratio` 从 2 降为 **0**；R8/R10 在整包与分诊中均不再作为问题源。
2. **第二批真实场景 triage**：当前 **已再次「清空」**（无 issue 热点、无优化模块热点），与第一批收口后的形态一致。
3. **下一轮建议**
   - **主线策略**：若需继续推进决策压力，优先考虑 **扩第三批真实场景**（新压力源），而不是继续在 R1~R10 上叠加以 issue 为空的 fix。
   - **若暂不扩包**：可转入更高层主线或其它非 benchmark 驱动任务；当前分诊板不再给出「必须打 hypothesis_layer」类信号。

---

## 复现命令（摘要）

```bash
python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_postfix_m01.json
python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_postfix_m01.json --out logs/benchmark_triage_board_postfix_m01.json
```

定点 sprint 记录：`docs/TARGETED_FIX_SPRINT_M0_5_HYPOTHESIS_FLOOR_FINE.md`。
