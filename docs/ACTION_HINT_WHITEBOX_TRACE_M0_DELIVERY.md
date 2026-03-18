# Action Hint Whitebox Trace M0（引导话术白盒轨迹 M0）交付

## 1. 目标与定位

在已通过的 Grid Search Whitebox Trace M0、Recheck Whitebox Trace M0、Action Hint Copy M0、Confirmation Input Bridge M0、Spatial Expression Sidecar / Local Task Space Grid / Grid-driven Search Expansion M0 基础上，为 `action_hint_copy` 建立正式白盒轨迹，使系统不仅输出主提示/后续提示/确认提示，还能够显式解释：

- 为什么主提示是这句
- 为什么 followup 是这句
- 为什么 confirmation 是这句
- 为什么没有选另一条提示路径
- 当前 flow / sidecar / grid / confirmation 如何影响话术

并补充**用户可见解释层**，用于未来线上与用户交互，帮助判断哪里错了、哪一步判断不合理。

**本轮定位**：不改 Action Hint 主逻辑；不做对话引擎；不做 NLG 重构；不做控制器升级；只做 Action Hint 的正式白盒化 + 用户可见解释层最小映射。

## 2. 核心原则（写死）

### 原则 1：沿用统一白盒模板

Action Hint Whitebox Trace 复用五块骨架：`reasoning_steps`、`weight_allocation`、`exclusion_log`、`interaction_trace`、`whitebox_summary` / `whitebox_applied`。

### 原则 2：话术要解释“为什么这样说”

白盒必须回答：为什么 primary/followup/confirmation 是当前句；当前话术更偏容器/遮挡/一般搜索/描述引导中的哪类；是否受 sidecar / grid / confirmation / current flow 影响。

### 原则 3：必须支持“用户可见白盒层”

除内部白盒字段外，必须额外产出一组**用户可见解释字段**（`ActionHintUserVisibleExplanation`），用于未来线上互动说明。用户可见层不得直接暴露原始内部 weight JSON，而要映射成简洁可理解的解释短句。

### 原则 4：结果与过程并存

保留原有 `action_hint_primary`、`action_hint_followup`、`action_hint_confirmation`、`action_hint_stage`、`action_hint_reason`。Whitebox Trace 是补全过程，不替代现有结果字段。

## 3. 代码交付

- 新增：`decision_monitor/action_hint_whitebox_trace.py`
- 接入：`decision_monitor/builder.py`（在 `action_hint_copy`、`confirmation_input_bridge`、`grid_search_expansion` 已构建之后）
- Frame：`decision_monitor/schema.py` 新增 `action_hint_whitebox_trace`
- 写回：`runtime/context.py` + `main.py` 写回白盒摘要与用户可见解释字段
- Viewer：`tools/decision_monitor_viewer.py` 新增卡片「引导话术白盒轨迹 / Action Hint Whitebox Trace (M0)」与专家模式 section

## 4. 数据结构

### 内部白盒（五块骨架）

- `ActionHintReasoningStep`：step_index / step_name / step_input_summary / step_output_summary
- `ActionHintWeightItem`：hint_id / hint_human_label / weight_total / weight_components / weight_reason
- `ActionHintExclusionItem`：excluded_hint_id / excluded_hint_human_label / excluded_reason / excluded_at_stage
- `ActionHintInteractionItem`：system_prompt_summary / user_feedback_raw / mapped_confirmation_type / next_effect / interaction_effect_on_hint
- `ActionHintWhiteboxTraceResult`：reasoning_steps / weight_allocation / exclusion_log / interaction_trace / **user_visible_explanation** / whitebox_summary / whitebox_applied

### 用户可见白盒层（解释映射，不直出 JSON）

- `ActionHintUserVisibleExplanation`：
  - `user_visible_reason_primary`
  - `user_visible_reason_followup`
  - `user_visible_reason_confirmation`
  - `user_visible_changed_by_feedback`
  - `user_visible_excluded_alternative`

## 5. 推理过程（固定 4 步）

1. **read_hint_context**：汇总 flow_type、focus_target_expression、grid 推荐、search 状态、confirmation input / next_effect
2. **select_primary_hint**：解释当前主提示类型（容器/遮挡/一般搜索/描述引导）及依据
3. **select_followup_and_confirmation**：解释 followup/confirmation 受 grid expansion 或目标短名影响
4. **compose_hint_outcome**：解释是否受反馈影响、是否携带 grid/sidecar 补位，并生成 whitebox_summary

## 6. 权重分配（规则权重，第一版写死）

- 容器流：container_hint_bonus(+0.70)、actionable_expression_bonus(+0.15)、container_name_bonus(+0.10)
- 遮挡流：occlusion_hint_bonus(+0.70)、near_field_bonus(+0.15)、focus_location_bonus(+0.10)
- 一般搜索：general_search_bonus(+0.50)、focus_present_bonus(+0.20)、grid_support_bonus(+0.10)
- 描述引导：bootstrap_bonus(+0.60)、target_unclear_bonus(+0.20)
- followup/confirmation：grid_followup_bonus(+0.20)、confirmation_phrase_bonus(+0.20)
- penalty：feedback_conflict_penalty(-0.30)、wrong_flow_penalty(-0.30)、over_specific_penalty(-0.10)、blocked_context_penalty(-0.20)

