# Targeted Fix Sprint M0.3（Hypothesis Layer：压 high_dead_branch_ratio 定点优化）

## 1. 目标（写死）

- **目标场景**：`R1_container_real`
- **目标问题**：`high_dead_branch_ratio`（hypothesis 分支发散 / 低价值备选过多 / dead branch 偏高）
- **本轮边界**：最小、可验证、可回归；不做学习型分支选择器、不改指标公式、不扩 triage/benchmark。

## 2. 关键前置：让 R1 可被“代码变更”驱动

原 `R1_container_real` 为 `snapshot_json` 载体，无法反映 `hypothesis_layer` 的新规则（复用旧 frame）。  
本轮将 R1 切换为 `ctx_json` 驱动 builder（只改输入层，不改评测逻辑），并新增：

- `tests/real_scenarios/ctx/R1_container_real_ctx.json`
- `tools/real_scenario_pack.py`：R1 input_mode 改为 `ctx_json`

## 3. 本轮改动（最小规则）

### 3.1 `hypothesis_layer`：强 container 提示时压低并行弱分支

当 builder 注入 `object_search_hint` 且出现显式 `容器候选：...` 时：

- **默认仅保留 1 条主假设**（container_candidate）
- 仅在 `fine_interaction` 且确有近场交互信号时，允许额外保留 1 条 `interaction_target_candidate` 作为“唯一次要分支”
- 同时抑制在 container 场景下的 `path_continuation_candidate` / `occluded_object_candidate` 弱并行分支进入

目的：减少低价值备选进入结构树，从源头降低 dead branch / prune_rate。

### 3.2 `reasoning_structure_tree`：不再强行合成 pruned alternative（当假设层已单一收敛）

结构树原逻辑会无条件合成一个 pruned alternative hypothesis，用于“至少有一个 exclusion 节点”。  
本轮改为：

- **仅当 `hypothesis_layer.hypotheses >= 2`** 时才生成 pruned alternative 与其 exclusion 节点
- 当假设层已强约束到单一主假设时，避免引入低价值 pruned 分支污染指标

（注意：这是“结构树展示/组织层”对 hypothesis_layer 的一致性跟随，不改变指标公式与主逻辑。）

## 4. Before / After（R1）

### Before（ctx_json 驱动基线）

来自：`logs/_tmp_R1_after_m03_ctx.json`

- issue_type：`high_dead_branch_ratio`
- prune_rate：0.667
- branch_count：3
- dead_branch_count：2
- quality_grade：acceptable

### After（本轮规则生效）

来自：`logs/_tmp_R1_after_m03_final.json`

- issue_type：**None（消失）**
- prune_rate：**0.50（下降）**
- branch_count：**2（下降）**
- dead_branch_count：**1（下降）**
- quality_grade：acceptable（保持）
- optimization_hint_type：none（因 issue 消失）

## 5. 回归影响（R5 / R6）

回归输出：

- `logs/_tmp_R5_regress_m03.json`
- `logs/_tmp_R6_regress_m03.json`

结论：均未出现新的 tree issue（issue_type 为空），质量等级保持 acceptable，属于无回归。

## 6. 结论

**Targeted Fix Sprint M0.3：通过。**

- R1 的 `high_dead_branch_ratio` 已缓解/消失（prune_rate、branch_count、dead_branch_count 均改善）
- 改动保持最小、可审计、可回归
- 未引入对 R5/R6 的明显回归

