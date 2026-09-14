# 主线 2 第二阶段：Object Search Interaction M1.5 交付说明

**依据**：Object Search Interaction M1 已完成；将“最小多轮寻物子任务”推进为更像真实人机协作任务流的交互式寻物系统。  
**目标**：多轮交互节奏、容器/遮挡/口袋三类分流、等待用户输入后的超时/回退逻辑、更明确的下一步建议链、search_resolution_path。  
**约束**：不正式改 Task Chain 主体、不做完整对话系统、不做多对象并发寻物、不做开放世界搜索、不新增大一统全局状态机。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/object_search_interaction.py` | INTERACTION_FLOW_TYPES、FALLBACK_ACTIONS；ObjectSearchInteractionResult 新增 interaction_flow_type、interaction_step_index、interaction_expected_user_input、interaction_timeout_ms、interaction_timeout_triggered、fallback_action、fallback_reason、next_search_step_summary、search_resolution_path、interaction_retry_count；build 新增 prev_flow_type/prev_step_index/prev_resolution_path/prev_retry_count/interaction_timeout_ms/interaction_timeout_triggered；flow 映射、超时 fallback、path 累积、next_search_step_summary 生成、默认 timeout 30s。 |
| `decision_monitor/builder.py` | 调用 build_object_search_interaction 时传入 object_search_flow_type、object_search_step_index、object_search_resolution_path（逗号分隔转 list）、object_search_retry_count、object_search_timeout_ms、object_search_timeout_triggered。 |
| `runtime/context.py` | 新增 object_search_flow_type、object_search_step_index、object_search_expected_input、object_search_timeout_ms、object_search_timeout_triggered、object_search_fallback_action、object_search_next_step、object_search_resolution_path、object_search_retry_count。 |
| `main.py` | monitor_ctx 增加 M1.5 上一帧字段；写回 frame.object_search_interaction 的 M1.5 字段到 runtime_ctx（含 resolution_path 逗号拼接）。 |
| `tools/decision_monitor_viewer.py` | 交互式寻物卡片升级为 M1.5，展示 flow、step_index、expected_input、timeout_ms/timeout_triggered、fallback_action/reason、next_search_step_summary、search_resolution_path、retry_count；sections 增加 M1.5 字段列表。 |
| `decision_monitor/CONTRACT.md` | object_search_interaction 段落补充 M1.5 说明与未实现项。 |
| `docs/MAINLINE_2_OBJECT_SEARCH_INTERACTION_M1_5_DELIVERY.md` | **新建**。本文档。 |

---

## 2. M1.5 数据结构升级说明

### ObjectSearchInteractionResult 新增字段

| 字段 | 类型 | 含义 |
|------|------|------|
| interaction_flow_type | str | container_check_flow / occlusion_clear_flow / pocket_check_flow / last_location_flow / description_bootstrap_flow |
| interaction_step_index | int | 当前流内步骤序号 |
| interaction_expected_user_input | str | 期待的用户输入类型（container_yes_no / occlusion_cleared / pocket_checked / object_appearance / last_location / user_reply） |
| interaction_timeout_ms | float | 等待超时毫秒（默认 30s） |
| interaction_timeout_triggered | bool | 本帧是否因超时触发回退 |
| fallback_action | str | 超时后的回退动作 |
| fallback_reason | str | 回退原因 |
| next_search_step_summary | str | 下一步建议链摘要 |
| search_resolution_path | List[str] | 本轮搜索走过的流节点（轻量） |
| interaction_retry_count | int | 超时回退触发次数 |

---

## 3. 典型 flow 规则说明

- **container_check_flow**：subtask_state==checking_container_candidate；发现容器候选→询问是否在容器/是否打开→用户 yes/opened→rechecking；用户 no→容器候选回退、not_found_yet。  
- **occlusion_clear_flow**：subtask_state==clearing_occlusion；遮挡/近场缺证→要求清理遮挡→用户确认已清理→rechecking；超时→continue_search_with_recheck 或 report_not_found_yet。  
- **pocket_check_flow**：action==ask_user_to_check_pocket 或 not_found_yet 且上一动作为口袋类；目标不可见且无强容器候选→提示检查口袋/包→用户已检查仍无→继续下一步；超时→ask_last_location 或 continue_search_with_recheck。  
- **last_location_flow**：subtask_state==searching_from_last_confirmed 且存在 last_confirmed 或用户给出 last_location；明确以最后位置为搜索起点。  
- **description_bootstrap_flow**：subtask_state in (target_unclear, gathering_description)；目标不清晰时先问外观/大小→用户回复后推进到 searching_from_last_confirmed 或 not_found_yet。  

---

## 4. timeout / fallback 规则说明

- 当 interaction_timeout_triggered==True 且上一动作为“等待用户输入”类时，执行 fallback。  
- **container_check_flow 超时**：fallback_action=ask_last_location，fallback_reason=容器确认超时，转为询问最后位置；subtask_state→not_found_yet，action→ask_last_location。  
- **occlusion_clear_flow 超时**：fallback_action=continue_search_with_recheck，fallback_reason=遮挡清理超时；subtask_state→rechecking，不再等待。  
- **pocket_check_flow 超时**：fallback_action=ask_last_location，fallback_reason=口袋检查超时；action→ask_last_location。  
- 其他等待超时：fallback_action=report_not_found_yet。  
- path 在超时回退时追加 "fallback" 节点；interaction_retry_count 自增。  
- 等待用户输入时若未传入 interaction_timeout_ms，默认 30000 ms。  

---

## 5. 用户输入与 flow 联动规则说明

- search_user_object_appearance → description_bootstrap_flow 推进。  
- search_user_last_location → last_location_flow，写回 object_user_confirmed_location。  
- search_user_container_answer → container_check_flow；yes/opened→rechecking；no→容器回退。  
- search_user_occlusion_cleared → occlusion_clear_flow→rechecking。  
- search_user_checked_pocket → pocket_check_flow→not_found_yet 或继续。  
- search_user_cancelled → 任意 flow 可终止，terminal=cancelled，can_resume=True。  
- last_user_response_type / last_user_response_value 继续更新；interaction_step_index 同 flow 内递增，换 flow 归零；retry_count 在超时回退时递增。  

---

## 6. next_search_step_summary / resolution_path 生成规则说明

- **next_search_step_summary**：由当前 action 与可选 fallback 拼接。例如：ask_user_to_open_container → “先打开{容器}确认；若未找到，再回到最后可信位置或继续查找”；ask_user_to_clear_occlusion → “先清理前方遮挡；若仍未发现，再检查容器或口袋”；report_last_confirmed_location → “先根据最后确认位置从{位置}开始；若无结果，再检查容器候选或询问最后放置位置”；ask_user_to_check_pocket → “先检查口袋/随身包；若仍未找到，再询问最后放置位置或继续补证”；ask_last_location → “先提供最后放置位置；再以此为起点继续搜索”；continue_search_with_recheck → “按补证建议继续搜索；若有遮挡或容器候选再分流处理”。若有 fallback_action，追加“超时回退:{fallback_action}”。  
- **search_resolution_path**：列表，最多保留约 12 个节点；当前 flow_type 与上一节点不同时追加；rechecking、candidate_found、search_done、fallback 按状态追加；用于 Viewer 与后续经验系统引用。  

---

## 7. Viewer 展示说明

- 卡片标题：交互式寻物 / Object Search Interaction (M1.5)。  
- 新增展示：interaction_flow_type、interaction_step_index、interaction_expected_user_input、interaction_timeout_ms、interaction_timeout_triggered、fallback_action、fallback_reason、next_search_step_summary、search_resolution_path（→ 串联）、interaction_retry_count。  
- 保留：search_subtask_state、interaction_action、interaction_prompt、suggested_search_zone、search_result_level、search_terminal_status、search_can_resume_main_task、blocking_issue、interaction_applied。  
- sections 可展开 object_search_interaction 查看全部 M1.5 字段。  

---

## 8. 样本运行结果

- **无目标/描述不足** → flow_type=description_bootstrap_flow，action=ask_object_appearance，expected_user_input=object_appearance，timeout_ms=30000。  
- **有容器候选** → flow_type=container_check_flow，action=ask_if_in_container 或 ask_user_to_open_container，expected_user_input=container_yes_no；用户回答 yes→rechecking，path 含 container_check_flow、rechecking。  
- **遮挡/近场缺证** → flow_type=occlusion_clear_flow，action=ask_user_to_clear_occlusion，expected_user_input=occlusion_cleared；超时触发→fallback_action=continue_search_with_recheck，path 含 fallback。  
- **无强容器、目标不可见** → flow_type=pocket_check_flow，action=ask_user_to_check_pocket；next_search_step_summary 含“先检查口袋/随身包…”。  
- **有 last_confirmed** → flow_type=last_location_flow，next_search_step_summary 含“先根据最后确认位置从…开始”。  

---

## 9. 真实化与预留

| 项目 | 状态 |
|------|------|
| interaction_flow_type、step_index、expected_user_input、timeout_ms、timeout_triggered、fallback_action/reason、next_search_step_summary、search_resolution_path、retry_count；三类 flow 显式化；超时+fallback 闭环；用户输入与 flow 联动；Viewer；runtime_ctx | **真实化** |
| 完整对话管理器、开放世界搜索、多对象并发寻物、经验沉淀与学习型策略、正式并入 Task Chain | **未实现**（本轮不做） |

---

## 10. 验收与本轮是否通过

- **验收**：运行时存在可读的 Object Search Interaction M1.5；三类典型 flow 至少有显式 flow_type 或状态表达；存在最小等待输入+超时+fallback 闭环；next_search_step_summary 能表达更像真实任务流的下一步建议链；search_resolution_path 存在；Viewer 能展示 flow/timeout/fallback/resolution path；不破坏既有链路。  
- **本轮是否通过**：实现与文档满足上述要求即通过。
