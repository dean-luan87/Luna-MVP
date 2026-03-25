# Luna Reasoning Console M0（推理控制台 M0）交付

## 1. 定位（写死）

**完整形态上位总纲**：`docs/LUNA_MAINLINE_SHAPE_BLUEPRINT.md`（Console 属于观察与工具入口层，须与主线—白盒—日志同链）。

Reasoning Console 是未来 Luna 的**开箱找问题中心**，也是所有推理/白盒/可视化/错判归因的**统一入口**。

**硬约束（必须遵守）**：

> 后续任何新功能，只要存在判断、排除、推荐、用户反馈影响推进、解释层输出，必须接入 Reasoning Console。不得另起新的独立白盒页/调试页/推理页。

**阶段性总原则（一期收口，写死）**：

> 当前推理主线骨架（交互链 + 白盒链 + 结构链 + 质量链 + 知识预留链 + 策略影子层）在 Console 内形成统一入口。后续新增相关解释/优化/知识/策略内容，优先接入该 Console；不得另起平行页面/体系。

## 2. 本轮 M0 目标

- **统一聚合层**：把一帧中分散模块聚合为 `ReasoningConsoleSnapshot`
- **最小 API**：列表/详情/模块白盒/问题筛选
- **最小单页控制台**：左列表 + 右详情；白盒 tabs；用户可见解释区；3x3 网格；规则版错误归因

## 3. 覆盖模块（M0）

- 核心总览：mainline_integration / task_chain_bridge / task_arbitration / task_bundle（若有）
- Search 与空间：object_search_interaction / spatial_expression_sidecar / local_task_space_grid / grid_search_expansion
- 白盒：grid_search_whitebox_trace / recheck_whitebox_trace / action_hint_whitebox_trace / confirmation_whitebox_trace
- 辅助：recheck_planner / confirmation_input_bridge / action_hint_copy
- 用户可见解释层：聚合展示（不直出内部 weight JSON）
- **环境 / 任务链前提（M0）**：`environment_task_context_reserve` + 扁平摘要字段（`environment_scene_type`、`task_chain_stage`、`context_premise_summary` 等）；详情见 `docs/ENVIRONMENT_TASK_CONTEXT_RESERVE_M0_DELIVERY.md`
- **决策污染观察占位（M0）**：`decision_contamination_guard_reserve` + `contamination_observation_summary` / `contamination_entry_risk_hint` / `contamination_mitigation_reserved`；**Reserved / Future Governance**，无强判定；详情见 `docs/DECISION_CONTAMINATION_GUARD_RESERVE_M0.md`
- **后置信息处理占位（M0）**：`post_processing_intelligence_reserve` + `post_processing_summary` / `post_processing_routing_hint` / `library_link_reserved` / `memory_write_reserved`；**Reserved / Pre-Library Layer**，与记忆系统严格分离、无真实写入；详情见 `docs/POST_PROCESSING_INTELLIGENCE_RESERVE_M0.md`

## 4. 代码交付

- 聚合层：`tools/reasoning_console_aggregator.py`
- API 层：`tools/reasoning_console_api.py`
- 页面 + Server：`tools/reasoning_console_server.py`

## 5. API（M0 最小集）

- `GET /api/reasoning/snapshots?view=all|blocked|issue|with_feedback`
- `GET /api/reasoning/snapshots/{id}`
- `GET /api/reasoning/snapshots/{id}/whitebox/{module}`（module 支持 grid_search / recheck / action_hint / confirmation）
- `GET /api/reasoning/issues?view=issue`

数据源：

- 默认读取 `REASONING_CONSOLE_JSONL_PATH`；若未设置，尝试 `logs/decision_monitor.jsonl`
- 为避免大文件全扫：仅读取 JSONL 末尾窗口（M0）

## 6. UI（M0）

- 左侧：快照列表（goal/flow/terminal/blocked/issue + integration_summary）
- 右侧：总览、**环境/任务链前提（Environment & Task Context）**、用户可见解释层、3x3 网格（简版）、白盒 tabs（Grid/Recheck/ActionHint/Confirmation；白盒区含「前提锚点」一行）、规则版错误归因

## 6.5 UI（M0.5：去日志化整理版）

**只做页面重排与摘要化**，不新增能力、不改后台主逻辑。

- 第一屏改为“四卡问题总览”：当前目标 / 当前主判断 / 当前最可能问题 / 当前状态
- 任务链区按“找问题”顺序：空间与搜索 → 行动建议 → 反馈与推进
- 白盒默认展示**摘要**，并提供“展开完整白盒”（不删内部白盒内容）
- 用户可见解释区改为更接近“对话解释”的问答口径
- 3x3 网格高亮 recommended cell（底色），减少日志感

## 7. 错误归因（M0 规则版）

仅做可审计 tag，不做模型与概率：

- `blocked_recheck`
- `mapping_issue`
- `missing_user_visible_explanation`
- `weak_visual_evidence_but_hint_specific`

输出字段：
- possible_issue_type
- possible_issue_reason
- suggested_debug_module

## 8. 运行方式

```bash
python3 tools/reasoning_console_server.py --jsonl logs/decision_monitor.jsonl --host 127.0.0.1 --port 8777
```

## 9. 结论（M0）

