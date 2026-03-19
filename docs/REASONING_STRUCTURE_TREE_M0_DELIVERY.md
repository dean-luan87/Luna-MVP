# Reasoning Structure Tree M0（推理与决策结构树 M0）交付

## 1. 定位（写死）

Reasoning Structure Tree 是 Luna 的统一推理骨架，用于把线索/候选可能性/分支推理/排除/用户反馈/收敛结果按树状结构组织起来。  
它不替代现有白盒模块；白盒继续保留，结构树是更上层的“总组织结构”。

## 2. 本轮 M0 只做什么

- 树结构骨架
- 基础节点类型
- 现有模块内容最小挂接
- 最小可视化（Reasoning Console 区块）
- 最小指标占位（depth/branch/dead/active_path）

不追求复杂算法与最优树生成；后续允许优化树质量、剪枝策略、压缩长度与精度。

## 3. 代码交付

- 结构树：`decision_monitor/reasoning_structure_tree.py`
- Console 聚合挂接：`tools/reasoning_console_aggregator.py`（快照新增 `reasoning_structure_tree`）
- Console 页面展示：`tools/reasoning_console_server.py`（区块 “推理结构树”）

## 4. 数据结构

- `ReasoningTreeNode`
- `ReasoningStructureTreeResult`

字段与含义以 `decision_monitor/reasoning_structure_tree.py` 为准。

## 5. 节点类型（M0 固定）

- evidence / hypothesis / search_candidate
- grid_decision / recheck_decision / action_hint
- confirmation_input
- exclusion / resolution

## 6. 最小生成规则（M0）

- 根节点：目标/flow/terminal/next_effect 摘要
- 线索节点：evidence_ledger（首条）+ visual_candidate（若有）
- 假设节点：hypothesis_layer（首条）+ 至少一个 pruned alternative
- 动作节点：grid/recheck/action_hint（若有则挂接）
- 反馈节点：confirmation_input_bridge（若有输入则挂接）
- 结果节点：terminal/blocked/unresolved（最小表达）
- 排除节点：至少一个 pruned/exclusion 节点

## 7. 指标占位（M0）

- tree_depth
- branch_count
- dead_branch_count
- active_path_node_ids / pruned_node_ids

## 8. 强约束（写入 CONTRACT）

> 后续任何新功能，只要产生新的推理分支、排除路径、用户反馈驱动路径或结果收敛路径，都应逐步接入 Reasoning Structure Tree；不得长期只存在于模块内部而不进入总结构树。

## 9. 结论（M0）

结构树已完成“架子”与最小挂接，并在 Reasoning Console 中可视化展示；后续可在不破坏接口的前提下逐步优化树质量与剪枝。

## 10. M0.5（树视图整理版：仅展示升级）

M0 已具备结构树数据层，但展示仍偏“文字摘要”。  
M0.5 在 **不改后端树生成逻辑、不改节点模型结构、不改 API** 的前提下，只升级 Reasoning Console 的展示层：

- 按 `parent_node_id` 组织为真正层级树（缩进树/折叠树）
- 默认展开：root + active path + resolved path
- pruned/rejected 分支弱化显示但不隐藏（可折叠）
- 每个节点先显示摘要卡（type/title/summary/status/confidence/source），展开再看细节字段

该版本仍为工程展示版，后续若要提升树质量再在 M1+ 阶段处理剪枝与压缩策略。

## 11. 成长链接入（Experience / Evidence Whitebox Trace M0）

结构树不仅组织交互链（search/recheck/hint/confirmation），也应组织成长链（evidence/hypothesis/experience governance）。  
当存在以下模块输出时，结构树应至少可见：

- evidence 节点：来自 `evidence_ledger`
- hypothesis 节点：来自 `hypothesis_layer`
- governance 节点：来自 `experience_evolution`（以 resolution 节点形式呈现治理 outcome）
- exclusion 节点：至少包含未采用 hypothesis 与未采用治理 outcome
- feedback-driven 标记：若确认输入影响 evidence/hypothesis/experience，则节点 `is_user_feedback_driven=true`

## 12. 指标化接入（Reasoning Tree Metrics M0）

当结构树接入后，必须逐步纳入统一指标体系（tree_depth/branch/dead/feedback/resolution_len 等），用于衡量收敛质量与优化抓手。  
参见：`docs/REASONING_TREE_METRICS_M0_DELIVERY.md`。

