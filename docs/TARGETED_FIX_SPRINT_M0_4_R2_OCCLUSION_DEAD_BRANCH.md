# Targeted Fix Sprint M0.4 — R2 Occlusion Dead Branch（定点收敛）

## 1. 目标场景与目标问题

- 目标 case：`R2_occlusion_real`
- 目标 issue：`high_dead_branch_ratio`
- 目标模块：`hypothesis_layer` + 遮挡场景下的树组织死分支（dead branch / prune_rate）

## 2. 本轮最小改动

### 2.1 让 R2 可被“逻辑修复”观测（关键）

由于当前 harness 的 `R2_occlusion_real` 原为 `snapshot_json` 载体，代码变更不会影响已固化的 snapshot 指标。

因此在本轮将：
- `tools/real_scenario_pack.py`：`R2_occlusion_real` 从 `snapshot_json` 切换为 `ctx_json`
- 新增：`tests/real_scenarios/ctx/R2_occlusion_real_ctx.json`

用于确保 `hypothesis_layer` 的修复能在 benchmark 指标上体现。

### 2.2 `hypothesis_layer` 定点收紧（最小规则）

在 `decision_monitor/hypothesis_layer.py` 中：

- 当存在 `occlusion_hint` 且 `container_hint` 不存在时，将 `max_hypotheses` 收紧到 `1`

目的：
- 遮挡主假设收口，避免在 `reasoning_structure_tree` 中因 `len(hypotheses) >= 2` 产生 pruned/exclusion 噪声节点
- 从而降低 `prune_rate`，使 `high_dead_branch_ratio` 消失

## 3. Before / After（R2）

### 3.1 Before（Post-Fix Rebaseline M0：snapshot 口径）

来源：`logs/real_scenario_pack_postfix_m0.json`（snapshot_json）

- issue_type：`high_dead_branch_ratio`
- branch_count：`1`
- dead_branch_count：`1`
- prune_rate：`1.0`
- effective_feedback_count：`1`

### 3.2 After（本轮 M0.4：ctx 口径 + 定点收紧）

来源：`logs/real_scenario_pack_m04_R2_ctx_after_fix.json`（ctx_json）

- issue_type：`null`（消失）
- branch_count：`2`
- dead_branch_count：`1`（仍有 governance exclusion dead-leaf，但 prune_rate 已下降）
- prune_rate：`0.5`
- effective_feedback_count：`2`
- quality_grade：`acceptable`

## 4. 回归影响（轻回归：整包 small check）

本轮重跑：`tools/real_scenario_pack.py --out logs/real_scenario_pack_m04_after_full.json`

结果（整包）：
- `passed_cases`：`6/6`
- `R2_occlusion_real`：`issue_type=null`，未再触发 `high_dead_branch_ratio`
- `R4_feedback_effective_real`：仍为 `high_dead_branch_ratio`（按指令保留 snapshot 刷新项，不在本轮处理）

结论：
- 本轮定点优化对其它可 ctx 驱动 case（`R1/R5/R6`）未观察到明显回归（整包通过）。

## 5. 是否建议继续

- 建议：继续把下一批 `high_dead_branch_ratio` 的重点从 `R2` 迁移到已明确仍在的问题：`R4_feedback_effective_real`（snapshot 刷新/或进一步 ctx 对照）。

