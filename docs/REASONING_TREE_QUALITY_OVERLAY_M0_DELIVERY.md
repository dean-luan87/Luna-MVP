# Reasoning Tree Quality Overlay M0（推理树质量叠加层 M0）交付

## 1. 定位（写死）

- **评分不是独立系统**，而是结构树上的**质量叠加层**：树表达“怎么想的”，质量层表达“想得好不好”。
- 扣分/加分来源回挂到树和分支上；节点级轻量 quality flag 供一眼可读。
- 后续场景评测与优化闭环以这棵**带质量标记的树**为基础。
- 不做：复杂总分系统、历史趋势、图书馆对照、多维权重学习、场景级大盘、自动优化打分器。

## 2. 交付件

- 实现：`decision_monitor/reasoning_tree_quality_overlay.py`
- 接入：`decision_monitor/schema.py`、`decision_monitor/builder.py`（在 metrics 之后生成）
- 聚合与展示：`tools/reasoning_console_aggregator.py`、`tools/reasoning_console_server.py`（与结构树同一区块，不独立评分页）
- 单测：`tests/test_reasoning_tree_quality_overlay.py`
- smoke/JSONL：`tools/smoke_reasoning_tree_quality_overlay.py`

## 3. 数据结构

### 树级：ReasoningTreeQualityOverlayResult

- `structure_score` / `convergence_score`（0–100）
- `quality_grade`：good / acceptable / poor
- `quality_summary`、`score_reason_summary`
- `score_penalty_sources`、`score_bonus_sources`（列表）
- `active_path_quality`、`active_path_cost`
- `node_quality_annotations`：node_id → {quality_flag, quality_note}（方案 A 轻量挂接）
- `quality_overlay_applied`

### 节点级 quality_flag（最小集）

- healthy / costly / weak_support / pruned / feedback_effective / feedback_ineffective / blocked

## 4. 最小评分规则（M0 规则版）

- **structure_score**：基于 tree_depth、branch_count、dead_branch_count、prune_rate、resolution_path_length；树浅、死分支少、收敛路径短则分高。
- **convergence_score**：基于 effective_feedback_count、resolved、blocked、possible_tree_issue_type、optimization_feedback_loop.validation_result；反馈有效、resolved、无阻断则分高。
- **quality_grade**：good（双高且无重大 issue）、acceptable（可收敛或一高一低）、poor（深树/高 dead/blocked 等）。

## 5. runtime_ctx 摘要字段（预留）

在消费 frame 处可写入：`reasoning_structure_score`、`reasoning_convergence_score`、`reasoning_quality_grade`、`reasoning_quality_summary`。

## 6. Console 接入

- 在 **Reasoning Structure Tree** 区块内或紧邻展示：树级 Structure Score、Convergence Score、Quality Grade；Quality Summary；Penalty/Bonus Sources。
- 节点在树视图中显示 quality_flag（来自 node_quality_annotations）。
- 评分与树为一个整体，不拆成两个互不相干的大区块。

## 7. CONTRACT 强约束

> 推理质量评分默认作为 Reasoning Structure Tree 的**质量叠加层**存在，不应长期作为独立、脱离结构树的评分系统平行存在。

## 8. 结论（M0）

质量叠加层已接入 frame / JSONL / Console，与结构树合并展示；当前为规则版，后续场景评测与优化对比默认以此为基础。
