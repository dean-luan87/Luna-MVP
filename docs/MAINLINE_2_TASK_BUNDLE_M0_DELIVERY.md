# 主线 2 第二阶段：Task Bundle M0 交付说明

**依据**：Task Arbitration M0 已完成；将 merge_into_bundle 从“可合并判断”推进为“真正存在的联合任务包结构”。  
**目标**：同环境、可共享骨架与感知的任务集合用 Task Bundle 承载；不做正式执行器、不正式改 Task Chain。  
**约束**：不做 bundle 执行图、不做多 bundle 并存与调度、不做学习型合并策略、不新增大一统全局状态机。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/task_bundle.py` | **新建**。TaskBundleResult；BUNDLE_STATUSES、BUNDLE_TASK_TYPES_ALLOWED；build_task_bundle(task_arbitration, state, skeleton_mix, local_goal_spatial_map, object_search_interaction, recheck_planner, object_temporal_ledger, incoming_*, frame_seq)；仅当 arbitration_action==merge_into_bundle 时生成；共享焦点/zone/骨架/原因；阻断规则。 |
| `decision_monitor/schema.py` | 引入 TaskBundleResult；DecisionMonitorFrame 新增 task_bundle。 |
| `decision_monitor/builder.py` | 引入 task_bundle；在 task_arbitration 之后调用 build_task_bundle，写入 frame.task_bundle。 |
| `runtime/context.py` | 新增 current_task_bundle_id、current_task_bundle_zone、current_task_bundle_tasks、current_task_bundle_focus、current_task_bundle_status、current_task_bundle_applied。 |
| `main.py` | 写回 task_bundle 各字段到 runtime_ctx。 |
| `tools/decision_monitor_viewer.py` | 新增「联合任务包 / Task Bundle (M0)」卡片；sections 增加 task_bundle。 |
| `decision_monitor/CONTRACT.md` | 补充 task_bundle 说明与未实现项。 |
| `docs/MAINLINE_2_TASK_BUNDLE_M0_DELIVERY.md` | **新建**。本文档。 |

---

## 2. TaskBundle 数据结构说明

### TaskBundleResult

| 字段 | 类型 | 含义 |
|------|------|------|
| bundle_id | str | 当帧生成的 bundle 标识（如 bundle_123） |
| bundle_zone | str | 包对应区域摘要 |
| bundle_task_types | List[str] | 合并的任务类型（去重，最多 6 个） |
| bundle_dominant_skeleton | str | 主导骨架（来自 skeleton_mix） |
| bundle_shared_focus | str | 共享焦点摘要（smap/搜索区/候选/容器/incoming_zone） |
| bundle_reason | str | 合并原因（同环境/共享搜索区/共享容器/近场复核/路径锚点等） |
| bundle_status | str | proposed / active / blocked / closed |
| bundle_created | bool | 本帧是否真正创建了 bundle |
| bundle_applied | bool | 是否已应用（阻断时为 False） |
| bundle_block_reason | str | 阻断原因（若有） |

---

## 3. bundle 生成规则说明

- **前提**：仅当 task_arbitration.arbitration_action == merge_into_bundle 时允许生成；否则 bundle_created=False，bundle_status=closed。  
- **同环境合并**：environment_overlap_level==high 且 arbitration 已为 merge_into_bundle 时，收集当前 foreground_task_type、incoming_task_type、candidate_task_types，去重后写入 bundle_task_types（仅允许 object_search、recheck、observation、navigation、interaction_confirm、safety_guard），最多 6 个。  
- **共享骨架**：bundle_dominant_skeleton = skeleton_mix.dominant_skeleton。  
- **共享焦点**：从 local_goal_spatial_map.focus_region/confirm_region 摘要、object_search_interaction.suggested_search_zone、object_temporal_ledger.current_candidate_location/current_container_candidate、incoming_task_zone 择一或组合成 bundle_shared_focus；bundle_zone 取 incoming_task_zone 或 suggested_search_zone 或 focus 摘要。  
- **bundle_reason**：至少包含“同环境任务合并”，并可追加共享搜索区域、共享容器候选、共享近场复核、共享路径段/锚点。  

---

## 4. bundle 阻断规则说明

- 当 minimum_mode_active、runtime_domain_state==frozen、scene_gate_action==freeze_to_minimum_mode、high_level_output_suppressed、human_check_pending 任一为真，或 arbitration_action != merge_into_bundle 时：  
  - 若不满足合并前提：bundle_created=False，bundle_status=closed。  
  - 若满足合并但守底阻断：bundle_applied=False，bundle_status=blocked，bundle_block_reason 写明原因；可不生成有效 bundle_id 或仍生成占位。  
- 当前实现：阻断时直接返回 bundle_created=False 或 status=blocked 的 TaskBundleResult，不写入 active/applied。  

---

## 5. 最小 bundle 执行效果说明

- 不做真正执行图；仅做“系统承认 bundle 存在”的运行事实：  
  - frame.task_bundle 写入；  
  - runtime_ctx 写入 current_task_bundle_id、current_task_bundle_zone、current_task_bundle_tasks（逗号分隔）、current_task_bundle_focus、current_task_bundle_status、current_task_bundle_applied；  
  - Viewer 展示当前 bundle；  
  - 若 bundle_applied=True，shared focus/zone 可供后续执行层引用。  

---

## 6. Viewer 展示说明

- 卡片标题：联合任务包 / Task Bundle (M0)。  
- 展示：bundle_id、bundle_zone、bundle_task_types、bundle_dominant_skeleton、bundle_shared_focus、bundle_reason、bundle_status、bundle_created、bundle_applied、bundle_block_reason。  
- sections 可展开 task_bundle 查看全部字段。  

---

## 7. 样本运行结果

- **arbitration_action != merge_into_bundle** → bundle_created=False，bundle_status=closed。  
- **arbitration_action == merge_into_bundle 且无守底阻断** → bundle_created=True，bundle_status=active，bundle_applied=True，bundle_task_types 非空，bundle_shared_focus/bundle_reason 有值。  
- **merge_into_bundle 但 minimum_mode_active** → bundle_applied=False，bundle_status=blocked，bundle_block_reason 有值。  

---

## 8. 真实化与预留

| 项目 | 状态 |
|------|------|
| TaskBundleResult 全字段、仅 merge 时生成、共享焦点/zone/骨架/原因、阻断规则、Viewer、runtime_ctx | **真实化** |
| bundle 执行图、正式改 Task Chain、多 bundle 并存与调度、学习型合并策略、数据库/持久化 | **未实现**（本轮不做） |

---

## 9. 验收与本轮是否通过

- **验收**：运行时存在可读 Task Bundle；仅 arbitration_action==merge_into_bundle 时真正生成 bundle；bundle 能表达合并任务类型、zone/focus、主导骨架、合并原因；守底阻断时不标 active/applied；Viewer 能展示；不破坏既有链路。  
- **本轮是否通过**：实现与文档满足上述要求即通过。
