# Luna Reasoning Console M0（推理控制台 M0）交付

## 1. 定位（写死）

Reasoning Console 是未来 Luna 的**开箱找问题中心**，也是所有推理/白盒/可视化/错判归因的**统一入口**。

**硬约束（必须遵守）**：

> 后续任何新功能，只要存在判断、排除、推荐、用户反馈影响推进、解释层输出，必须接入 Reasoning Console。不得另起新的独立白盒页/调试页/推理页。

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
- 右侧：总览、用户可见解释层、3x3 网格（简版）、白盒 tabs（Grid/Recheck/ActionHint/Confirmation）、规则版错误归因

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

