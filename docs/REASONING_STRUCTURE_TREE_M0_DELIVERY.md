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

### 6.1 Environment & Task Context 轻挂接（M0）

当 frame 含 `environment_task_context_reserve` 时，根 `node_summary` 追加 `env=<scene_type> task_stage=<stage>`；`tree_summary` 末尾可追加截断版 `context_premise_summary`（便于与前提层对齐，不重构树模型）。详见 `docs/ENVIRONMENT_TASK_CONTEXT_RESERVE_M0_DELIVERY.md`。
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

## 9. 与 Quality Overlay 的关系（M0）

推理树质量叠加层（Reasoning Tree Quality Overlay M0）直接叠在结构树上：树级评分（structure/convergence/grade）与节点级 quality_flag 均以本树为基础；评分与树一体展示，见 `docs/REASONING_TREE_QUALITY_OVERLAY_M0_DELIVERY.md`。

## 9.5 与 Timeline 的关系（M0）

推理时间轴视图（Reasoning Timeline View M0）与结构树为并列视角：

- 结构树：分支/排除/收敛关系
- 时间轴：事件先后/关键转折/状态切换

时间轴只读主线输出并在 Console 中靠近结构树展示，见 `docs/REASONING_TIMELINE_VIEW_M0_DELIVERY.md`。

## 10. 结论（M0）

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

## 13. 时空间连续性接口预留（M0）

连续性属于内部强影响因子，应进入结构树依据层。M0 仅做轻挂接：在结构树摘要中附一句 continuity 影响摘要；不改变树模型结构、不引入复杂连续性细节。  
参见：`docs/SPATIOTEMPORAL_CONTINUITY_RESERVE_M0_DELIVERY.md`。

## 14. Memory vs Novel Information Channel（M0）

推理过程应显式区分“记忆信息调用”与“新增信息获取”两条信息通道。M0 仅做轻挂接：

- root 摘要附加 dominant_reasoning_channel / dominant_decision_channel 简短标记
- 不改变树模型主结构，不引入复杂记忆系统细节

参见：`docs/MEMORY_NOVEL_INFORMATION_CHANNEL_M0_DELIVERY.md`。

