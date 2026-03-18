# 主线 2 第二阶段统一收口文档

**主线名称**：主线 2 — 目标驱动的时空状态内核  
**阶段**：第二阶段（局部空间结构化 → 证据—假设—补证 → 对象时空与寻物 → 任务编排 → 经验治理）  
**收口范围**：M0 / M1 / M1.5 / M2 及相关子主线  
**结论**：**阶段性收口**。当前已形成局部认知运行内核，可审计、可回顾、可继续扩展。

---

## 1. 文档定位

- 本文档用于对「主线 2 第二阶段」进行**统一收口**，对当前已完成的全部能力做系统级结案。
- 这是**阶段性收口**，不是项目最终完成；其作用是把分散的 M0 / M1 / M1.5 / M2 及相关子主线整理成可审计、可回顾、可继续扩展的**阶段基线**。
- **不是**：母法、索引总表、后续 roadmap。  
- **而是**：「当前阶段完成了什么」的**统一结案页**。

---

## 2. 本阶段目标回顾

主线 2 第二阶段的总体目标是：从**局部空间状态**出发，逐步构建一套可运行、可观测、可扩展的**局部认知运行内核**，包括：

- **局部空间结构**：将当前目标下的空间事实结构化（四类区域、标尺、关系），而不是裸感知堆砌。
- **骨架与空间治理**：用骨架组合制组织当前帧的感知偏好，并做过滤、短时记忆与遗忘治理。
- **证据—假设—补证链**：在空间与骨架基础上形成最小证据账本、受约束假设候选与补证执行入口，形成可解释的推理闭环。
- **对象级时空与寻物**：单对象时空账本（最后可信与当前候选分离、最小容器逻辑）与交互式寻物子任务流（药盒范式：多轮 flow、超时/回退、下一步建议链）。
- **任务编排与桥接**：任务仲裁、联合任务包、任务链摘要桥接，使上层能读懂当前编排结果。
- **经验演化治理**：对经验候选做聚合、审计与约束，区分能力进化与幸运污染，不反写主策略。

上述能力均以「规则型 + 最小闭环」落地，不引入学习系统、不跨会话持久化、不正式改 Task Chain 主体。

---

## 3. 本阶段已完成能力总览

按主线能力分组，不按时间流水账。

### 3.1 空间结构与标尺能力

| 能力 | 版本 | 当前能做什么 | 已真实化程度 | 仍未做 |
|------|------|----------------|----------------|--------|
| **LocalGoalSpatialMap** | M0 / M1 / M1.5 | 四类区域（focus / traversable / risk / confirm）top-k、priority_rank、stability_score；宪法标尺层：方向扇区仅用 BASE_SECTORS，近场由 sector=front + distance_band 组合；relative_bearing_deg、distance_cm、staleness_ms、distance_band、offset_band、scene_profile | 区域与标尺规则型生成并写入 frame / runtime_ctx；Viewer 展示 | 3D、全局地图、长时空间记忆、复杂空间推理 |
| **LocalGoalSpatialRelations** | M2 | 区域关系最小版：adjacent_to、overlaps_with、supports、conflicts_with；规则型从扇区与距离带生成 | 关系列表写入 frame；供证据/假设/分池引用 | 复杂拓扑、长期关系图 |
| **SpatialScale** | M1.5 | scene_profile、effective_body_width_cm、effective_body_height_cm、clearance_required_cm、forward_speed_cm_s、speed_band、reaction_horizon_ms | 用户包络与速度标尺写入 frame；宪法最小接入 | 平滑速度闭环、复杂标尺策略 |

### 3.2 骨架与空间治理能力

| 能力 | 版本 | 当前能做什么 | 已真实化程度 | 仍未做 |
|------|------|----------------|----------------|--------|
| **Skeleton Mix** | M0 | 当前帧骨架配比（navigation / fine_interaction / observation / safety）、四权重与 floor、dominant_skeleton、mix_reason；由 goal_type、scene、minimum_mode、goal_progress_paused、runtime_domain 等规则型推导 | frame.skeleton_mix 与 runtime_ctx 写入；Viewer 展示 | 学习型权重、多骨架竞争 |
| **Skeleton Filter** | M0 | keep_region_types、suppress_region_types、granularity_bias、filter_reason；由 skeleton_mix 规则型生成 | frame.skeleton_filter 与 runtime_ctx 写入；供记忆/证据/假设引用 | 对象级复杂过滤、与 detector/OCR 主链联动 |
| **Spatial Memory Pooling** | M0 | 四层空间记忆池（working / episode / stable / anchor）；SpatialMemoryItem 与分池规则；working/episode 为主，stable/anchor 占位 | frame.spatial_memory_pools 与 runtime_ctx 摘要写入；Viewer 展示 | 数据库/持久化、Value Decay、Evidence Replacement、与 Hypothesis 联动 |
| **Spatial Forgetting** | M0 | working 按 TTL 过期；episode 按 Task-End/上下文切换 collapse 或最小时间过期；forgetting_reason_summary、forgetting_actions_applied | frame.spatial_forgetting 与 runtime_ctx 写入 | Value Decay、Stable/Anchor 长期遗忘、学习型策略 |

