# 主线 2 第二阶段最终收口文档（Phase 2 Final Closure）

**文档性质**：本阶段**最终收口页**；接口冻结完成后形成稳定基线，供下一阶段（Local Task Space Grid M0）进入前提。  
**不是**：母法、单模块 delivery、roadmap、索引总表。

---

## §1 文档定位

- 本文档是主线 2 第二阶段的**最终收口页**，对当前已完成能力做统一结案与边界写死。
- **作用**：明确「本阶段完成了什么」「没完成什么」「哪些接口已冻结」「下一阶段从哪里进入」。
- **不是**：母法、单模块交付说明、后续 roadmap、能力索引总表。  
- **而是**：阶段结案 + 接口冻结前提下的稳定基线描述。

---

## §2 本阶段完成了什么

按能力域划分，不按文件堆砌。

### 2.1 真实视觉与候选层

- **静态图输入桥 M0**：单张图片进主流程（STATIC_IMAGE_INPUT_PATH / --image），与 pipeline 打通。
- **候选审计 M0**：detector/OCR 候选与 search_target 做映射审计；mapped_candidate_labels、candidate_audit_status、candidate_audit_reason。
- **真实视觉接入 M0**：YOLO11n（或 v8n/受控 demo_fallback）接入；detector_mode、detector_model_name、detector_candidate_labels、detector_probe_candidate_labels 可审计。
- **分层阈值 / probe 语义**：main 与 probe 候选分离；probe 不污染主候选语义边界。
- **TTS skip gating 同帧审计闭环**：输出与决策同帧可审计，skip 原因可追溯。

### 2.2 空间表达层

- **Spatial Expression Sidecar M0**：真实视觉候选（bbox）→ 二维相对方位表达；focus_target_expression、focus_target_debug_expression；精确坐标与 band/sector 保留于日志层。
- **Spatial Expression → Search 文案接入 M0.5**：focus_target_expression 仅接入 suggested_search_zone、next_search_step_summary；无 sidecar 时完整回退。
- **Level 2 口语化行动表达 M0**：focus_target_actionable_expression、focus_target_actionable_debug_reason；近场/桌面试点；zone/next_step 优先 Level 2。

### 2.3 Search 交互闭环层

- **Object Search Interaction M0/M1/M1.5**：子任务状态机、容器/遮挡/口袋等 flow、超时/fallback、next_search_step_summary、search_resolution_path。
- **Action Hint Copy M0**：推理→引导→确认 文案链；action_hint_primary、action_hint_followup、action_hint_confirmation。
- **Confirmation Input Bridge M0**：用户确认输入桥；离散输入类型 + 窄规则文本映射；confirmation_bridge_next_effect；mark_target_found/cancel_search 时本帧改写 search_terminal_status、search_can_resume_main_task。

### 2.4 任务编排与经验治理层

- **Task Arbitration / Bundle / Task Chain Bridge M0**：五维仲裁、merge_into_bundle 包结构、任务链可读摘要。
- **Experience / Evidence Evolution M0/M1**：经验候选聚合与治理、snapshot 多轮、不反写主策略。
- **Mainline Integration M0**：摘要消费与软控制；object_search、recheck、experience 只读进入主流程。

### 2.5 已有阶段基础能力（仍属本阶段基线）

- Skeleton Mix / Filter；Spatial Memory Pooling / Forgetting；Evidence Ledger；Hypothesis Layer；Recheck Planner；Object Temporal Ledger；LocalGoalSpatialMap / Relations / SpatialScale；Scene Gate 轻量控制与人工沟通校准。

---

## §3 当前最小闭环能力

当前已形成的**可审计交互闭环**可概括为：

1. **真实视觉候选**：detector（YOLO）产出 + 候选审计 + 目标映射。
2. **目标映射**：search_target_label 与 mapped_candidate_labels 一致时可驱动 sidecar 与 search。
3. **容器流 / 遮挡流**：interaction_flow_type、next_search_step_summary、超时/fallback 显式化。
4. **位置表达（L1/L2）**：Level 1 相对方位 + Level 2 口语化行动表达；日志层保留精确 band/sector。
5. **Action Hint**：主提示、后续提示、确认提示，按 flow 写死。
6. **Confirmation Input**：用户反馈（显式类型或窄规则映射）→ next_effect。
7. **最小推进 / 恢复**：mark_target_found → search_terminal_status=found、search_can_resume_main_task=True；cancel_search → terminal=cancelled；其余 next_effect 可审计、供下轮或下游消费。

上述闭环**不包含**：真实深度/厘米级距离、完整多轮对话引擎、动作控制/路径规划/执行器、局部环境模型/点阵图。

---

## §4 已真实化 vs 仍预留

| 类别 | 内容 |
|------|------|
| **已真实化** | 静态图输入桥与候选审计；真实 YOLO 接入与 detector_mode 可审计；分层阈值与 probe 语义边界；Sidecar M0（L1+精确日志）；Search 文案 M0.5；Level 2 口语化行动表达（近场试点）；Action Hint Copy M0；Confirmation Input Bridge M0；Search 终端最小推进（found/cancelled）；骨架/记忆/证据/假设/补证/对象账本/寻物/仲裁/桥接/经验 各 M0 基线。 |
| **仍预留** | 真实深度/厘米级距离；OCR/scene description 全链路真实化；完整多轮对话引擎；完整动作控制/路径规划/执行器；局部环境模型/点阵图/Grid；多对象全场账本、长期经验库、正式 Task Chain 主体、bundle 执行图。 |
| **明确不做（本阶段）** | 以「通过」名义声称深度/距离/对话/执行器/环境模型已完成；demo 产出作为认知真实性最终依据；绕开已冻结接口新增并行体系。 |

---

## §5 关键通过口径（写死）

以下口径为**本阶段通过**的写死表述，不得改写为“全部完成”：

| 口径 | 状态 |
|------|------|
| 真实视觉接入 M0 | 通过 |
| 目标词映射 | 通过 |
| 静态图输入桥 + 候选审计 | 通过 |
| 分层阈值 + probe | 通过 |
| TTS skip gating 同帧审计闭环 | 通过 |
| Spatial Expression Sidecar M0 | 通过 |
| Search 文案接入 M0.5 | 通过 |
| Level 2 口语化行动表达 M0 | 通过 |
| Action Hint Copy M0 | 通过 |
| Confirmation Input Bridge M0 | 通过 |

---

## §6 当前边界（必须硬写）

- **当前不代表**真实深度/厘米级距离已完成。  
- **当前不代表** OCR / scene description 全部真实化。  
- **当前不代表**完整多轮对话引擎已完成。  
- **当前不代表**完整动作控制 / 路径规划 / 执行器已完成。  
- **当前不代表**局部环境模型 / 点阵图已完成。

---

## §7 后续阶段入口

- **下一阶段默认入口**：`Local Task Space Grid M0`（或项目约定的等价入口）。
- **进入前提**：本阶段接口冻结完成（见 PHASE2_INTERFACE_FREEZE.md），CONTRACT 边界与扩展约束已生效。
- **后续新能力**不得绕开当前已冻结接口；如必须变更接口，需在 CONTRACT 与接口冻结文档中**显式修订**。

---

## §8 结论

当前已形成**「真实视觉候选 → 空间表达 → 引导 → 用户反馈 → 最小推进」的可审计交互内核**；本阶段收口与接口冻结完成后，可作为 Local Task Space Grid M0 及后续阶段的稳定基线。
