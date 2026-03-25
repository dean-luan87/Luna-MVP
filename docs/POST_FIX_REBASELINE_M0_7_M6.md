# Post-Fix Rebaseline M0.7 / M6（第八批真实场景修复后基线重刷）

## §1 目标

在以下已完成的前提下，对 **整包 Real Scenario Pack（46 case，含第八批 R41–R46）** 与 **Benchmark Triage Board** 做一次统一重刷，固化 **M1.1（第八批新 `*_expected` 标志 recheck 收口）** 之后的最新基线：

- Real Scenario Pack M0.7 / M6（第八批场景接入）
- Targeted Fix Sprint M1.1（`decision_monitor/recheck_planner.py` 中 M1.1 规则）

本回合 **不** 新功能、不扩场景、不改 triage 规则、不改 benchmark 结构。

**复现命令：**

```bash
python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_postfix_m07.json
python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_postfix_m07.json --out logs/benchmark_triage_board_postfix_m07.json
```

**产物：** `logs/real_scenario_pack_postfix_m07.json`、`logs/benchmark_triage_board_postfix_m07.json`

---

## §2 Before vs After 总结

### 对比基准

| 维度 | **Before**（第八批扩包后、M1.1 **前**） | **After**（M1.1 后，本重刷） |
|------|----------------------------------------|------------------------------|
| 产物 | `logs/real_scenario_pack_m07.json` | `logs/real_scenario_pack_postfix_m07.json` |
| `total_cases` | 46 | 46 |
| `passed_cases` | 40 | **46** |
| `quality_grade_distribution` | acceptable=40, **poor=6** | **acceptable=46** |
| `issue_type_distribution` | none=40, **blocked_without_resolution=6** | **none=46** |
| `top_priority_optimization_modules` | `recheck_planner` | **[]**（空） |
| `worst_real_case_ids`（摘要） | 含 **R41–R46**（均为 poor） | **R1, R2, R4**（均为 acceptable，无 poor） |

### 场景层（A）

- **total_cases**：不变（46）。
- **passed_cases**：40 → **46**。
- **quality**：由 **6 个 poor** 变为 **0**；全体 **acceptable**。
- **worst_real_case_ids**：由「第八批全占 poor 队列」变为 **与早期基线类似的 tie-break 顺序**（R1/R2/R4 等，**无 issue、无 poor**）。

### 问题层（B）

- **issue_type_distribution**：`blocked_without_resolution=6` → **0**；**无新 issue 类型**（仍为 `none` 占满）。
- **blocked_without_resolution**：从整包中 **清零**。

### 模块层（C）

- **top_priority_optimization_modules**：由 **`recheck_planner`** → **空**。
- **recheck_planner**：**不再**作为 triage 热点（`ranked_modules=[]`）。
- **triage**：**ranked_modules / ranked_issues 均为空**；`next_focus_issue_types=[]`；**分诊在「问题维度」上清空**（仅剩 acceptable 的 low 优先级排序）。

---

## §3 重点场景变化（R41–R46）

| case_id | Before（m07） | After（postfix_m07） |
|---------|---------------|----------------------|
| R41 | poor，`blocked_without_resolution`，`blocked=true` | **acceptable**，`issue_type=null`，**`blocked=false`**，`scenario_passed=true` |
| R42 | 同上 | 同上 |
| R43 | 同上 | 同上 |
| R44 | 同上 | 同上 |
| R45 | 同上 | 同上 |
| R46 | 同上 | 同上 |

**结论：** M1.1 修复在 **整包基线中一致体现**；R41–R46 已 **退出** `blocked_without_resolution` / poor / worst-issue 队列；**已退出**以 issue 为驱动的「最差 case」分诊（仍可能出现在 `worst_real_case_ids` 的 tie 中，但 **quality 均为 acceptable**）。

---

## §4 新 triage 结果（postfix_m07）

摘自 `logs/benchmark_triage_board_postfix_m07.json`：

- **当前最差场景（ranked 顶部）**：`R1_container_real`、`R2_occlusion_real`、`R3_general_search_real`（均为 **acceptable**，priority **low**，无 issue）。
- **当前 top modules**：**无**（`ranked_modules=[]`）。
- **当前 top issues**：**无**（`ranked_issues=[]`）。
- **triage 是否清空**：**在问题/模块维度已清空**；`triage_summary` 为弱排序下的 **“最差场景”** 文案（无 poor、无 blocked issue）。

---

## §5 结论

1. **M1.1 是否有效**：**是**。`blocked_without_resolution` 从整包清零，R41–R46 全部 **pass** 且 **acceptable**。
2. **下一轮建议优先方向**：
   - **若要以 triage 驱动下一波修复**：需 **扩第九批**或**换更高压场景**，否则当前 **无 issue 热点**。
   - **若 triage 已够用**：可 **转回更高层主线**（非真实场景扩包），或推进已记录的「线程报损/切换/消耗」白盒观察层（**仅规划，不在此轮实现**）。
3. **继续 fix 还是扩场景**：当前 **无 `recheck_planner` 类残留 issue**；**继续 fix 同一类 blocked 无靶子**，除非新场景或新指标再暴露问题。

---

## §6 判定（本轮验收）

| # | 要求 | 结果 |
|---|------|------|
| 1 | R41–R46 修复在整包中体现 | **是** |
| 2 | `blocked_without_resolution` 从第八批场景消失 | **是**（整包 0） |
| 3 | triage 变化 | **是**（热点评级清空） |
| 4 | 下一轮主线 | **扩第九批或转高层主线**（见 §5） |

**本轮：通过。**