### 3.3 证据—假设—补证链

| 能力 | 版本 | 当前能做什么 | 已真实化程度 | 仍未做 |
|------|------|----------------|----------------|--------|
| **Evidence Ledger** | M0 | 1～3 条 claim（主导空间关注、主要空间结构、记忆状态）；supporting/conflicting/missing_evidence、evidence_confidence、risk_if_wrong、suggested_next_check；从 smap、relations、mix、filt、pools、forgetting、goal、state 规则型生成 | frame.evidence_ledger 与 runtime_ctx 首条摘要；Viewer 展示 | 完整候选推理、学习型证据权重、长期证据账本 |
| **Hypothesis Layer** | M0 | 1～3 条受约束候选（path_continuation、interaction_target、occluded_object、container_candidate）；hypothesis_confidence、verification_hint、hypothesis_status；风险闸门：safety 主导或 runtime_domain  degraded/frozen 时不得 promoted | frame.hypothesis_layer 与 runtime_ctx 首条写入；Viewer 展示 | 学习型假设排序、长期 hypothesis ledger、开放世界无限候选 |
| **Recheck Planner** | M0 | 从 hypothesis 首条 verification_hint 或 evidence 首条 suggested_next_check 生成 recheck_action/recheck_reason/recheck_target；阻断条件与主循环一致；recheck_environment/recheck_close_range 对接 local_goal_recheck_mode/type | frame.recheck_planner 与 runtime_ctx 写入；主循环具备一次性 force_sample 执行入口 | 多步 planner、学习型补证策略、完整对象级主动搜索 |

### 3.4 对象级时空与寻物能力

| 能力 | 版本 | 当前能做什么 | 已真实化程度 | 仍未做 |
|------|------|----------------|----------------|--------|
| **Object Temporal Ledger** | M0 / M1 / M1.5 | 单对象优先；last_confirmed_* 与容器候选分离；最小容器逻辑（容器打开/关闭/对象进入候选）；用户确认/否认写回；LedgerEvent 与 ledger_state_summary | frame.object_temporal_ledger 与 runtime_ctx 写入；Viewer 展示最后可信/当前候选/容器状态 | 多对象全场账本、复杂 re-id、持久化、复杂容器视觉识别 |
| **Object Search Interaction** | M0 / M1 / M1.5 | 子任务状态机、用户回复注入、结果分级；M1.5：interaction_flow_type（container/occlusion/pocket/last_location/description_bootstrap）、超时/fallback、next_search_step_summary、search_resolution_path；三类典型流显式化 | frame.object_search_interaction 与 runtime_ctx 同步；Viewer 展示 flow/timeout/fallback/path | 完整对话管理器、开放世界搜索、多对象并发寻物、正式并入 Task Chain |

### 3.5 任务编排与经验治理能力

| 能力 | 版本 | 当前能做什么 | 已真实化程度 | 仍未做 |
|------|------|----------------|----------------|--------|
| **Task Arbitration** | M0 | 五维规则型判断（风险、环境重合、资源冲突、用户打扰、当前主任务）；arbitration_action（preempt/interrupt_then_resume/merge_into_bundle/run_in_background/defer/continue_current）；foreground_task_type 与模块映射 | frame.task_arbitration 与 runtime_ctx 写入；Viewer 展示 | 完整意图池、多任务执行器、正式改 Task Chain |
| **Task Bundle** | M0 | 仅当 arbitration_action==merge_into_bundle 时生成；bundle_task_types、bundle_dominant_skeleton、bundle_shared_focus、bundle_reason；守底阻断时 bundle_applied=False | frame.task_bundle 与 runtime_ctx 写入；Viewer 展示 | bundle 执行图、多 bundle 并存与调度、学习型合并策略 |
| **Task Chain Bridge** | M0 | 将 arbitration/bundle/object_search 映射为任务链可读状态（active/paused/waiting_user/blocked/bundled/done/cancelled）；task_chain_foreground_summary、task_chain_can_resume、task_chain_summary_text 等 | frame.task_chain_bridge 与 runtime_ctx 写入；Viewer 展示 | 正式改 Task Chain 主体、task dispatcher、完整任务恢复器 |
| **Experience / Evidence Evolution** | M0 / M1 | M0：经验候选审计（单次成功不升格、fallback/否认过多 blocked/rejected）；M1：同类聚合（experience_group_key、aggregated_source_paths、repeated_pattern_count）、contradiction_sources、evolution_confidence_band、future_use_scope、审计报告式 reason；snapshot_for_next 供下一帧聚合 | frame.experience_evolution 与 runtime_ctx 首条摘要写入；Viewer 展示 | 长期经验库、自动策略更新、跨会话沉淀、经验层反写主策略 |

