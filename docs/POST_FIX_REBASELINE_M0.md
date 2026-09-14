# Post-Fix Rebaseline M0（优化后真实场景基线重刷）

## §1 目标

在已完成定点优化之后：

- **Targeted Fix Sprint M0.1** — Recheck Planner（见 `docs/TARGETED_FIX_SPRINT_M0_1_RECHECK_BLOCKED.md`）  
- **Targeted Fix Sprint M0.2** — Confirmation Input Bridge（见 `docs/TARGETED_FIX_SPRINT_M0_2_CONFIRMATION_FEEDBACK.md`）  
- **Targeted Fix Sprint M0.3** — Hypothesis Layer（见 `docs/TARGETED_FIX_SPRINT_M0_3_HYPOTHESIS_DEAD_BRANCH.md`）  

对当前 **Real Scenario Pack + Benchmark Triage Board** 做一次**统一重刷**，形成新的真实场景基线（**事实源**），用于回答：

1. 第一批问题是否在**整包**上可感知缓解  
2. 最差场景与 triage 排序是否变化  
3. 下一轮应优先打哪些 module / issue  

**说明**：`logs/` 默认被 `.gitignore` 忽略；本文 **§2–§4 已内嵌** 本次跑出的摘要。若需复现，在仓库根目录执行：

```bash
python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_postfix_m0.json
python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_postfix_m0.json --out logs/benchmark_triage_board_postfix_m0.json
```

---

## §2 Before vs After 总结

### 2.1 整包级「Before」口径（重要）

- **历史整包 JSON（如 `logs/real_scenario_pack_m0.json`）未检入仓库**，无法在 git 中做字节级 diff。  
- **Case 级 Before**：R1 / R5 / R6 的修复前后对照，以 sprint 文档中的定点记录为准（见 §3）。  
- **整包级 After**：以本次生成的 `logs/real_scenario_pack_postfix_m0.json` 为准（摘要如下）。

### 2.2 场景层（After：Post-Fix 整包）

| 指标 | 值 |
|------|-----|
| `total_cases` | 6 |
| `passed_cases` | **6** |
| `worst_real_case_ids` | `R1_container_real`, `R2_occlusion_real`, `R4_feedback_effective_real` |
| `quality_grade_distribution` | `acceptable`: **6**（无 poor / good） |
| `top_priority_optimization_modules`（harness 聚合） | `hypothesis_layer` |

**解读**：整包 6/6 通过 floor/default 规则；质量档全部落在 acceptable。`worst_real_case_ids` 仍按「poor 优先 → dead_branch」启发式排序，**不代表** R1 仍带 tree issue（见 §3）。

### 2.3 Issue 层（After）

| `issue_type_distribution` | 计数 |
|---------------------------|------|
| `none` | 4 |
| `high_dead_branch_ratio` | 2 |

| 指标 | After 观察 |
|------|------------|
| `blocked_without_resolution` | **0 例**（分布中未出现） |
| `feedback_not_effective` | **0 例**（分布中未出现） |
| `high_dead_branch_ratio` | **2 例**（R2、R4，均为 **snapshot_json 载体**，quality_summary 带 `reserve snapshot`） |

**对比 sprint 意图**：M0.3 目标 R1 的 `high_dead_branch_ratio` 已从「定点 before」消除；整包上 **R1 不再贡献** `high_dead_branch_ratio`，与定点结论一致。剩余 2 例主要来自**固定 snapshot**，反映的是载体/快照与当前树的张力，而非 R1/R5/R6 ctx 驱动路径的回退。

### 2.4 Module 层（After：Triage）

来自 `logs/benchmark_triage_board_postfix_m0.json`：

| 排序 | `ranked_modules` |
|------|------------------|
| 1 | `hypothesis_layer`（related_case_count=2，issue_types=`high_dead_branch_ratio`） |

`next_focus_modules`：`["hypothesis_layer"]`  

**Before（叙述）**：M0.3 前 R1 在定点基线上带 `high_dead_branch_ratio` 且 `optimization_hint_module` 可指向假设层；**After** 整包 triage 的模块焦点**收缩**到仍带 dead-branch 信号的 **R2/R4**，模块名仍为 `hypothesis_layer`，但**关联 case 集合已从「含 R1」转为「仅 snapshot 两例」**——即 **triage 的 case 优先级排序已变**（见 §4）。

---

## §3 重点场景变化（R1 / R5 / R6）

### R1 — `R1_container_real`（ctx_json）

| 维度 | Sprint M0.3 记录的 Before（ctx 基线） | **本次 Post-Fix 整包（After）** |
|------|----------------------------------------|----------------------------------|
| `issue_type` | `high_dead_branch_ratio` | **`null`** |
| `dead_branch_count` | 2 | **1** |
| `branch_count` | 3 | **2** |
| `prune_rate` | 0.667 | **0.5** |
| `quality_grade` | acceptable | acceptable |
| `scenario_passed` | true | **true** |