Reasoning Console M0 已具备：**聚合 + API + 页面**三件套，并可作为后续推理/白盒/可视化与错判归因的统一入口基线。

## 10. Reasoning Structure Tree（M0）

Reasoning Console M0 起新增一个区块展示 **Reasoning Structure Tree**（推理与决策结构树）：

- M0 先做规则聚合树（只读挂接），用于把线索/假设/动作/反馈/排除/收敛结果按树状结构组织起来
- 不替代现有白盒模块；结构树是更上层的总骨架
- 页面最小展示：树状列表 + active/pruned 区分 + 指标占位（depth/branch/dead）

### 10.1 UI（M0.5：树视图整理版）

在不改结构树数据来源的前提下，将结构树区域从“线性文本摘要”升级为 **层级树视图**：

- 按 `parent_node_id` 渲染父子层级与同级分支
- active/pruned/resolved/blocked/watchlist 状态有明显视觉区分
- 节点默认摘要卡展示，支持展开细节字段
- 默认展开 root + active/resolved 路径，pruned 分支弱化但可见

### 10.2 成长链白盒接入（M0）

Reasoning Console 新增白盒模块入口（仍默认摘要，可展开）：

- Evidence / Hypothesis Whitebox
- Experience Governance Whitebox

并要求结构树可见 evidence/hypothesis/governance/exclusion/feedback-driven 节点。

### 10.2.5 推理树质量叠加层（M0）

在 **Reasoning Structure Tree** 区块内（与树一体）展示质量叠加：Structure Score、Convergence Score、Quality Grade、Quality Summary、Penalty/Bonus Sources；节点在树视图中显示 quality_flag。不设独立评分页，见 `docs/REASONING_TREE_QUALITY_OVERLAY_M0_DELIVERY.md`。

### 10.3 结构树指标化接入（M0）

Reasoning Console 在结构树区块附近新增 **Tree Metrics** 区块，展示：

- tree_depth / branch_count / dead_branch_count
- active_path_length / resolution_path_length
- feedback_node_count / effective_feedback_count
- prune_rate
- possible_tree_issue_type / possible_tree_issue_reason

### 10.3.5 推理时间轴视图接入（M0）

Reasoning Console 在结构树区块附近新增 **Reasoning Timeline (M0)** 轻量区块，展示事件先后与关键转折：

- key_transition_count / key_transition_summary
- 纵向事件列表（event_type/summary/source/importance）

并明确：时间轴与结构树并列视角，不替代结构树；不做复杂时间系统/动画回放。

### 10.4 优化建议层接入（M0）

Reasoning Console 在 Tree Metrics 附近新增 **Optimization Hint** 区块，展示：

- hint_type / priority
- suggested module / action
- trigger issue
- reason（含“为什么不是别的模块”）

### 10.5 优化建议验证闭环接入（M0）

Reasoning Console 在 Optimization Hint 区块之后新增 **Optimization Feedback Loop** 区块，展示：

- baseline vs current 指标摘要
- delta 核心指标
- validation_result / validation_reason
- suggested_next_step
- worth_persisting_to_library（占位）

### 10.6 Knowledge Dual-Channel Interface 接口预留（M0）

Reasoning Console 新增轻量区块 **Knowledge Interface Reserve**，仅展示三块摘要：

- Persist Candidate（type / worth / reason）
- Optimization Candidate（type / needs_external / lookup_type）
- Injection Slot（target module / stage / mode / payload）

当前仅占坑，不做图书馆写入/检索/注入执行。

### 10.6.5 Strategy Injection Shadow（影子验证，M0）

在不执行真实注入的前提下，新增轻量区块 **Strategy Injection Shadow (M0)**，展示：

- target module / injection mode
- expected tree change / metric change / issue relief（均为“假设/预估”）
- risk level（low/medium/high/unknown）
- next step

并明确：Reserved for future library integration；No real injection executed。

### 10.7 时空间连续性接口预留（M0）

Reasoning Console 新增轻量区块 **Spatiotemporal Continuity (M0)**，默认只展示：

- support level（high/medium/low/broken/unknown）
- influence reason（结果性影响摘要）
- affected module
- preserved/broken

并明确：当前不展开连续性底层细节与调试台。

### 10.7.5 Memory vs Novel Information Channel（M0）

Reasoning Console 新增轻量区块 **Memory vs Novel Information (M0)**，用于显式区分推理所用信息来源通道：

- dominant_reasoning_channel / dominant_decision_channel
- memory/novel/hybrid 通道计数
- novel_memory_candidate（占位：新信息是否正在形成记忆候选）

并明确：当前只做来源通道与候选占位，不做长期记忆系统重构/评分/写库/检索。

## 11. 阶段性收口（Backbone Closure）

本阶段“推理主线骨架”收口文档见：`docs/MAINLINE_REASONING_BACKBONE_CLOSURE_M0.md`。

## 12. 场景评测支架（Benchmark Harness）

统一场景评测支架见：`docs/SCENARIO_BENCHMARK_EVALUATION_HARNESS_M0_DELIVERY.md`。  
后续真实场景验证优先接入该支架，统一产出结构树/质量等级/issue/优化建议/验证结果，避免散落 smoke/临时脚本。