---

## 4. 当前系统链路（文字版）

当前阶段已形成的认知运行链可概括为六层，构成**局部认知运行内核**（仍不是完整世界模型）：

1. **空间事实层**：LocalGoalSpatialMap、LocalGoalSpatialRelations、SpatialScale 提供当前目标下的局部空间结构化表达与标尺约束；方向与距离带遵守标尺宪法，不引入未定义扇区。
2. **结构治理层**：Skeleton Mix / Filter 决定当前帧的骨架组合与感知过滤偏好；Spatial Memory Pooling 与 Spatial Forgetting 对短时记忆做分池与遗忘治理，为证据与假设提供稳定输入边界。
3. **证据推理层**：Evidence Ledger 产出少量 claim 与 suggested_next_check；Hypothesis Layer 产出受约束的候选解释与 verification_hint；Recheck Planner 将补证建议转为可执行入口（一次性 force_sample），形成最小证据—假设—补证闭环。
4. **对象任务层**：Object Temporal Ledger 维护单对象最后可信与当前候选、最小容器逻辑；Object Search Interaction 在目标不清/有容器/有遮挡/口袋等场景下驱动多轮交互流，产出 resolution_path、next_search_step_summary、超时与 fallback，支撑「药盒范式」。
5. **任务编排层**：Task Arbitration 做五维判断并产出 arbitration_action；Task Bundle 仅在 merge_into_bundle 时生成联合任务包；Task Chain Bridge 将编排结果映射为任务链可读的 state/substate/foreground/can_resume，供上层统一读取。
6. **经验治理层**：Experience Evolution 对经验候选做来源聚合、支撑/冲突/回退统计、watchlist/promotable/blocked/rejected 判定与 evolution_confidence_band、future_use_scope 约束；单次成功不升格、多次支撑+用户确认才可能 promotable；不反写 hypothesis/object_ledger/recheck，仅产出治理摘要与 snapshot_for_next。

上述链路在运行时通过 DecisionMonitorFrame 与 runtime_ctx 可见，Viewer 可展示各层结果，相关单测覆盖关键路径且未破坏主线。

---

## 5. 本阶段「已真实化」与「仍预留」的边界

### 已真实化（概括）

- 局部空间结构化（四类区域、标尺、关系）并进入 frame / runtime_ctx。
- 骨架组合制进入运行时（mix/filter），过滤、记忆分池与遗忘最小闭环。
- 证据账本、假设层、补证规划最小闭环，且补证具备一次性执行入口。
- 单对象时空账本与最小容器逻辑，用户确认/否认写回。
- 交互式寻物任务流最小版（子任务状态机、三类 flow、超时/fallback、resolution_path、next_search_step_summary）；Spatial Expression → Search 文案 M0.5：sidecar 位置短语仅接入文案层（suggested_search_zone、next_search_step_summary），不做距离与动作控制。
- 任务仲裁、联合任务包、任务链桥接，且桥接结果可被上层读取。
- 经验候选治理（聚合、contradiction_sources、confidence_band、future_use_scope、审计式 reason、snapshot 多轮聚合）。

### 仍预留（明确未做）

- 全局地图、3D 世界模型、长时空间记忆。
- 多对象全场账本、复杂 re-id、持久化。
- 长期经验库、自动策略更新、学习型编排、跨会话经验沉淀。
- 正式 Task Chain 主体改造、多任务执行器、bundle 执行图、多 bundle 并存与调度。
- 开放世界搜索、完整对话管理器、多对象并发寻物。
- Value Decay、Evidence Replacement 完整版、stable/anchor 深化、学习型假设排序、多步 recheck planner。
- 经验层反写主策略（除非单独修法）。

以上边界必须清晰，防止后续误判已完成范围。

---

## 6. 当前阶段通过判定理由

主线 2 第二阶段可以判定为「阶段性收口」的理由包括：

