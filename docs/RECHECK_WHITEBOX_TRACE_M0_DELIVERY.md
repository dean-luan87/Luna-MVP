# Recheck Whitebox Trace M0（补证链路白盒轨迹 M0）交付

## 1. 目标与定位

本交付将 Recheck（补证）从“有补证建议动作”升级为“有白盒补证过程”。在不新增补证动作、**不改** `recheck_planner` 主逻辑、**不改** `object_search_interaction` 主状态机、**不做** 控制层升级的前提下，为补证链路补齐可审计的白盒轨迹。

白盒轨迹必须回答：

- 为什么要补证
- 为什么选这个补证动作
- 为什么没选别的补证动作
- 当前阻断来自哪里
- 用户反馈或当前 flow 如何影响补证语义（仅解释，不反写主逻辑）

## 2. 核心原则（冻结约束复用）

- **沿用统一白盒模板**：复用冻结的五块骨架：`reasoning_steps / weight_allocation / exclusion_log / interaction_trace / whitebox_summary + whitebox_applied`
- **结果与过程并存**：保留 `recheck_planner` 原字段（`recheck_action/recheck_reason/recheck_target/recheck_blocked/...`），白盒仅补全过程
- **阻断显式化**：`minimum_mode_active / runtime_domain_state=frozen / scene_gate freeze / high_level_output_suppressed / human_check_pending` 等必须进入 reasoning/exclusion/summary 的可读项，而非仅一个 `blocked` 标志

## 3. 代码交付

- 新增：`decision_monitor/recheck_whitebox_trace.py`
- 接入：`decision_monitor/builder.py`（在 `recheck_planner` 已有结果、且 `confirmation_input_bridge` 已构建后）
- Frame：`decision_monitor/schema.py` 新增 `recheck_whitebox_trace`
- 写回：`runtime/context.py` + `main.py` 写回摘要字段
- Viewer：`tools/decision_monitor_viewer.py` 新增卡片与专家模式 section

## 4. 数据结构（与统一白盒模板对齐）

`RecheckWhiteboxTraceResult`：

- `reasoning_steps: List[RecheckReasoningStep]`
- `weight_allocation: List[RecheckWeightItem]`
- `exclusion_log: List[RecheckExclusionItem]`
- `interaction_trace: List[RecheckInteractionItem]`
- `whitebox_summary: Optional[str]`
- `whitebox_applied: bool`

其中：

- `RecheckReasoningStep`: `step_index/step_name/step_input_summary/step_output_summary`
- `RecheckWeightItem`: `action_id/action_human_label/weight_total/weight_components/weight_reason`
- `RecheckExclusionItem`: `excluded_action_id/excluded_action_human_label/excluded_reason/excluded_at_stage`
- `RecheckInteractionItem`: `system_prompt_summary/user_feedback_raw/mapped_confirmation_type/next_effect/interaction_effect_on_recheck`

## 5. 推理过程（Reasoning Steps）规则

固定 4 步写死：

1. `read_recheck_context`：汇总 flow、hypothesis、missing evidence、当前 recheck_action/blocked、confirmation input
2. `select_recheck_action`：解释当前 action 与其依据（不改变 action）
3. `exclude_other_actions`：解释替代动作未选中或被阻断（进入 `exclusion_log`）
4. `compose_recheck_outcome`：解释 blocked 与 action 的主链含义，并生成 `whitebox_summary`

## 6. 权重分配（Weight Allocation）规则

当前为显式规则权重（非学习），第一版写死：

- 近场补证优先：`close_range_bonus(+0.60) / focus_present_bonus(+0.20) / container_or_occlusion_bonus(+0.15)`
- 环境补证优先：`environment_bonus(+0.60) / wide_uncertainty_bonus(+0.20) / no_clear_focus_bonus(+0.10)`
- 视角动作优先：`look_forward_bonus(+0.40) / directional_alignment_bonus(+0.20)`
- 等待/确认优先：`hold_and_confirm_bonus(+0.50) / human_input_needed_bonus(+0.20)`
- penalty：`blocked_penalty(-0.80) / human_check_pending_penalty(-0.60) / wrong_scope_penalty(-0.30) / weak_evidence_penalty(-0.10)`

输出要求：

- `weight_allocation` 至少包含 **selected action + 1~2 个排除 action**
- 每条包含 `weight_components` 与简短 `weight_reason`

## 7. 排除逻辑（Exclusion Log）规则

至少记录 1~3 条：

- **替代动作未选中**：例如 local container/occlusion flow 下 `recheck_environment` 被排除
- **动作被阻断**：例如 `human_check_pending` / `minimum_mode_active` 导致排除原因包含 `blocked:*`

## 8. 互动过程（Interaction Trace）规则

读取：

- `confirmation_input_bridge`（raw/type/next_effect）
- `action_hint_copy`（system_prompt_summary）

无互动时必须显式：`no_interaction_this_frame`（由 `interaction_effect_on_recheck` 给出）

## 9. runtime_ctx 写回字段

- `recheck_whitebox_summary`
- `recheck_whitebox_primary_score`
- `recheck_whitebox_exclusion_summary`
- `recheck_whitebox_interaction_summary`

## 10. 验收标准对齐

- frame/jsonl 中存在 `recheck_whitebox_trace`
- reasoning_steps 固定 4 步
- weight_allocation 覆盖 selected + 1~2 excluded
- exclusion_log 至少 1 条
- interaction_trace 覆盖有/无互动
- Viewer 与 runtime_ctx 可见摘要
- 不改动 `recheck_planner` / `object_search_interaction` 主逻辑

---

## 11. 本轮结论（写死）

- **本轮结论**：通过  
- **自动化测试**：4/4 通过（`tests/test_recheck_whitebox_trace.py`）  
- **实跑 smoke**：通过（`run_video_a3_trace.py --smoke --max-frames N`）  
- **JSONL 审计**：通过（frame 中明确出现 `recheck_whitebox_trace`）  
- **当前状态**：**实现 + 测试均通过**

自动化测试与 smoke 验证已通过，具备完全通过口径。若内部保留“回归/性能全量跑过才叫完全通过”的更高标准，则以该更高标准为准；否则本交付可定性为完全通过。

**结构通过**：五块白盒骨架齐全；frame / viewer / runtime_ctx / jsonl 全接上；不改 recheck_planner 主逻辑。  
**单测覆盖**：正常补证、阻断态、无互动、有 confirmation 输入。  
**白盒主线**：与 Grid Search Whitebox Trace M0 并列，当前 Luna 白盒骨架已有两个正式通过样板（搜索建议层 + 补证层）。下一步可进入 Action Hint Whitebox Trace M0，将引导话术层白盒化。

