# Reasoning Tree Metrics M0（结构树指标化 / 决策质量度量 M0）交付

## 1. 定位（写死）

指标层不是展示装饰，而是后续推理优化、图书馆沉淀与后台评估的抓手。  
本轮 M0 只做规则版度量：能算、能展示、能比较、能抓明显问题；不做算法优化与学习。

**硬约束**：指标来源必须基于 Reasoning Structure Tree。  
**下游**：Reasoning Tree Quality Overlay M0 消费本指标产出树级/节点级质量标记，见 `docs/REASONING_TREE_QUALITY_OVERLAY_M0_DELIVERY.md`。

## 2. 交付件

- 指标计算：`decision_monitor/reasoning_tree_metrics.py`
- frame 接入：`decision_monitor/schema.py` + `decision_monitor/builder.py`（字段 `reasoning_tree_metrics`）
- Console 展示：`tools/reasoning_console_aggregator.py` + `tools/reasoning_console_server.py`
- 单测：`tests/test_reasoning_tree_metrics.py`
- smoke/JSONL：`tools/smoke_reasoning_tree_metrics.py`

## 3. 指标结构：ReasoningTreeMetricsResult

- tree_depth
- branch_count
- dead_branch_count
- active_path_length
- resolution_path_length
- feedback_node_count
- effective_feedback_count（规则版）
- prune_rate
- resolved / blocked
- possible_tree_issue_type / possible_tree_issue_reason
- metrics_summary / metrics_applied

## 4. 指标计算口径（M0）

- tree_depth：root→最深节点层数
- branch_count：拥有 \(\ge 2\) 子节点的节点数（规则版分叉）
- dead_branch_count：leaf 且状态为 pruned/rejected/blocked 且不在 active_path 的数量
- active_path_length：active_path_node_ids 数量
- resolution_path_length：root→resolved_node_id 的父链长度（无则 0）
- feedback_node_count：`is_user_feedback_driven=true` 的节点数
- effective_feedback_count（规则版）：反馈节点满足以下任一即计有效：
  - next_effect != none
  - status ∈ {resolved, blocked, watchlist}
  - 进入 active path（且非 root）
- prune_rate：dead_branch_count / max(branch_count,1)

## 5. 最小问题归因（M0）

按顺序命中：
- tree_too_deep（depth>5）
- too_many_branches（branch>5）
- high_dead_branch_ratio（prune_rate>0.6）
- feedback_not_effective（feedback>0 且 effective==0）
- long_resolution_path（resolved 且 resolution_path_length>5）
- blocked_without_resolution（blocked 且 not resolved）

## 6. 与图书馆/后续优化的关系

未来图书馆重点吸收的不是单条日志，而是结构树及其质量指标（depth/branch/dead/resolution_len/effective_feedback 等）。  
后续 Luna 优化目标之一，是让树更短、更稳、更快收敛、更少死分支，并可被这些指标量化验证。

## 7. 结论（M0）

结构树指标化已建立并接入 frame + Console + JSONL；当前为规则版度量，后续可在不破坏接口的前提下迭代精度与覆盖面。

## 8. 下一层：Optimization Hint（M0）

指标层用于“发现问题并量化”，下一层 **Optimization Hint** 用于把诊断推进为“先改哪里、为什么、怎么改”的可审计建议。  
参见：`docs/OPTIMIZATION_HINT_M0_DELIVERY.md`。