- **关键链路已闭合**：从空间事实 → 骨架与记忆治理 → 证据—假设—补证 → 对象时空与寻物 → 任务编排 → 经验治理，各层均有产出并写入 frame 与 runtime_ctx，且层间依赖仅读已有结果、不凭空引入新主感知源。
- **运行时可见、Viewer 可见、runtime_ctx 可见**：决策显示器每关键周期产出一帧；各模块结果可在 Viewer 中按卡片与 sections 展开；runtime_ctx 承载首条/摘要字段供主循环与下游引用。
- **相关单测未破坏主线**：decision_monitor 及相关单测覆盖 LocalGoalState、空间图、骨架、记忆、证据、假设、补证、对象账本、寻物、仲裁、bundle、桥接、经验演化等，通过且不破坏既有行为。
- **已形成可继续扩展的局部认知运行内核**：当前结构支持在「不推翻现有层」的前提下，以新增层或增强层方式扩展（如 Task Chain 主体对接、Object Search M1.5 深化、Experience 持久化等）。
- **再继续扩模块会边际递减，应先收口**：本阶段已落地的模块数量与契约边界足够支撑下一轮「在基线上增强」而非「另起一套宇宙」的推进方式。

---

## 7. 当前主线状态表

| 模块 / 阶段 | 状态词 | 说明 |
|-------------|--------|------|
| LocalGoalSpatialMap M0 / M1 / M1.5 | 通过 | 区域与标尺规则型生成，宪法标尺层接入 |
| LocalGoalSpatialRelations M2 | 通过 | 区域关系最小版 |
| Skeleton Mix M0 | 通过 | 骨架配比进入 frame / runtime_ctx |
| Skeleton Filter M0 | 通过 | 过滤策略进入 frame / runtime_ctx |
| Spatial Memory Pooling M0 | 通过 | 四层分池，working/episode 为主 |
| Spatial Forgetting M0 | 通过 | working TTL + episode collapse/过期 |
| Evidence Ledger M0 | 通过 | 最小证据账本与 suggested_next_check |
| Hypothesis Layer M0 | 通过 | 受约束假设候选与 verification_hint |
| Recheck Planner M0 | 通过 | 最小补证执行入口 |
| Object Temporal Ledger M0 / M1 / M1.5 | 通过 | 单对象、last_confirmed 与容器候选分离 |
| Object Search Interaction M0 / M1 / M1.5 | 通过 | 子任务状态机、flow/timeout/fallback/path |
| Spatial Expression → Search 文案 M0.5 | 通过 | 仅表达接入：suggested_search_zone/next_search_step_summary 用 sidecar 位置短语增强；不做距离与动作控制 |
| Level 2 口语化行动表达 M0 | 通过 | 近场试点：focus_target_actionable_expression + debug_reason；zone/next_step 优先 Level 2；日志层保留精确字段 |
| Action Hint Copy M0 | 通过 | 推理→引导→确认 文案链；主/后续/确认提示；仅表达层，不做动作控制 |
| Confirmation Input Bridge M0 | 通过 | 用户确认输入桥；离散类型+窄规则映射；按 flow 最小推进；mark_target_found/cancel_search 本帧改写终端态 |
| Task Arbitration M0 | 通过 | 五维仲裁与 arbitration_action |
| Task Bundle M0 | 通过 | merge_into_bundle 时生成包结构 |
| Task Chain Bridge M0 | 通过 | 任务链可读摘要 |
| Experience / Evidence Evolution M0 / M1 | 通过 | 经验候选聚合与治理、snapshot 多轮 |
| 主线 A | 已收口 | Scene Gate 轻量控制与人工沟通校准 |
| 主线 2 第一阶段 | 已收口 | LocalGoalState、recheck 执行、观察优先级 |
| 主线 2 第二阶段 | 已收口 | 本阶段基线如本文档所述 |
| 三大宪法（标尺/骨架/记忆） | 冻结 | 后续实现不得绕开 |

---

## 8. 结论

- 主线 2 第二阶段已形成**局部认知运行内核**：从局部空间结构、骨架与记忆治理、证据—假设—补证、对象时空与寻物、任务编排到经验治理，形成一条可运行、可观测、可审计的认知运行链。
- 当前能力已足以支撑后续更高层扩展（如 Task Chain 主体对接、寻物/经验深化、持久化等），且扩展应建立在本阶段基线上。
- 后续推进应**建立在本阶段收口文档与 CONTRACT 之上**，不应绕开或推翻当前结构；新增能力以「新增层」或「增强层」方式推进，避免另起一套编排或推理宇宙。
- **后续推进原则**：后续扩展应优先采用「增强已有层 / 新增受约束层」的方式推进，不得绕开当前阶段已形成的运行内核另起并行体系。