输出至少包含：当前被选 primary 的 weight、至少 1 个未被选主提示类型的 weight、1 个 followup/confirmation 的 weight（建议）。

## 7. 排除逻辑（Exclusion Log）

至少记录：其它主提示路径未被选中（如 flow=container 故未选遮挡提示）；其它 followup/confirmation 路径未被选中（如 grid expansion 已存在故未选“继续一般搜索”）。exclusion_log 至少 1～3 条，建议至少 1 条 followup/confirmation 级排除。

## 8. 互动过程（Interaction Trace）

读取 confirmation_input_bridge、action_hint_copy、grid_search_expansion、当前 search 状态。显式记录：当前系统提示摘要（primary/followup/confirmation）；用户反馈 raw/type/next_effect；对话术的影响（如 confirmed_no、opened_container、occlusion_cleared、target_found）。无互动时必须显式 `no_interaction_this_frame`。

## 9. 用户可见白盒层（必须）

至少生成：主提示解释（如“我之所以先让你看杯子里，是因为当前目标更像在容器里”）；后续提示解释；确认提示解释；反馈影响解释（如“你刚才说「没有」，所以我降低了这个方向的优先级”）；替代路径解释（如“我暂时没有先让你看别的位置，因为当前这个方向更相关”）。短句可对用户展示，不泄露内部 JSON/分值，但必须真实映射内部白盒原因。

## 10. 与现有模块关系

- **只读输入**：action_hint_copy、object_search_interaction、spatial_expression_sidecar、grid_search_expansion、confirmation_input_bridge、local_task_space_grid、evidence_ledger、hypothesis_layer（若需要）
- **不反写**：不改变 Action Hint 结果、Search 状态机、ConfirmationInputBridge 结果、Recheck/evidence/experience/arbitration/bundle

## 11. 接入位置

- **builder**：在 action_hint_copy、confirmation_input_bridge、grid_search_expansion 已构建之后构建 action_hint_whitebox_trace
- **frame**：DecisionMonitorFrame 新增 action_hint_whitebox_trace
- **runtime_ctx**：action_hint_whitebox_summary、action_hint_whitebox_primary_score、action_hint_whitebox_exclusion_summary、action_hint_whitebox_interaction_summary、action_hint_user_visible_reason_primary、action_hint_user_visible_changed_by_feedback
- **Viewer**：卡片展示 reasoning steps、selected primary weight、exclusion log、interaction trace、user visible explanation、whitebox summary、applied；专家模式可展开完整 trace

## 12. 验收标准

1. frame 中存在可审计的 `action_hint_whitebox_trace`
2. reasoning_steps 至少 4 步
3. weight_allocation 至少包含 selected primary + 1 个排除话术路径
4. exclusion_log 至少 1 条
5. interaction_trace 能记录“有互动”或“无互动”
6. user_visible_explanation 存在
7. Viewer / runtime_ctx 可见白盒摘要与用户可见解释
8. 不破坏：action_hint_copy、grid_search_expansion、recheck_whitebox_trace、object_search_interaction 主状态机、confirmation_input_bridge、evidence/experience/arbitration/bundle

## 13. 测试要求（最小）

- **图2（遮挡流，无互动）**：primary 解释为“先移开遮挡”；exclusion 能说明“没选容器提示/一般搜索提示”；user_visible_reason_primary 有值；interaction_trace = no_interaction_this_frame
- **图3（容器流，有反馈）**：如加 opened_container 或 confirmed_no；primary 解释为“先看杯子里”；feedback 影响解释有值；user_visible_changed_by_feedback 有值

## 14. 文档同步

- 本文档：`docs/ACTION_HINT_WHITEBOX_TRACE_M0_DELIVERY.md`
- 已更新：`decision_monitor/CONTRACT.md`、`docs/PHASE2_STATUS_MATRIX.md`、`docs/WHITEBOX_TRACE_SCHEMA_FREEZE_M0.md`、`docs/PHASE2_INTERFACE_FREEZE.md`

当前 Action Hint 已完成白盒化；当前支持用户可见解释层；当前只解释现有话术结果，不改写主逻辑。

---

## 15. 本轮结论（待审计后写死）

- **本轮结论**：**实现通过 + 测试均通过（单测 + smoke/JSONL）**。
- **实现通过**：`decision_monitor/action_hint_whitebox_trace.py` 已接入 `decision_monitor/builder.py` 并落入 `DecisionMonitorFrame.action_hint_whitebox_trace`。
- **自动化测试通过**：4/4 通过（`tests/test_action_hint_whitebox_trace.py`；覆盖遮挡无互动、容器有反馈、bootstrap、用户可见解释层完整性）。
- **smoke / JSONL 验证通过**：已运行最小 smoke 脚本 `tools/smoke_action_hint_whitebox_trace.py`，生成 1 帧 JSONL（`logs/smoke_action_hint_whitebox_trace_*.jsonl`），并验证：
  - frame 中存在 `action_hint_whitebox_trace`
  - `mainline_integration.integration_summary` 非空（可作为 runtime_ctx 摘要审计入口）
- **当前状态**：实现完成；单测通过；smoke/JSONL 验证通过；用户可见白盒层已接入。
