# R4 Snapshot Refresh M0（R4_feedback_effective_real 快照基线刷新）

## §1 问题背景

`R4_feedback_effective_real` 在“更像 snapshot 残留”的归因里被标记为：其 `high_dead_branch_ratio` 更像旧 snapshot 标注噪声，而不是当前主逻辑会持续产生的问题。

直接可见的信号是：旧 snapshot 内部给出了

- `prune_rate = 0.5`
- 但同时 `possible_tree_issue_type = high_dead_branch_ratio`

而主逻辑的 issue 规则（指标化）里 `high_dead_branch_ratio` 触发阈值要求 `prune_rate` 更高（规则版 M0 的条件不应在 `0.5` 时仍标记为该 issue）。

因此本轮目标不是修主逻辑，而是把 R4 的“基线表示方式”刷新到与当前主逻辑指标生成口径对齐。

---

## §2 刷新方式（选 A / B）

选用：**B（改为 ctx 载体）**

原因（写死）：
- snapshot_json 载体在此 case 上出现“issue_type 标注与自身 prune_rate 不自洽”的残留倾向
- 为了让 R4 指标重新由当前主逻辑动态重算，避免继续把错误/过时的 snapshot 基线当作真相来源

本轮做的具体改动：
- `tools/real_scenario_pack.py`：将 `R4_feedback_effective_real` 的 `input_mode` 从 `snapshot_json` 切到 `ctx_json`
- 新增：`tests/real_scenarios/ctx/R4_feedback_effective_real_ctx.json` 作为新的 ctx-like 输入载体

---

## §3 before / after（关键字段对比）

### R4 before（旧 snapshot：`tests/real_scenarios/snapshots/R4_feedback_effective_real.json`）
- `issue_type`：`high_dead_branch_ratio`
- `quality_grade`：`acceptable`
- `branch_count`：`2`
- `dead_branch_count`：`1`
- `prune_rate`：`0.5`
- `effective_feedback_count`：`2`
- `optimization_hint_type`：`reduce_dead_branches`
- `optimization_feedback_loop.validation_result`：`not_enough_data`

### R4 after（刷新后：ctx-like 重算，来自 `logs/real_scenario_pack_after_r4_refresh.json`）
- `issue_type`：`null`（high_dead_branch_ratio 消失）
- `quality_grade`：`acceptable`
- `branch_count`：`2`
- `dead_branch_count`：`1`
- `prune_rate`：`0.5`（保持，但不再触发该 issue）
- `effective_feedback_count`：`2`
- `optimization_hint_type`：`none`

---

## §4 结果（是否从错误 triage 噪声中移除）

刷新后 benchmark / triage 对齐情况（来自 `logs/benchmark_triage_board_after_r4_refresh.json`）：

- `issue_type_distribution`：`none = 6`（`high_dead_branch_ratio = 0`）
- `ranked_cases`：所有 case 的 `issue_type` 均为 `null`
- `ranked_modules` / `ranked_issues`：均为空
- `next_focus`：不再由 `R4` 的 `high_dead_branch_ratio` 驱动

结论：`R4_feedback_effective_real` 已不再作为错误 top triage issue 的噪声来源。

---

## §5 结论（是否可认为基线刷新完成）

可以认为 R4 的 snapshot baseline refresh 已完成：
- snapshot 与主逻辑指标口径对齐
- high_dead_branch_ratio 在 R4 上不再出现
- triage 不再把 R4 作为高优先级 issue（噪声源）驱动

