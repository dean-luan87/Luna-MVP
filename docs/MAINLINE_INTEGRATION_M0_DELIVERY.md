# 主线接入 M0 交付说明（Cognitive Runtime Mainline Integration M0）

## 目标

将主线 2 第二阶段已完成的「局部认知运行内核」以**受控方式**接入主流程，原则为：

- **摘要先行**：主流程先读取并记录各模块摘要
- **软控制优先**：仅允许轻量动作从认知内核进入主流程
- **硬边界保留**：守底/阻断逻辑不改，不反写策略
- **不重构主流程**：不正式改 Task Chain 主体、不改 detector/OCR/Dynamic Policy 根逻辑

## 接入范围（本轮）

| 模块 | 接入方式 |
|------|----------|
| task_chain_bridge | 摘要消费，运行摘要与调度参考 |
| task_arbitration | 摘要消费，运行摘要与调度参考 |
| task_bundle | 摘要消费，运行摘要与调度参考 |
| object_search_interaction | 摘要 + interaction_prompt/object_search_action 进入 integration_soft_actions |
| recheck_planner | 未阻断时 recheck_* / look_forward / shift_view_* 走已有 local_goal_recheck_* / view_behavior_hint；阻断记入 integration_blocked_actions |
| experience_evolution | 只读摘要，进入 integration_observation_notes / integration_summary；**不反写策略** |

## 未接入

- hypothesis_layer 的直接策略控制
- object_temporal_ledger 对主流程的硬控制
- experience_evolution 对主策略的反写
- detector/OCR/动态策略根逻辑重构
- 完整 Task Chain 主体改造

## 数据结构：MainlineIntegrationResult

| 字段 | 说明 |
|------|------|
| integration_enabled | 是否启用主线接入 |
| integration_summary | 标准化一句摘要（fg=…; tc_state=…; arb=…; bundle=…; search=…; recheck=…; exp=…） |
| integration_consumed_modules | 当前主流程已消费的模块列表（task_chain_bridge, task_arbitration, task_bundle, object_search_interaction, recheck_planner, experience_evolution） |
| integration_soft_actions | 本轮被主流程采纳的轻量动作（如 recheck_environment, object_search_prompt_ready, arbitration_summary_ready） |
| integration_blocked_actions | 存在但未被采纳/被守底阻断的动作（如 blocked_recheck_environment, blocked_task_resume） |
| integration_observation_notes | 观察备注（含经验摘要等只读信息） |
| integration_applied | 本帧接入结果是否已应用 |

## 主流程消费摘要（只读优先）

主流程通过 `frame.mainline_integration` 及 `runtime_ctx.mainline_integration_*` 读取并记录：

- **任务链摘要**：task_chain_state, task_chain_substate, task_chain_foreground_summary, task_chain_can_resume, task_chain_bundle_state
- **任务编排摘要**：task_arbitration_action, task_arbitration_reason, current_foreground_task_type, current_task_bundle_* 
- **寻物摘要**：object_search_state, object_search_action, object_search_prompt, object_search_zone, object_search_flow_type, object_search_next_step, search_terminal_status
- **补证摘要**：recheck_action, recheck_reason, recheck_target, recheck_blocked
- **经验摘要（只读）**：experience_evolution_type, experience_evolution_status, experience_evolution_reason, experience_evolution_hint, experience_evolution_confidence_band/scope

## 软控制接入规则

- **recheck_planner**：未阻断时 recheck_environment / recheck_close_range 走 local_goal_recheck_*；look_forward / shift_view_* 走 view_behavior_hint；阻断则记入 integration_blocked_actions。
- **object_search_interaction**：interaction_prompt 进入摘要/日志/对话入口；object_search_action 进入 integration_soft_actions；不直接改写主任务执行器。
- **task_arbitration / task_bundle / task_chain_bridge**：仅作运行摘要与调度参考，不直接改 Task Chain 主逻辑。
- **experience_evolution**：仅进入 integration_observation_notes / integration_summary，不反写策略。

## runtime_ctx 最小接入字段

- mainline_integration_summary
- mainline_integration_modules（逗号分隔）
- mainline_integration_soft_actions（逗号分隔）
- mainline_integration_blocked_actions（逗号分隔）
- mainline_integration_applied

## Viewer

- Frame 中新增 `mainline_integration` 字段。
- 新增卡片「主线接入 / Mainline Integration (M0)」，展示：integration_enabled, integration_summary, integration_consumed_modules, integration_soft_actions, integration_blocked_actions, integration_observation_notes, integration_applied。

## 验收标准（本轮）

1. 主流程能读取并汇总 6 模块摘要。
2. 存在明确的 MainlineIntegrationResult 及 frame.mainline_integration。
3. recheck 类动作仍能通过已有最小入口生效。
4. object_search_interaction 至少能以 prompt/action 摘要方式进入主流程。
5. experience_evolution 只读接入，不反写策略。
6. Viewer 能展示主线接入结果。
7. 不破坏主线 A、主线 2 第一阶段、主线 2 第二阶段既有链路与单测。

## 约束（本轮遵守）

- 不重构主流程
- 不正式修改 Task Chain 主体
- 不改 detector/OCR/Dynamic Policy 根逻辑
- 不让经验层反写策略
- 不新增新的大一统全局状态机
- 不做完整任务执行器改造
- 不做持久化数据库
- 不做学习型接入策略

## 修改文件清单

- `decision_monitor/mainline_integration.py`（新建）
- `decision_monitor/schema.py`（MainlineIntegrationResult 引用 + frame.mainline_integration）
- `decision_monitor/builder.py`（调用 build_mainline_integration，写入 frame）
- `runtime/context.py`（mainline_integration_* 字段）
- `main.py`（frame → runtime_ctx 写回 mainline_integration_*）
- `tools/decision_monitor_viewer.py`（主线接入 M0 卡片 + sections）
- `docs/MAINLINE_INTEGRATION_M0_DELIVERY.md`（本文件）
- `decision_monitor/CONTRACT.md`（主线接入 M0 条款）
