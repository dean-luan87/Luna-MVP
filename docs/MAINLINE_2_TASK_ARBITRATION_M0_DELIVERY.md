# 主线 2 第二阶段：Task Arbitration M0 交付说明

**依据**：“意图池化 → 空间聚合 → 任务仲裁 → 骨架融合 → 分层执行”中任务仲裁层最小落成目标  
**目标**：把任务仲裁第一次落成最小运行时结构；五维判断、轻量 foreground/candidate 类型、仲裁动作输出；不做完整任务中心、不做多任务执行器、不正式改 Task Chain。  
**约束**：不做正式 Task Bundle 执行图、不做复杂任务对象模型、不做学习型编排、不新增大一统全局状态机。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/task_arbitration.py` | **新建**。TaskArbitrationResult；ARBITRATION_ACTIONS、FOREGROUND_TASK_TYPES、LEVELS；build_task_arbitration(goal, state, skeleton_mix, object_search_interaction, recheck_planner, object_temporal_ledger, incoming_task_*)；五维规则与仲裁规则。 |
| `decision_monitor/schema.py` | 引入 TaskArbitrationResult；DecisionMonitorFrame 新增 task_arbitration。 |
| `decision_monitor/builder.py` | 引入 task_arbitration；在 object_search_interaction 之后调用 build_task_arbitration，写入 frame.task_arbitration。 |
| `runtime/context.py` | 新增 current_foreground_task_type、task_arbitration_action/reason/risk/overlap/conflict/user_cost/applied、incoming_task_type/zone/risk/requires_user_attention。 |
| `main.py` | monitor_ctx 增加 incoming_task_*；写回 task_arbitration 各字段到 runtime_ctx。 |
| `tools/decision_monitor_viewer.py` | 新增「任务仲裁 / Task Arbitration (M0)」卡片；sections 增加 task_arbitration。 |
| `decision_monitor/CONTRACT.md` | 补充 task_arbitration 说明与未实现项。 |
| `docs/MAINLINE_2_TASK_ARBITRATION_M0_DELIVERY.md` | **新建**。本文档。 |

---

## 2. TaskArbitration 数据结构说明

### TaskArbitrationResult

| 字段 | 类型 | 含义 |
|------|------|------|
| foreground_task_type | str | 当前主任务类型（见 FOREGROUND_TASK_TYPES） |
| candidate_task_types | List[str] | 候选任务类型轻量列表 |
| arbitration_action | str | preempt / interrupt_then_resume / merge_into_bundle / run_in_background / defer / continue_current |
| arbitration_reason | str | 仲裁原因摘要 |
| risk_priority_level | str | low / medium / high |
| environment_overlap_level | str | low / medium / high |
| resource_conflict_level | str | low / medium / high |
| user_interruption_cost | str | low / medium / high |
| arbitration_applied | bool | 仲裁结果是否已应用 |

---

## 3. 五维判断规则说明

- **A/B. 风险与目标优先级（risk_priority_level）**：minimum_mode_active、runtime_domain_state==frozen、scene_gate_action==freeze_to_minimum_mode → high；degraded、high_level_suppressed、recheck_blocked → medium；否则 low。  
- **C. 资源冲突（resource_conflict_level）**：incoming 需用户注意力且当前 search_waiting 或 human_check_pending → high；同类型或同通道（object_search/recheck）→ medium；否则 low。  
- **D. 环境重合度（environment_overlap_level）**：incoming_task_zone 与当前 suggested_search_zone 包含关系 → high；有其一 → medium；否则 low。  
- **E. 用户打扰成本（user_interruption_cost）**：human_check_pending 或 search_waiting_user_input → high；foreground 为 object_search/interaction_confirm → medium；否则 low。  

---

## 4. arbitration_action 最小规则说明

- **preempt**：minimum_mode 或 frozen 或 scene_gate freeze → 安全/守底优先，foreground_task_type=safety_guard。  
- **merge_into_bundle**：incoming 存在且 environment_overlap_level==high 且 resource_conflict_level!=high。  
- **defer**：resource_conflict_level==high 且风险不足以 preempt。  
- **run_in_background**：incoming 为 observation/recheck 且 user_interruption_cost==low 且不需要用户注意力。  
- **interrupt_then_resume**：incoming_task_risk 为 high/medium 且当前为 navigation/observation 且 user_cost!=high。  
- **continue_current**：默认。  

---

## 5. foreground / candidate task 类型映射说明

- **foreground**：minimum_mode 或 frozen 或 freeze → safety_guard；Object Search 活跃（search_terminal_status==none 且 subtask 非 search_done）→ object_search；Recheck 有 action 且未 blocked → recheck；goal_type hold_for_floor → safety_guard；observe_navigate/confirm_path/slow_down_observe → navigation；close_range_check → interaction_confirm；run_detector_check/run_ocr_check/recheck_environment → observation。  
- **candidate_task_types**：从 recheck_planner、object_search_interaction、state（safety_guard）、skeleton_mix（observation/navigation）、incoming_task_type 收集去重，最多 8 项。  

---

## 6. Viewer 展示说明

- 卡片标题：任务仲裁 / Task Arbitration (M0)。  
- 展示：foreground_task_type、candidate_task_types、arbitration_action、arbitration_reason、risk_priority_level、environment_overlap_level、resource_conflict_level、user_interruption_cost、arbitration_applied。  
- sections 可展开 task_arbitration 查看全部字段。  

---

## 7. 样本运行结果

- **minimum_mode_active=True** → arbitration_action=preempt，foreground_task_type=safety_guard，risk_priority_level=high，arbitration_applied=False。  
- **无 incoming、正常导航** → arbitration_action=continue_current，foreground_task_type=navigation。  
- **incoming_task_type=observation、user_cost=low** → 可能 run_in_background。  
- **incoming_task_zone 与当前 suggested_search_zone 重合、conflict 非 high** → merge_into_bundle。  

---

## 8. 真实化与预留

| 项目 | 状态 |
|------|------|
| TaskArbitrationResult 全字段、五维规则、仲裁动作规则、foreground/candidate 映射、Viewer、runtime_ctx | **真实化** |
| 完整意图池、多任务执行器、正式 Task Bundle、正式改 Task Chain、学习型编排、数据库/持久化 | **未实现**（本轮不做） |

---

## 9. 验收与本轮是否通过

- **验收**：运行时存在可读 Task Arbitration 结果；能输出 preempt、merge_into_bundle、run_in_background、defer、continue_current 中部分有效决策；五维判断显式体现；Viewer 能展示；不破坏既有链路。  
- **本轮是否通过**：实现与文档满足上述要求即通过。
