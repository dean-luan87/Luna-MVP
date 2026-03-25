# R2 / R4 Snapshot vs Logic Disambiguation M0（R2 / R4 残留问题归因判断）

## §1 目标（只做归因，不做修复）

针对当前 Post-Fix Rebaseline M0 后仍残留的：

- `R2_occlusion_real`
- `R4_feedback_effective_real`

共同 issue：`high_dead_branch_ratio`

本轮只回答：更像 `snapshot` 残留/表达偏差，还是更像 `主逻辑`（`hypothesis_layer` / `reasoning_structure_tree` 组织）仍未收干净。

最终输出：
- 每个 case 的 `likely_problem_source`：`snapshot` / `logic` / `undetermined`
- 下一步推荐：是否优先刷 snapshot，还是继续开 M0.4

---

## §2 归因方法（M0 简化对照）

对每个 case 做两种口径：

1. Snapshot 口径：直接读取 `tests/real_scenarios/snapshots/*.json` 内嵌的 `reasoning_tree_metrics / reasoning_tree_quality_overlay / optimization_hint`。
2. Ctx-like 口径：用现有 `DecisionMonitorBuilder` 手工构造最小输入（不引入新功能），跑出真实 `reasoning_tree_metrics` 与 `optimization_hint`。

判断规则（写死/简化）：

- 若 Snapshot 的 `possible_tree_issue_type=high_dead_branch_ratio` 与其自身 `prune_rate`/树指标不一致，则更像 `snapshot` 表达/基线残留。
- 若 Snapshot 与 Ctx-like 同向一致（例如两边都触发 `prune_rate > 0.6`），则更像 `logic` 仍在产生 dead 分支。

---

## §3 R2 对照结果（Snapshot vs Ctx-like）

### 3.1 Snapshot（`tests/real_scenarios/snapshots/R2_occlusion_real.json`）

- `possible_tree_issue_type`：`high_dead_branch_ratio`
- `branch_count`：1
- `dead_branch_count`：1
- `prune_rate`：1.0
- `effective_feedback_count`：1
- `optimization_hint`：`reduce_dead_branches`
- `suggested_optimization_module`：`hypothesis_layer`
- snapshot 内嵌原因：`possible_tree_issue_reason=reserve snapshot`

### 3.2 Ctx-like（最小 occlusion-like 输入构造）

本次构造点：
- `visual_audit_objects_main`：cup 与 bottle bbox 显著重叠且 bottle bbox center 不在 cup bbox 内（避免 container 命中，尽量触发 occlusion）。
- `confirmation_input_type`：`occlusion_cleared`

跑出结果（来自 `DecisionMonitorBuilder().build(ctx).to_dict()`）：

- `possible_tree_issue_type`：`high_dead_branch_ratio`
- `branch_count`：3
- `dead_branch_count`：2
- `prune_rate`：0.667
- `effective_feedback_count`：2
- `optimization_hint`：`reduce_dead_branches`
- `suggested_optimization_module`：`hypothesis_layer`

### 3.3 R2 归因结论

- Snapshot 与 Ctx-like **同向**出现 `high_dead_branch_ratio`
- 且两边都符合（`prune_rate > 0.6`）触发逻辑

结论：`R2_occlusion_real` **更像 logic 问题**（至少在当前 ctx-like 口径下，主逻辑会继续产生 dead 分支比率）。

---

## §4 R4 对照结果（Snapshot vs Ctx-like）

### 4.1 Snapshot（`tests/real_scenarios/snapshots/R4_feedback_effective_real.json`）

- `possible_tree_issue_type`：`high_dead_branch_ratio`
- `branch_count`：2
- `dead_branch_count`：1
- `prune_rate`：0.5
- `effective_feedback_count`：2
- `optimization_hint`：`reduce_dead_branches`
- `suggested_optimization_module`：`hypothesis_layer`
- snapshot 内嵌原因：`possible_tree_issue_reason=reserve snapshot`

关键矛盾：
- `high_dead_branch_ratio` 在主逻辑指标规则中要求 `prune_rate > 0.6`
- 但 Snapshot 同时给出 `prune_rate=0.5`

### 4.2 Ctx-like（最小 feedback-effective 输入构造）

本次构造点：
- 仅 bottle 可见（避免引入额外容器/遮挡噪声）
- `confirmation_input_type=target_found`
- `search_subtask_state=waiting_user`

跑出结果：

- `possible_tree_issue_type`：`null`
- `branch_count`：2
- `dead_branch_count`：1
- `prune_rate`：0.5
- `effective_feedback_count`：2
- `optimization_hint`：`none`

### 4.3 R4 归因结论

- Snapshot 与 Ctx-like **不一致**：
  - Snapshot：标记 `high_dead_branch_ratio`，但自身 `prune_rate=0.5` 不满足触发条件
  - Ctx-like：`prune_rate=0.5` 且 issue 为 `null`，与主逻辑规则一致

结论：`R4_feedback_effective_real` **更像 snapshot 问题**（snapshot 表达/基线指标残留/标注不自洽）。

---

## §5 归因汇总（针对共同 issue：high_dead_branch_ratio）

- `R2_occlusion_real`：更像 `logic`
- `R4_feedback_effective_real`：更像 `snapshot`
- 因两 case 归因不一致，本轮总体判断：`undetermined`（但 R4 有强 snapshot 证据链）

---

## §6 下一步建议（必须二选一或三选一中的明确项）

推荐下一步：`collect_more_ctx_cases`

原因（简短）：
1. R4 snapshot 明显不自洽，下一轮应优先刷新/修正 R4 的 snapshot 表达（但这属于“snapshot-baseline step”，需要更多证据后才能决定是否进入 M0.4）。
2. R2 在 ctx-like 口径下仍可触发 `high_dead_branch_ratio`，如果修正 snapshot 后 R2 仍然残留，则更值得开 M0.4。

本轮建议先收集更多 ctx-like 或新增更贴近当前语义的输入，让我们能把“R2 的逻辑死分支”与“R4 的 snapshot 标注偏差”完全切开。

---

## §7 本轮是否通过

- 已对 R2 / R4 做了最小 snapshot vs ctx-like 对照
- 输出每个 case 的 `likely_problem_source`
- 给出明确 `recommended_next_step`
- 未引入新功能 / 未开新 fix sprint / 未扩真实场景包

本轮判定：**通过（归因判断可支持下一步决策）**。

