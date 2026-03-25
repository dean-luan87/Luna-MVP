# Environment & Task Context Reserve M0（环境信息 / 任务链信息白盒占位层）交付

## 1. 定位（写死）

在 Reasoning Structure Tree、Timeline、全链 Whitebox、Metrics/Quality、Optimization、Knowledge Interface、Continuity、Post-Fix Rebaseline 等已有能力之上，增加**最小前提条件层**：

- **环境**：场景类型、可见性、轻量约束与风险标签（粗映射）
- **任务链**：阶段、当前动作、用户/系统侧效果摘要（非完整 Task Engine）
- **一句话前提**：`context_premise_summary` 串起环境与任务链，便于观察与对比

**不做**：复杂环境建模、任务中心重构、环境评分、历史对比、自动归因引擎。

## 2. 交付件

| 类型 | 路径 |
|------|------|
| 核心模块 | `decision_monitor/environment_task_context_reserve.py` |
| Frame 字段 | `DecisionMonitorFrame.environment_task_context_reserve` |
| Builder 接入 | `decision_monitor/builder.py`（timeline 生成后写回 reserve，并追加 `context_premise_recorded` 时间轴事件） |
| 结构树挂接 | `decision_monitor/reasoning_structure_tree.py`（根 `node_summary` + `tree_summary` 追加 env/stage/premise） |
| 时间轴 | `decision_monitor/reasoning_timeline_view.py`（`append_context_premise_event`） |
| Console 聚合 | `tools/reasoning_console_aggregator.py`（`ReasoningConsoleSnapshot` 扁平摘要字段） |
| Console UI | `tools/reasoning_console_server.py`（「环境 / 任务链前提」区块 + 白盒区前提锚点行） |
| Decision Monitor Viewer | `tools/decision_monitor_viewer.py`（卡片 + 专家折叠字段） |
| RuntimeContext | `runtime/context.py`（摘要字段占位，供主链写回） |
| 单测 | `tests/test_environment_task_context_reserve.py` |
| smoke | `tools/smoke_environment_task_context_reserve.py` |

## 3. 数据结构（M0）

- **`EnvironmentContextReserve`**：`environment_scene_type`、`environment_context_summary`、`environment_constraints[]`、`environment_risk_factors[]`、`environment_visibility_state`、`environment_context_applied`
- **`TaskChainContextReserve`**：`task_chain_id`、`task_chain_stage`、`task_chain_previous_step`、`task_chain_current_action`、`task_chain_user_action_effect`、`task_chain_system_action_effect`、`task_chain_context_summary`、`task_chain_context_applied`
- **`EnvironmentTaskContextReserveResult`**：上述两者 + `context_premise_summary` + `context_premise_applied` + `whitebox_context_premise_line`（与 premise 一致，供白盒区展示）

## 4. 生成规则（摘要）

只读 frame：`object_search_interaction`、`reasoning_tree_metrics`、`spatiotemporal_continuity_reserve`、`confirmation_input_bridge`、`recheck_planner`、`action_hint_copy`、`spatial_expression_sidecar`、`reasoning_timeline_view` 等，按写死粗规则映射场景类型、可见性、约束/风险、任务阶段与用户/系统效果，并拼出中文一句话前提。

## 5. 测试与 smoke

- 单测：`python3 -m pytest tests/test_environment_task_context_reserve.py`
- smoke：`python3 tools/smoke_environment_task_context_reserve.py` → `logs/smoke_environment_task_context_reserve_*.jsonl`

## 6. 结论（M0）

环境/任务链前提已纳入白盒体系占位层；后续可逐步细化环境与任务链事实源，**不得**绕过本层长期只读结果不写前提。
