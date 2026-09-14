# 主线 2 第二阶段：Task Chain 接口对接 M0 交付说明

**依据**：Task Arbitration M0、Task Bundle M0、Object Search Interaction M1 已完成；增加“任务链摘要桥接层”，将下层运行事实统一映射为 Task Chain 可读摘要。  
**目标**：上层第一次真正“看懂”下层在发生什么；不正式改 Task Chain 主体、不做执行器。  
**约束**：不正式修改 Task Chain 主体、不做任务执行器、不做新全局大状态机、不做多 bundle 调度、不做数据库/持久化、不做学习型编排。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/task_chain_bridge.py` | **新建**。TaskChainBridgeResult；TASK_CHAIN_STATES / TASK_CHAIN_BUNDLE_STATES；build_task_chain_bridge(task_arbitration, task_bundle, object_search_interaction, state, current_foreground_task_type)；状态映射、foreground/substate/bundle_state/can_resume/summary_text 规则。 |
| `decision_monitor/schema.py` | 引入 TaskChainBridgeResult；DecisionMonitorFrame 新增 task_chain_bridge。 |
| `decision_monitor/builder.py` | 引入 task_chain_bridge；在 task_bundle 之后调用 build_task_chain_bridge，写入 frame.task_chain_bridge。 |
| `runtime/context.py` | 新增 task_chain_state、task_chain_substate、task_chain_foreground_summary、task_chain_can_resume、task_chain_bundle_state、task_chain_blocked、task_chain_block_reason、task_chain_summary_text、task_chain_bridge_applied。 |
| `main.py` | 写回 task_chain_bridge 各字段到 runtime_ctx。 |
| `tools/decision_monitor_viewer.py` | 新增「任务链桥接 / Task Chain Bridge (M0)」卡片；sections 增加 task_chain_bridge。 |
| `decision_monitor/CONTRACT.md` | 补充 task_chain_bridge 说明与未实现项。 |
| `docs/MAINLINE_2_TASK_CHAIN_BRIDGE_M0_DELIVERY.md` | **新建**。本文档。 |

---

## 2. TaskChainBridge 数据结构说明

### TaskChainBridgeResult

| 字段 | 类型 | 含义 |
|------|------|------|
| task_chain_foreground_summary | str | 前台任务摘要（如 object_search、blocked(safety_guard)、bundled(object_search+observation)） |
| task_chain_state | str | 任务链视角状态：active / paused / waiting_user / blocked / bundled / done / cancelled |
| task_chain_substate | str | 子状态摘要（如 searching_from_last_confirmed、bundle_active、safety_preempt、waiting_human_check） |
| task_chain_blocked | bool | 是否处于阻断状态 |
| task_chain_block_reason | str | 阻断原因（minimum_mode_active / runtime_domain_state=frozen 等） |
| task_chain_can_resume | bool | 是否可恢复主任务 |
| task_chain_bundle_state | str | bundle 语境：none / proposed / active / blocked / closed |
| task_chain_source_modules | List[str] | 当前摘要来源模块（task_arbitration、task_bundle、object_search_interaction） |
| task_chain_summary_text | str | 标准化摘要串，供任务链/日志/UI 使用 |
| task_chain_bridge_applied | bool | 桥接是否已应用 |

---

## 3. 状态映射规则说明

- **blocked**：minimum_mode_active、runtime_domain_state==frozen、scene_gate_action==freeze_to_minimum_mode、high_level_output_suppressed、human_check_pending 任一为真；或 arbitration_action==preempt 且 foreground_task_type==safety_guard。  
- **waiting_user**：human_check_pending 或 object_search_interaction.search_waiting_user_input==True。  
- **done**：object_search_interaction.search_terminal_status=="found"。  
- **cancelled**：object_search_interaction.search_terminal_status=="cancelled"。  
- **bundled**：task_bundle.bundle_created==True 且 bundle_status in (proposed, active)。  
- **paused**：goal_progress_paused==True 或 arbitration_action in (interrupt_then_resume, defer)。  
- **active**：以上皆不满足时。  

优先级：blocked > waiting_user > done > cancelled > bundled > paused > active。

---

## 4. foreground / substate / bundle_state 生成规则说明

- **task_chain_foreground_summary**：若 blocked 且 safety_guard → "blocked(safety_guard)"；若 bundled 且 bundle_task_types 非空 → "bundled(type1+type2+...)"；否则取 arbitration foreground_task_type 或 "unknown"。  
- **task_chain_substate**：阻断时取 safety_preempt 或 "blocked"；waiting_user 时取 "waiting_human_check"；bundled 时取 "bundle_active"；defer 时取 "deferred_by_conflict"；interrupt_then_resume 时取 "interrupt_then_resume"；否则沿用 object_search_interaction.search_subtask_state。  
- **task_chain_bundle_state**：直接来自 task_bundle.bundle_status，无 bundle 或未创建时为 "none"；proposed/active/blocked/closed 一一对应。  

---

## 5. can_resume 规则说明

- blocked 时 → False。  
- object_search_interaction.search_can_resume_main_task==True 或 search_terminal_status in (found, cancelled) → True。  
- arbitration_action==interrupt_then_resume 且 task_chain_state in (done, cancelled) → True。  
- 否则 → False。  

---

## 6. summary_text 生成规则说明

标准化字符串包含：前台任务、状态、子状态（若有）、可恢复、bundle 状态、阻断原因（若有）。  
示例风格：  
- “前台任务=object_search；状态=waiting_user；子状态=checking_container_candidate；可恢复=False；bundle=none”  
- “前台任务=bundled(object_search+observation)；状态=bundled；子状态=bundle_active；可恢复=False”  
- “前台任务=safety_guard；状态=blocked；子状态=safety_preempt；可恢复=False；原因=minimum_mode_active”  

---

## 7. Viewer 展示说明

- 卡片标题：任务链桥接 / Task Chain Bridge (M0)。  
- 展示：task_chain_foreground_summary、task_chain_state、task_chain_substate、task_chain_bundle_state、task_chain_can_resume、task_chain_blocked、task_chain_block_reason、task_chain_summary_text、task_chain_source_modules、task_chain_bridge_applied。  
- sections 可展开 task_chain_bridge 查看全部字段。  

---

## 8. 样本运行结果

- **无 search、无 bundle、未阻断** → task_chain_state=active，task_chain_foreground_summary 来自 arbitration，task_chain_bundle_state=none。  
- **search_terminal_status=found** → task_chain_state=done，task_chain_can_resume=True。  
- **human_check_pending 或 search_waiting_user_input** → task_chain_state=waiting_user，task_chain_substate=waiting_human_check。  
- **minimum_mode_active** → task_chain_state=blocked，task_chain_blocked=True，task_chain_block_reason=minimum_mode_active，task_chain_can_resume=False。  
- **bundle_created 且 bundle_status=active** → task_chain_state=bundled，task_chain_bundle_state=active，task_chain_foreground_summary 含 "bundled(...)"。  

---

## 9. 真实化与预留

| 项目 | 状态 |
|------|------|
| TaskChainBridgeResult 全字段、状态映射、foreground/substate/bundle_state/can_resume/summary_text、Viewer、runtime_ctx、仅读已有模块 | **真实化** |
| 正式改 Task Chain 主体、task dispatcher、多 bundle 调度、完整任务恢复器、数据库/持久化、学习型编排 | **未实现**（本轮不做） |

---

## 10. 验收与本轮是否通过

- **验收**：运行时存在可读 Task Chain Bridge 结果；arbitration/bundle/search 至少部分状态已映射为 task_chain_state；task_chain_state 覆盖 active/waiting_user/blocked/bundled/done/cancelled 等有效状态；task_chain_can_resume 有明确规则；Viewer 能展示；不破坏既有链路。  
- **本轮是否通过**：实现与文档满足上述要求即通过。
