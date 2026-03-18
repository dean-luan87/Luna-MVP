# Phase 2 接口冻结文档（Interface Freeze）

**说明**：以下字段/接口为 Phase 2 收口后的**冻结基线**。后续模块优先复用，不得随意改名或改语义；如必须改，需在本文档与 CONTRACT 中**显式修订**。

---

## A. 视觉候选侧接口

| 字段/接口 | 含义 | 来源 |
|-----------|------|------|
| detector_mode | 检测器模式（如 real_yolo / demo_fallback） | visual_candidate_audit |
| detector_candidate_labels | 主路检测候选标签列表 | visual_candidate_audit |
| mapped_candidate_labels | 与 search_target 映射上的候选标签 | visual_candidate_audit |
| candidate_audit_status | 候选审计状态 | visual_candidate_audit |
| probe / main 候选语义边界 | main 候选与 probe 候选分离；probe 不污染主候选 | 视觉层约定 |

---

## B. 空间表达侧接口

| 字段/接口 | 含义 | 来源 |
|-----------|------|------|
| focus_target_expression | Level 1 相对位置表达（如 中间偏左/中间偏右） | spatial_expression_sidecar |
| focus_target_debug_expression | 精确/日志层表达（sector、bearing、band 等） | spatial_expression_sidecar |
| focus_target_actionable_expression | Level 2 口语化行动表达（近场试点） | spatial_expression_sidecar |
| focus_target_actionable_debug_reason | Level 2 生成依据摘要 | spatial_expression_sidecar |

---

## C. Search 文案侧接口

| 字段/接口 | 含义 | 来源 |
|-----------|------|------|
| suggested_search_zone | 建议搜索区（可含 L1/L2 位置短语） | object_search_interaction |
| next_search_step_summary | 下一步建议摘要（可含位置+动作） | object_search_interaction |
| search_zone_from_sidecar | 本帧 zone 是否来自 sidecar | object_search_interaction |

---

## D. Action Hint 接口

| 字段/接口 | 含义 | 来源 |
|-----------|------|------|
| action_hint_primary | 主提示（先看哪里/先检查什么/先移开什么） | action_hint_copy |
| action_hint_followup | 后续提示 | action_hint_copy |
| action_hint_confirmation | 确认提示 | action_hint_copy |
| action_hint_stage | reasoning / guidance / confirmation | action_hint_copy |
| action_hint_reason | 调试用生成依据 | action_hint_copy |

---

## E. Confirmation Input 接口

| 字段/接口 | 含义 | 来源 |
|-----------|------|------|
| confirmation_input_type | 离散确认类型（见 CONTRACT） | confirmation_input_bridge |
| confirmation_input_raw_text | 原始文本（注入或映射前） | confirmation_input_bridge |
| confirmation_bridge_next_effect | 推进效果（advance_to_recheck / mark_* / cancel_search 等） | confirmation_input_bridge |
| confirmation_bridge_target_flow | 目标 flow（container_check_flow / occlusion_clear_flow 等） | confirmation_input_bridge |
| confirmation_bridge_applied | 是否产生有效 next_effect | confirmation_input_bridge |

---

## F. Search 终端最小推进接口

| 字段/接口 | 含义 | 来源 |
|-----------|------|------|
| search_terminal_status | 寻物终端状态（如 found / cancelled） | object_search_interaction |
| search_can_resume_main_task | 是否可恢复主任务 | object_search_interaction |

---

## 冻结约定

- 上述字段当前可视为**稳定接口**；后续模块（含 Local Task Space Grid M0）优先复用，不得随意改名或改语义。
- 如必须修改，需在**本文档**与 **decision_monitor/CONTRACT.md** 中显式修订并注明版本/日期。

## 冻结原则补充（双层并存）

- **日志精确层与表达层双层并存**：精确事实（bbox、bearing、band、sector 等）作为主事实保留；表达层（L1/L2/Action Hint/Confirmation）仅为映射与交互，不得替代或反写底层主事实。

## Grid 轻消费约束（M0.5）

- Grid 的 human label / adjacent / followup_hint 仅用于**组合式文案补位**（如 `{原文案}（{格标签}）`），不得替代 sidecar 的 Level 1/2 表达与 Action Hint 主语义；不得进入 evidence/hypothesis/arbitration/bundle 主判断。

## Grid-driven Search Expansion 约束（M0）

- Grid-driven Search Expansion 仅为**扩搜建议层**：产出 primary/secondary cell 与 hint/reason；不得直接改 detector/recheck 执行顺序；不得接管 object_search_interaction 主状态机；仅允许以“附加建议”形式进入 next_search_step_summary / action_hint_followup。

## Grid Search Whitebox Trace 约束（M0）

- Grid Search Whitebox Trace 必须作为正式结果进入 frame/viewer/runtime_ctx/jsonl；不得仅用 print。\n- Whitebox 仅解释扩搜建议层（Reasoning/Weight/Exclusion/Interaction），不得反写 expansion 或主状态机；规则权重为显式规则分值，不是学习权重。

## Whitebox Trace Frozen Schema（统一白盒模板冻结）

- **白盒结构**属于 Phase 2 之后的稳定接口模板：统一五块骨架 `reasoning_steps` / `weight_allocation` / `exclusion_log` / `interaction_trace` / `whitebox_summary+whitebox_applied`。  
- 后续模块白盒化优先复用该结构；不得随意改名/改语义。  
- 模块特有扩展字段允许，但必须在统一骨架之下，不得绕开。  
- **详见**：docs/WHITEBOX_TRACE_SCHEMA_FREEZE_M0.md。

## Recheck Whitebox Trace（M0）

- `recheck_whitebox_trace` 属于正式白盒输出：必须进入 frame/viewer/runtime_ctx/jsonl；只解释 `recheck_planner` 结果，不得反写主逻辑或主状态机。

## Action Hint Whitebox Trace（M0）

- `action_hint_whitebox_trace` 属于正式白盒输出：必须进入 frame/viewer/runtime_ctx/jsonl；只解释 `action_hint_copy` 结果，不得反写主逻辑；必须产出**用户可见解释层**（user_visible_explanation），不得将内部 weight JSON 直出给用户。
