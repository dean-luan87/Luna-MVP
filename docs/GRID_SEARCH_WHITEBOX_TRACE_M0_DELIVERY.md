# Grid Search Whitebox Trace M0 交付说明（局部任务空间格搜索扩展白盒轨迹 M0）

**定位**：不是新功能层，不改变 Grid-driven Search Expansion 的建议结果。  \
本模块将扩搜建议层过程化、可解释化、可审计化：推理过程、权重分配、排除逻辑、互动过程都进入 frame/viewer/runtime_ctx/jsonl。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/grid_search_whitebox_trace.py` | **新建**。Whitebox 数据结构与 build_grid_search_whitebox_trace |
| `decision_monitor/schema.py` | DecisionMonitorFrame 新增 `grid_search_whitebox_trace` |
| `decision_monitor/builder.py` | 在 grid_search_expansion 之后构建 whitebox，并写入 frame（不改 expansion 结果） |
| `runtime/context.py` | 新增 whitebox 摘要字段：grid_search_whitebox_summary / primary_score / exclusion_summary / interaction_summary |
| `main.py` | 写回上述摘要字段到 runtime_ctx |
| `tools/decision_monitor_viewer.py` | 新增「搜索扩展白盒轨迹」卡片；sections 增加 grid_search_whitebox_trace |

---

## 2. 数据结构说明

- `GridSearchReasoningStep`：step_index/name/input_summary/output_summary
- `GridSearchWeightItem`：cell_id/human_label/weight_total/weight_components/weight_reason
- `GridSearchExclusionItem`：excluded_cell_id/human_label/excluded_reason/excluded_at_stage
- `GridSearchInteractionItem`：system_prompt_summary/user_feedback_raw/mapped_confirmation_type/next_effect/interaction_effect_on_search
- `GridSearchWhiteboxTraceResult`：reasoning_steps、weight_allocation、exclusion_log、interaction_trace、whitebox_summary、whitebox_applied

---

## 3. 推理过程（Reasoning Trace）

固定 4 步（M0）：read_context → select_primary → select_secondary → compose_hint。每步记录输入摘要与输出摘要。

---

## 4. 权重分配（Weight Allocation Trace）

即使是规则，也显式权重化（固定规则权重，非学习权重）。\n\n- 容器流：container_priority_score=+0.70、focus_bonus=+0.20、adjacency_bonus=+0.15、same_row_bonus=+0.05\n- 遮挡流：occlusion_priority_score=+0.70、focus_bonus=+0.20、adjacency_bonus=+0.15、same_column_bonus=+0.05\n- 一般搜索：focus_priority_score=+0.60、adjacency_bonus=+0.20、same_band_bonus=+0.10\n- penalty：confirmation_rejection_penalty=-0.40、non_adjacent_penalty=-0.20、weak_relevance_penalty=-0.10\n\n输出包含 primary、secondary，以及至少 1 个排除格（或弱相关格）的总分与组成项。

---

## 5. 排除逻辑（Exclusion Trace）

exclusion_log 至少保留 1~3 条：\n- 未作 primary 的原因（flow 优先级/限制）\n- 未入 secondary 的原因（非邻接/超限/弱相关/交互否定信号）

---

## 6. 互动过程（Interaction Trace）

读取 action_hint_copy 与 confirmation_input_bridge：\n- 系统刚才提示（primary/followup 摘要）\n- 用户反馈 raw、映射类型、next_effect\n- 对扩搜的影响描述（仅在 trace 中体现，不反写 expansion）\n\n无互动时写 `no_interaction_this_frame`。

---

## 7. 接入说明

- **builder**：grid_search_expansion 之后构建 whitebox，写入 frame.grid_search_whitebox_trace。\n- **runtime_ctx**：写回 whitebox_summary、primary_score、exclusion_summary、interaction_summary。\n- **Viewer**：展示 reasoning/weights/exclusion/interaction 的摘要块，并在专家 sections 可展开完整结构。\n\n---

## 8. 验收要点

- frame 中存在 grid_search_whitebox_trace\n- reasoning_steps ≥ 4\n- weight_allocation 至少包含 primary/secondary/排除格\n- exclusion_log ≥ 1\n- interaction_trace 能反映有/无互动\n- 不改变 expansion 结果与主状态机\n+
