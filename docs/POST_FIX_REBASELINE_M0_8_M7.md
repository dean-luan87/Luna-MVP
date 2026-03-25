# Post-Fix Rebaseline M0.8 / M7（第九批真实场景修复后基线重刷）

## §1 目标

在以下已完成的前提下，对 **整包 Real Scenario Pack（52 case，含第九批 R47–R52）** 与 **Benchmark Triage Board** 做一次统一重刷，固化 **M1.2（第九批新 `*_expected` 标志 recheck 收口）** 之后的最新基线：

- Real Scenario Pack M0.8 / M7（第九批场景接入）
- Targeted Fix Sprint M1.2（`decision_monitor/recheck_planner.py` 中 M1.2 规则）

本回合 **不** 新功能、不扩场景、不改 triage 规则、不改 benchmark 结构。

**复现命令：**

```bash
python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_postfix_m08.json
python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_postfix_m08.json --out logs/benchmark_triage_board_postfix_m08.json
```

**产物：** `logs/real_scenario_pack_postfix_m08.json`、`logs/benchmark_triage_board_postfix_m08.json`

---

## §2 Before vs After 总结

### 对比基准

| 维度 | **Before**（第九批扩包后、M1.2 **前**） | **After**（M1.2 后，本重刷） |
|------|----------------------------------------|------------------------------|
| 产物 | `logs/real_scenario_pack_m08.json` | `logs/real_scenario_pack_postfix_m08.json` |
| `total_cases` | 52 | 52 |
| `passed_cases` | 46 | **52** |
| `quality_grade_distribution` | acceptable=46, **poor=6** | **acceptable=52** |
| `issue_type_distribution` | none=46, **blocked_without_resolution=6** | **none=52** |
| `top_priority_optimization_modules` | `recheck_planner` | **[]**（空） |
| `worst_real_case_ids`（摘要） | 含 **R47–R52**（均为 poor） | **R1, R2, R4**（均为 acceptable，无 poor） |

### 场景层（A）

- **total_cases**：不变（52）。
- **passed_cases**：46 → **52**。
- **quality**：由 **6 个 poor** 变为 **0**；全体 **acceptable**。
- **worst_real_case_ids**：由「第九批占 poor 队列」变为 **tie-break 占位**（R1/R2/R4，**无 poor**）。

### 问题层（B）

- **issue_type_distribution**：`blocked_without_resolution=6` → **0**；**无新 issue 类型**（`none` 占满）。
- **blocked_without_resolution**：从整包中 **清零**。

### 模块层（C）

- **top_priority_optimization_modules**：由 **`recheck_planner`** → **空**。
- **recheck_planner**：**不再**作为 triage 热点（`ranked_modules=[]`）。
- **triage**：**ranked_modules / ranked_issues 均为空**；`next_focus_issue_types=[]`；**问题维度清空**。

---

## §3 重点场景变化（R47–R52）

| case_id | Before（`m08` 扩包） | After（`postfix_m08`） |
|---------|----------------------|-------------------------|
| R47–R52 | poor，`blocked_without_resolution`，`blocked=true` | **acceptable**，`issue_type=null`，**`blocked=false`**，`scenario_passed=true` |

**结论：** M1.2 在 **整包基线中一致体现**；R47–R52 已 **退出** `blocked_without_resolution` / poor / issue 驱动分诊（`worst_real_case_ids` 中若出现 R1/R2/R4 仅为 **acceptable** 的弱排序，**非**问题 case）。

---

## §4 新 triage 结果（postfix_m08）

摘自 `logs/benchmark_triage_board_postfix_m08.json`：

- **当前最差场景（ranked 顶部）**：`R1_container_real`、`R2_occlusion_real`、`R3_general_search_real`（均为 **acceptable**，**low**，无 issue）。
- **当前 top modules**：**无**（`ranked_modules=[]`）。
- **当前 top issues**：**无**（`ranked_issues=[]`）。
- **triage 是否清空**：**在问题/模块维度已清空**；`triage_summary` 为无 issue 下的弱排序文案。

---

## §5 结论

1. **M1.2 是否有效**：**是**。`blocked_without_resolution` 从整包清零，R47–R52 全部 **pass** 且 **acceptable**。
2. **下一轮建议优先方向**：
   - **若要再以 triage 驱动修复**：需 **扩第十批**真实场景或换压力维度，否则 **无 issue 热点**。
   - **若阶段重心在主线能力**：可 **暂时切回更高层主线**；线程报损/切换/消耗类白盒仍为 **占位**，不在此轮实现。
3. **继续 fix 还是扩场景**：当前 **无 recheck 类残留 issue**；**继续同定点 fix 无靶子**，除非新批场景再暴露。

---

## §6 判定（本轮验收）

| # | 要求 | 结果 |
|---|------|------|
| 1 | R47–R52 修复在整包中体现 | **是** |
| 2 | `blocked_without_resolution` 从第九批场景消失 | **是**（整包 0） |
| 3 | triage 变化 | **是**（热点评级清空） |
| 4 | 下一轮主线 | **扩第十批或转高层主线**（见 §5） |

**本轮：通过。**
