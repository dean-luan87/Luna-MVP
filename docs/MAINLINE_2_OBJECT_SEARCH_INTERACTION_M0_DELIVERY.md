# 主线 2 第二阶段：Object Search Interaction M0 交付说明

**依据**：Object Temporal Ledger M1.5 已完成；主线 2 第二阶段交互式寻物最小版目标  
**目标**：在对象账本/证据/假设/补证基础上，增加最小“交互式寻物层”，生成最小人机协作搜索动作建议；不做法语系统、不做复杂多轮规划、不做开放世界搜索。  
**约束**：仅读取已有结构；不新增主感知输入；不改 detector/OCR/Dynamic Policy 主链；不多对象并行寻物；不持久化。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/object_search_interaction.py` | **新建**。SEARCH_STATES、INTERACTION_ACTIONS、PROMPT_TEMPLATES；ObjectSearchInteractionResult；build_object_search_interaction(focus_object_label, object_temporal_ledger, evidence_ledger, hypothesis_layer, recheck_planner, state)。 |
| `decision_monitor/schema.py` | 引入 ObjectSearchInteractionResult；DecisionMonitorFrame 新增 object_search_interaction。 |
| `decision_monitor/builder.py` | 引入 object_search_interaction；在 object_temporal_ledger 之后调用 build_object_search_interaction，写入 frame.object_search_interaction。 |
| `runtime/context.py` | 新增 object_search_action、object_search_prompt、object_search_zone、object_search_state、object_search_applied。 |
| `main.py` | 决策显示器块内将 object_search_interaction 摘要写入 runtime_ctx。 |
| `tools/decision_monitor_viewer.py` | 新增「交互式寻物 / Object Search Interaction (M0)」卡片；sections 增加 object_search_interaction。 |
| `decision_monitor/CONTRACT.md` | 补充 object_search_interaction 说明与未实现项。 |
| `docs/MAINLINE_2_OBJECT_SEARCH_INTERACTION_M0_DELIVERY.md` | **新建**。本文档。 |

---

## 2. ObjectSearchInteraction 数据结构说明

### ObjectSearchInteractionResult

| 字段 | 类型 | 含义 |
|------|------|------|
| search_target_label | str | 当前搜索目标标签（来自 focus_object_label） |
| search_state | str | target_unclear / searching / candidate_found / needs_user_input / needs_environment_change / not_found_yet |
| interaction_action | str | 见下方固定动作集合 |
| interaction_reason | str | 选择该动作的原因摘要 |
| interaction_prompt | str | 标准化短提示（供语音/多轮交互层引用） |
| suggested_search_zone | str | 建议搜索区域摘要（字符串） |
| blocking_issue | str | 阻断时写明来源 |
| interaction_applied | bool | 是否已执行（阻断时为 False） |

### interaction_action 固定集合

- ask_object_appearance / ask_last_location / ask_if_in_container  
- ask_user_to_clear_occlusion / ask_user_to_check_pocket / ask_user_to_open_container  
- continue_search_with_recheck  
- report_candidate_location / report_last_confirmed_location / report_not_found_yet  

---

## 3. interaction_action 与 search_state 规则说明

- **A. 目标描述不足**：focus_object_label 为空/过弱或 object_profile_summary 很弱 → search_state=target_unclear，action=ask_object_appearance。  
- **B. 有最后可信位置但当前无强候选** → search_state=not_found_yet 或 searching，action=report_last_confirmed_location。  
- **C. 存在容器候选**（container_state 为 object_inside_candidate / container_open_candidate / container_closed_candidate 等）→ 优先 ask_user_to_open_container 或 ask_if_in_container / report_candidate_location；search_state 可为 candidate_found 或 searching。  
- **D. 遮挡/近场缺证**（occluded_object_candidate 或 visibility 为 occluded/lost）→ action=ask_user_to_clear_occlusion 或 continue_search_with_recheck；search_state=needs_environment_change 或 searching。  
- **E. 高风险/阻断**（minimum_mode_active、runtime_domain_state==frozen、human_check_pending、recheck_blocked 等）→ interaction_applied=False，blocking_issue 写明来源；action 保留为建议。  
- **F. 口袋类建议**（最小占位）：对象不可见且容器候选弱 → action=ask_user_to_check_pocket，search_state=needs_user_input。  

---

## 4. interaction_prompt 标准化规则说明

- 每个 interaction_action 对应 PROMPT_TEMPLATES 中的标准短句。  
- 示例：ask_object_appearance→「请描述一下目标的大概外观或大小」；report_last_confirmed_location→可拼接 last_confirmed 位置；report_candidate_location→可拼接候选位置。  
- 本轮只输出标准化短提示，不生成最终自然语言大段文案。  

---

## 5. suggested_search_zone 生成规则说明

- 从 object_temporal_ledger 抽取：last_confirmed_location、current_candidate_location、current_container_candidate。  
- 按规则拼接为字符串摘要，如「last_confirmed / 容器候选 / 近场遮挡区 / 口袋类候选」。  
- 当前仅做字符串摘要，不做几何搜索图。  

---

## 6. 阻断规则说明

- 与 recheck_planner 一致：minimum_mode_active、runtime_domain_state==frozen、scene_gate_action==freeze_to_minimum_mode、high_level_output_suppressed、human_check_pending。  
- 若 recheck_planner.recheck_blocked 为 True，同样视为阻断，blocking_issue 可取 recheck_block_reason。  
- 阻断时 interaction_applied=False，blocking_issue 写明来源；interaction_action 仍保留为建议。  

---

## 7. Viewer 展示说明

- 卡片标题：交互式寻物 / Object Search Interaction (M0)。  
- 展示：当前目标、search_state、interaction_action、interaction_reason、interaction_prompt、suggested_search_zone、blocking_issue、interaction_applied。  
- sections 可展开 object_search_interaction 查看全部字段。  

---

## 8. 样本运行结果

- 无 focus_object 或目标过弱 → target_unclear + ask_object_appearance。  
- 有 last_confirmed、无强候选 → report_last_confirmed_location + suggested_search_zone 含该位置。  
- 有 container_candidate 且 container_state 为 object_inside_candidate → ask_user_to_open_container 或 ask_if_in_container。  
- 遮挡/occluded → ask_user_to_clear_occlusion 或 continue_search_with_recheck。  
- state 中 minimum_mode_active 或 human_check_pending 为 True → interaction_applied=False，blocking_issue 有值。  

---

## 9. 真实化与预留

| 项目 | 状态 |
|------|------|
| ObjectSearchInteractionResult 全部字段、规则 A～F、阻断、PROMPT_TEMPLATES、suggested_search_zone 字符串摘要 | **真实化** |
| 完整对话系统、复杂多轮规划、开放世界搜索、对象识别学习、语音/NLG 最终话术层、多对象并行寻物 | **未实现**（本轮不做） |

---

## 10. 验收与本轮是否通过

- **验收**：运行时存在可读 Object Search Interaction 结果；能生成多种 interaction_action；目标不足追问、有最后可信报告起点、有容器候选提示、有遮挡提示；阻断时不误标已执行；Viewer 可展示；不破坏既有链路。  
- **本轮是否通过**：实现与文档满足上述要求即通过。