**结论**：R1 上 **M0.3 的缓解在整包重刷中可复核**；树 issue 标签已清，指标仍优于 sprint 文挡中的 before。

### R5 — `R5_feedback_ineffective_real`（ctx_json）

| 维度 | M0.2 文档中的 Before（`_tmp_R5_before`） | **本次 Post-Fix 整包（After）** |
|------|------------------------------------------|----------------------------------|
| `effective_feedback_count` | 1 | **2** |
| `issue_type` | `high_dead_branch_ratio` | **`null`** |
| `quality_grade` | acceptable | acceptable |
| `scenario_passed` | true（default / floor） | **true** |

**结论**：反馈有效性相对 M0.2 文挡 before **已提升**；当前整包上 **不再标注** `high_dead_branch_ratio`，与 M0.3「R5 无回归」叙述一致并可量化对齐。

### R6 — `R6_blocked_or_fallback_real`（ctx_json）

| 维度 | M0.2 回归叙述 | **本次 Post-Fix 整包（After）** |
|------|----------------|----------------------------------|
| `quality_grade` | acceptable | acceptable |
| `issue_type` | （文档：无新问题） | **`null`** |
| `blocked`（metrics） | — | **false**（本 harness 语义下未标 blocked） |
| `scenario_passed` | — | **true** |

**结论**：未观察到「blocked_without_resolution」类 issue 在整包中复活；该 case 在 M0 规则下仍判 **通过**，与 sprint **无回归** 方向一致。

---

## §4 新 Triage 结果（Post-Fix）

**最差场景（分诊排序 top）**：`R2_occlusion_real`、`R4_feedback_effective_real`（并列 priority_score=80，`acceptable` + `high_dead_branch_ratio` + 可行动 hint）  

**当前 top modules**：`hypothesis_layer`  

**当前 top issues**：`high_dead_branch_ratio`（case_count=2，均关联 `hypothesis_layer`）  

**`triage_summary`（原文）**：  
最差场景：R2_occlusion_real, R4_feedback_effective_real；优先模块：hypothesis_layer；突出 issue：high_dead_branch_ratio。

**与修复前的差异（要点）**：

- **R1 不再出现在高分诊 case 前列**（本轮 ranked_cases 中 R1 为 score=20 的「低」档），与 M0.3 消除 R1 的 `high_dead_branch_ratio` **一致**。  
- **分诊注意力上移到仍为 snapshot 的 R2/R4**：后续若继续压 `high_dead_branch_ratio`，需区分「主线回归」与「更新 snapshot / 改 ctx 驱动载体」两条路径。

---

## §5 结论

1. **第一批 fix sprint 是否有效**  
   - **有效（在 R1/R5/R6 上可核对）**：R1 的 dead-branch/issue 缓解、R5 的反馈计数与 issue 标签改善，均能在整包 JSON 中复现。  
   - **整包层面**：`blocked_without_resolution` / `feedback_not_effective` **均未在 issue 分布中出现**；剩余主要矛盾为 **2 例 `high_dead_branch_ratio`（R2/R4 snapshot）**。

2. **下一轮建议优先打什么**  
   - **短期**：针对 **R2/R4** 的 snapshot 与树指标张力，决定是 **更新快照** 还是 **扩展 hypothesis/树组织规则**（仍属 `hypothesis_layer` / 结构树一致性范畴，但应先明确是否要求 snapshot 与 ctx 路径一致）。  
   - **不要**在未刷新载体前，把「仅 snapshot 残留」误判为 R1 回归。

3. **是否进入环境 / 任务链上下文占位层**  
   - **可以进入下一主题**（环境信息 / 任务链信息白盒占位 M0）：当前 **Post-Fix 整包 6/6 通过**，triage 给出稳定的新起点；后续优化应与 **载体刷新** 并行规划，避免 snapshot 与 ctx 路径长期分叉。

---

## §6 验收自检（本轮）

| # | 项 | 状态 |
|---|----|------|
| 1 | 生成 `logs/real_scenario_pack_postfix_m0.json` | ✅（本地；`logs/` 忽略） |
| 2 | 生成 `logs/benchmark_triage_board_postfix_m0.json` | ✅ |
| 3 | 本文档存在 | ✅ |
| 4 | Before/After 可理解（含 R1/R5/R6 + 整包 issue/module） | ✅ |
| 5 | 新 triage 起点明确 | ✅ |
| 6 | 未改 triage 规则、未扩场景、未开发新功能 | ✅ |

**本轮判定**：**通过**（作为 Post-Fix 统一基线重刷与阶段判断文档）。
