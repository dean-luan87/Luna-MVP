# 主线 2 第二阶段：Object Search Interaction M1 交付说明

**依据**：Object Search Interaction M0 已完成；主线 2 第二阶段 M1 目标  
**目标**：将“单步交互建议层”推进为“最小多轮寻物子任务”——子任务内部状态机、用户回复写回、交互链串联、结果分级、任务链接口预留（只对齐接口，不正式并入 Task Chain）。  
**约束**：不正式合并 Task Chain；不做完整对话系统；不做多对象并发寻物；不做开放世界搜索；不新增全局状态机（仅寻物子任务内部状态机）。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/object_search_interaction.py` | M1：SUBTASK_STATES、TERMINAL_STATUSES、RESULT_LEVELS；ObjectSearchInteractionResult 新增 search_subtask_state、search_waiting_user_input、search_terminal_status、search_can_resume_main_task、search_summary_for_task_chain、last_interaction_action、last_user_response_type/value、candidate_confidence_level、search_result_level；build 增加 prev_subtask_state、prev_last_interaction_action、prev_search_terminal_status 与 search_user_* 参数；实现最小状态机与用户回复驱动流转、结果分级。 |
| `decision_monitor/builder.py` | 将 search_user_last_location 映射为 object_user_confirmed_location、search_user_container_answer=no 映射为 object_user_denied_location 传入 build_object_temporal_ledger；build_object_search_interaction 传入 prev_* 与 search_user_*（来自 ctx）。 |
| `runtime/context.py` | 新增 search_subtask_state、search_waiting_user_input、search_terminal_status、search_can_resume_main_task、search_result_level、last_interaction_action；新增用户回复注入字段 search_user_object_appearance、search_user_last_location、search_user_container_answer、search_user_occlusion_cleared、search_user_checked_pocket、search_user_cancelled。 |
| `main.py` | monitor_ctx 增加上一帧子任务状态与用户回复字段；写回 runtime_ctx 增加 M1 寻物字段。 |
| `tools/decision_monitor_viewer.py` | 卡片升级为 M1：展示 search_subtask_state、search_result_level、search_waiting_user_input、search_terminal_status、search_can_resume_main_task；sections 增加 M1 字段。 |
| `decision_monitor/CONTRACT.md` | object_search_interaction 段落更新为 M0/M1；已支持用户回复注入与状态流转、任务链接口预留；未实现项更新。 |
| `docs/MAINLINE_2_OBJECT_SEARCH_INTERACTION_M1_DELIVERY.md` | **新建**。本文档。 |

---

## 2. M1 数据结构升级说明

### ObjectSearchInteractionResult 新增/明确

| 字段 | 类型 | 含义 |
|------|------|------|
| search_subtask_state | str | 寻物子任务内部状态（见 SUBTASK_STATES） |
| search_waiting_user_input | bool | 是否正在等待用户输入 |
| search_terminal_status | str | none / found / not_found / blocked / cancelled |
| search_can_resume_main_task | bool | 是否可恢复主任务 |
| search_summary_for_task_chain | str | 供任务链使用的摘要（仅预留） |
| last_interaction_action | str | 本帧输出的交互动作（下一帧为 prev） |
| last_user_response_type | str | 本帧消费的用户回复类型 |
| last_user_response_value | str | 本帧消费的用户回复值摘要 |
| candidate_confidence_level | float | 当前候选置信度 |
| search_result_level | str | confirmed / high_probability / weak_candidate / unresolved |

### 子任务状态（SUBTASK_STATES）

target_unclear、gathering_description、searching_from_last_confirmed、checking_container_candidate、clearing_occlusion、rechecking、waiting_user_reply、candidate_found、not_found_yet、search_done。

---

## 3. 子任务状态机规则说明

- **target_unclear / gathering_description**：目标弱或画像不足时进入；若收到 search_user_object_appearance → searching_from_last_confirmed（有 last_confirmed）或 not_found_yet。  
- **searching_from_last_confirmed**：存在 last_confirmed 时进入；有强容器候选 → checking_container_candidate；有遮挡 → clearing_occlusion；有强候选 → candidate_found。  
- **checking_container_candidate**：存在容器候选时进入；用户 container_answer=yes/opened → rechecking；no → not_found_yet，并写回 object_user_denied_location。  
- **clearing_occlusion**：遮挡/近场缺证时进入；search_user_occlusion_cleared=True → rechecking。  
- **rechecking**：补证进行中；可回到 candidate_found、not_found_yet、checking_container_candidate、clearing_occlusion。  
- **candidate_found**：强候选；search_result_level=high_probability 或 confirmed。  
- **not_found_yet**：未确认位置；search_result_level=weak_candidate 或 unresolved。  
- **search_done**：用户确认找到或取消；search_terminal_status=found/cancelled；search_can_resume_main_task=True。  
- **cancelled**：search_user_cancelled=True → search_done，terminal=cancelled。

---

## 4. 用户回复写回规则说明

- **search_user_last_location**：通过 ctx 传入 builder，映射为 object_user_confirmed_location 传入 build_object_temporal_ledger，更新 last_confirmed_location。  
- **search_user_container_answer=no**：将 object_container_candidate 作为 object_user_denied_location 传入 ledger，回退容器候选。  
- **search_user_container_answer=yes/opened**：不写回 ledger，子任务状态推进到 rechecking。  
- **search_user_occlusion_cleared**：状态推进到 rechecking。  
- **search_user_checked_pocket**：状态推进到 not_found_yet。  
- **search_user_object_appearance**：当前保存在 search interaction 的 last_user_response_* 中；若对象账本支持 appearance 摘要可后续扩展写回。

---

## 5. interaction_action 串联规则说明

- 各子任务状态映射到固定动作集合中的动作：target_unclear → ask_object_appearance；checking_container_candidate → ask_user_to_open_container / ask_if_in_container；clearing_occlusion → ask_user_to_clear_occlusion；rechecking → continue_search_with_recheck；searching_from_last_confirmed → report_last_confirmed_location；candidate_found → report_candidate_location；not_found_yet → report_not_found_yet / ask_last_location 等。  
- interaction_reason、interaction_prompt、suggested_search_zone 随状态与动作一起更新。

---

## 6. 结果分级规则说明

- **confirmed**：用户确认或 last_confirmed + 证据强一致（ledger_confidence≥0.85 等）。  
- **high_probability**：容器候选/当前位置候选较强（container_confidence≥0.5 或 ledger_confidence≥0.6）。  
- **weak_candidate**：仅有弱候选或需继续补证。  
- **unresolved**：当前无足够候选，仅知下一步排查方向。

---

## 7. 任务链接口预留说明

- 仅新增并写入摘要字段：search_subtask_state、search_waiting_user_input、search_terminal_status、search_can_resume_main_task、search_summary_for_task_chain。  
- 不做 task registration / dispatcher 改造，不正式改 Task Chain 主逻辑。

---

## 8. Viewer 展示说明

- 卡片标题：交互式寻物 / Object Search Interaction (M1)。  
- 展示：search_target_label、search_subtask_state、interaction_action、interaction_prompt、suggested_search_zone、search_result_level、search_waiting_user_input、search_terminal_status、search_can_resume_main_task、blocking_issue、interaction_applied。  
- sections 保留完整展开（含 last_user_response_*、candidate_confidence_level、search_summary_for_task_chain 等）。

---

## 9. 样本运行结果

- 无目标/弱目标 → target_unclear、ask_object_appearance、search_waiting_user_input=True。  
- 注入 search_user_last_location → searching_from_last_confirmed、report_last_confirmed_location；ledger 收到 object_user_confirmed_location。  
- 注入 search_user_cancelled=True → search_done、search_terminal_status=cancelled、search_can_resume_main_task=True。  
- 有容器候选 → checking_container_candidate、ask_if_in_container 或 ask_user_to_open_container；search_result_level=high_probability 或 weak_candidate。

---

## 10. 真实化与预留

| 项目 | 状态 |
|------|------|
| 子任务状态机、用户回复注入与驱动流转、结果分级、任务链接口字段、用户回复写回 ledger（last_location/container no） | **真实化** |
| 正式合并 Task Chain、完整对话管理、多对象并发寻物、开放世界搜索、经验沉淀 | **未实现**（本轮不做） |

---

## 11. 验收与本轮是否通过

- **验收**：运行时存在可读 Object Search Interaction M1；具备最小寻物子任务状态机；用户回复可注入并驱动状态变化；interaction_action 与状态串联；结果分级存在；任务链接口字段预留且未正式并入 Task Chain；Viewer 可展示子任务状态与下一步动作；不破坏 M0 及既有链路。  
- **本轮是否通过**：实现与文档满足上述要求即通过。
