# 决策显示器 6 层数据契约

主线 1：目标驱动的感知—理解—决策—行动链 + 决策显示器。  
本模块为开发态「真相窗」，不做复杂 UI；每关键周期产出一条 `DecisionMonitorFrame`。

## 统一结构 DecisionMonitorFrame

- **goal**：目标层
- **inputs**：输入层
- **state**：理解/状态层
- **decision**：决策层
- **outputs**：输出层
- **consequence**：后果评估层
- **local_goal_state**：主线 2.0 局部时空状态图（可选）
- **monitor_version**：契约版本
- **trace_anchor_id**：与现有 trace 对齐用（如 `frame_123`）

## 各层最小字段

| 层 | 字段 |
|----|------|
| **goal** | goal_id, goal_type, goal_description, goal_source, goal_priority, goal_confidence, goal_status, subgoal_description, goal_switch_reason |
| **inputs** | frame_seq, produced_ts, current_ts, delta_t_ms, sampled, route, active_b2_impact, raw_observation_summary, goal_relevant_observations, sensor_notes |
| **state** | c1_state, motion, diff, risk_score, safety_level, weak_evidence_level, traversability_state, local_risk_summary, goal_progress_state, state_confidence, state_notes, **prev_state_summary**, **state_delta_summary**, **state_trend**, **goal_progress_delta**（1.3）, **view_guard 十字段**（1.3A）, **predictive_hold_***（1.3B）, **runtime_domain_state**, **runtime_domain_confidence**, **domain_mismatch_detected**, **domain_mismatch_reason**, **cognitive_degrade_level**, **cognitive_output_allowed**, **degrade_action**, **recovery_condition**（1.3C）, **scene_type**, **scene_supported**, **scene_gate_state**, **scene_gate_reason**, **scene_gate_action**（Scene Gate v1）, **goal_progress_paused**, **minimum_mode_active**, **high_level_output_suppressed**, **scene_gate_control_applied**（Scene Gate 轻量控制）, **human_check_needed/reason/question/blocking_level/timeout_ms/default_action/response/resolved/pending/timeout_triggered**（人工沟通校准） |
| **decision** | decision_id, for_goal_id, decision_owner, decision_type, decision_reason, policy_mode_before, policy_mode_after, b2_impact_applied, escape_hatch_triggered, floor_forced, decision_confidence |
| **outputs** | policy_intent_summary, sampling_target_fps, detector_stride, ocr_stride, modules_run, modules_skipped, action_summary, user_facing_output, output_notes |
| **consequence** | expected_gain, expected_cost, expected_risk, consequence_confidence, evaluation_horizon_ms, rollback_hint, post_action_check_needed |

## 最后拍板者 decision_owner

- **floor_guard**：守底/escape hatch 触发
- **sampling_gate**：本帧被采样门跳过
- **b2_impact**：B2 impact 本帧生效（档位上调）
- **controller**：其余由 controller 拍板

## 输出方式

- **JSONL**：`DECISION_MONITOR_JSONL_PATH`（默认 `logs/decision_monitor.jsonl`）
- **终端摘要**：`DECISION_MONITOR_CONSOLE=1`，间隔 `DECISION_MONITOR_CONSOLE_INTERVAL`（默认 10 帧）

## 启用

- `DECISION_MONITOR_ENABLED=1` 时在 main 主循环中每关键周期产出一帧并写入 JSONL / 终端。

## 当前字段来源（真实 vs 占位）

| 来源 | 真实接入 | 占位 |
|------|----------|------|
| 主循环 / obs | frame_seq, current_ts, delta_t_ms, sampled, motion, path, branch, raw_observation_summary | — |
| policy_intent | policy_mode_before/after, sampling_target_fps, detector_stride, ocr_stride, b2_impact_applied | — |
| gate / floor | policy_should_sample, policy_run_detector/ocr, detector/ocr_floor_due, escape_hatch_fired | — |
| decision / risk | risk_score, safety_level | — |
| B2 | active_b2_impact, weak_evidence_level | — |
| **goal** | **goal_resolver**：goal_type, goal_description, subgoal_description, goal_status, goal_switch_reason（规则：floor_forced→hold_for_floor；b2_impact→slow_down_observe；sampled+detector/ocr→run_*_check；默认 observe_navigate） | goal_id/goal_source 等仍可扩展 |
| **consequence** | **consequence_evaluator**：expected_gain/cost/risk, consequence_confidence, rollback_hint, post_action_check_needed（规则：守底/B2/controller 采样/节流跳过） | evaluation_horizon_ms 固定 500 |
| **state 连续化** | **state_tracker**：prev_state_summary, state_delta_summary, state_trend（stable/improving/worsening/shifting/recovering）, goal_progress_delta；上一帧镜像 + 规则型差分与趋势 | 首帧无上一时刻，占位「首帧，无上一时刻」/「—」 |
| **state View Guard（1.3A）** | **view_guard**：view_alignment_state/score, view_misaligned, view_correction_needed/hint；vision_quality_state, vision_reliability_score, vision_degraded, vision_degrade_reason（occluded/blur/shake/no_forward_view）, vision_recovery_eta_ms；规则：frame_quality/view_confidence/occlusion_ratio/motion_instability → 退化判定 | 视线对齐依赖 ctx.forward_view_valid，无则 assumed_ok；无视觉信号时默认 good/1.0 |
| **state Predictive Hold（1.3B）** | **predictive_hold**：predictive_hold_allowed/active, predictive_hold_remaining_ms, predictive_hold_reason/confidence, predictive_hold_expired, predictive_recovery_action（recheck_environment/force_sample/freeze_to_minimum_mode）；规则：仅当 view_misaligned=False、vision_degraded=True、recovery_eta≤1500ms、state_trend=stable、风险低、无 floor/B2 触发时允许；超时后强制恢复动作 | 最大窗口 1500ms；恢复动作先只支持 recheck_environment |
| **state Runtime Domain Guard（1.3C）** | **runtime_domain_guard**：runtime_domain_state（normal/degraded/frozen）, runtime_domain_confidence, domain_mismatch_detected, domain_mismatch_reason（view_misaligned/vision_unusable/high_rotation_or_abnormal_motion）, cognitive_degrade_level（none/low/high）, cognitive_output_allowed, degrade_action（warn_user/recheck_environment/freeze_to_minimum_mode）, recovery_condition；规则：view_misaligned/vision_unusable/motion_instability≥阈值 → 失配；invalid 或极高运动 → frozen | 运动异常依赖 ctx.motion_instability |
| **state Scene Gate v1** | **scene_gate**：scene_type（normal_walk_navigation/stationary_observation/close_range_check/cautious_navigation/unsupported_motion_context/unsupported_view_context/unknown_context）, scene_supported, scene_gate_state（open/cautious/suspended）, scene_gate_reason, scene_gate_action（continue_normal/continue_cautious/pause_goal_progress/ignore_high_level_input/freeze_to_minimum_mode）；规则：吃 runtime_domain_guard 结果，非支持域挂起、不接高层输入 | 若当前场景属于已知非支持域，系统不再接受该场景的高层输入进入正常理解链 |
| **state Scene Gate 轻量控制 + 人工沟通校准（主线 A 收口）** | **builder**：根据 scene_gate_action 写 goal_progress_paused, minimum_mode_active, high_level_output_suppressed, scene_gate_control_applied；pause/freeze 时 goal_status=paused。**interaction_calibrator**：三类触发（Scene Gate 将 pause/freeze 且非硬证据；view_guard 长期偏航；runtime_domain degraded）产出 human_check_*；needed 且无回复时暂缓高代价动作。**main**：每帧写 state→runtime_ctx；超时则 check_timeout_and_apply_default 写 default_action；resolved 后清理。**runtime.gates.should_advance_goal**：goal_progress_paused=True 时主循环跳过 SPEAK 推进并打 log goal_progress_skipped_by_scene_gate | 超时默认动作与用户回复共用同一消费路径；Viewer 可区分超时执行与用户回复 |
| **local_goal_state（主线 2.0）** | **local_goal_state_builder**：从 goal/state/inputs/outputs/consequence 汇聚；goal_focus_region（前向观测区/路径确认区/近场检查区）, goal_progress_state, primary_view_direction, traversable_region_summary, next_best_action 等；第一版仅支持 observe_navigate/confirm_path/close_range_check | 不做全局地图/长时记忆/复杂对象追踪；仅围绕当前目标的短时局部状态 |
| **local_goal_spatial_map（主线 2 第二阶段）** | **M0**：四类区域（focus/traversable/risk/confirm）各 top-1，字段：region_type/sector/confidence/reason/ttl_ms。**M1**：top-k（1~3）、priority_rank、stability_score。**M1.5**：宪法标尺层接入——方向扇区仅用 **BASE_SECTORS**（front/front_left/front_right/left/right/rear），**不得**将 near_front 作为基础扇区；近场由 sector=front + distance_band=immediate/near 组合。每区域新增：relative_bearing_deg、distance_cm、staleness_ms、distance_band、offset_band；LocalGoalSpatialMap 新增 scene_profile（outdoor/indoor）。**spatial_scale**（M1.5）：scene_profile、effective_body_width_cm、effective_body_height_cm、clearance_required_cm、forward_speed_cm_s、speed_band、reaction_horizon_ms；用户包络默认宽度 70cm，高度可默认 profile；速度优先使用平滑后值（当前可占位）。**local_goal_spatial_relations**（**M2**）：区域关系最小版；SpatialRelation：source_region_type、source_priority_rank、target_region_type、target_priority_rank、relation_type（adjacent_to/overlaps_with/supports/conflicts_with）、confidence、reason；规则型生成：adjacent_to（扇区邻接+距离带接近）、overlaps_with（同扇区同/近带）、supports（confirm→focus、traversable→goal）、conflicts_with（risk vs traversable、risk vs focus/confirm）。**skeleton_mix**（**Skeleton Mix M0**）：当前帧骨架配比；SkeletonMix：navigation_weight、fine_interaction_weight、observation_weight、safety_weight、四类 floor（safety_floor≥0.15）、dominant_skeleton、mix_reason；由 goal_type、scene_type、scene_profile、minimum_mode_active、goal_progress_paused、high_level_output_suppressed、runtime_domain_state 规则型推导；frame.skeleton_mix 与 runtime_ctx 写入；Viewer 展示。**skeleton_filter**（**骨架过滤 M0**）：SkeletonFilterResult：keep_region_types、suppress_region_types、keep_anchor_priority、suppress_detail_level、granularity_bias、filter_reason；由 skeleton_mix（dominant + 四权重）规则型生成；Navigation/Fine Interaction/Observation/Safety 主导时保留与压低偏好不同；frame.skeleton_filter 与 runtime_ctx 写入；Viewer 展示。当前过滤仅作用于空间结构保留策略，不直接控制 detector/OCR。**spatial_memory_pools**（**骨架记忆分池 M0**）：四层空间记忆池（working_memory_items、episode_memory_items、stable_memory_items、anchor_memory_items）；SpatialMemoryItem：memory_layer、source_type、payload_summary、skeleton_context、retention_policy、timestamp、confidence 等；由 skeleton_mix、skeleton_filter、local_goal_spatial_map、local_goal_spatial_relations、goal 规则型分池；working/episode 为主，stable/anchor 当前仅占位；suppress 内容不进入 stable/anchor；frame.spatial_memory_pools 与 runtime_ctx 摘要写入；Viewer 展示。**spatial_forgetting**（**空间遗忘 M0**）：SpatialForgettingSummary：working_expired_count、episode_collapsed_count、episode_expired_count、forgetting_reason_summary、forgetting_actions_applied；Working 按 TTL 过期移除；Episode 按 Task-End/上下文切换 collapse 或按最小时间过期；Stable/Anchor 不做复杂遗忘（预留）；frame.spatial_forgetting 与 runtime_ctx 写入；Viewer 展示。当前仅完成 working TTL + episode task-end collapse + episode 最小过期；未实现 Value Decay、Evidence Replacement、stable/anchor 长期遗忘、学习型 forgetting policy。**evidence_ledger**（**证据账本 M0**）：EvidenceLedger（entries: List[EvidenceLedgerEntry]）；EvidenceLedgerEntry：claim_summary、supporting_evidence、conflicting_evidence、missing_evidence、evidence_confidence、risk_if_wrong、suggested_next_check；从 smap、relations、mix、filt、pools、forgetting、goal、state 规则型生成 1～3 条 claim（主导空间关注、主要空间结构、记忆状态）；支持/冲突/缺失证据与 suggested_next_check 规则型填充；frame.evidence_ledger 与 runtime_ctx 首条 claim 摘要写入；Viewer 展示。当前仅做最小证据账本；未实现完整候选推理、Hypothesis Layer、学习型证据权重、长期证据账本持久化。**hypothesis_layer**（**假设层 M0**）：HypothesisLayer（hypotheses、dominant_hypothesis_type、hypothesis_reason_summary）；Hypothesis：hypothesis_summary、hypothesis_type、supporting_evidence_refs、missing_evidence、hypothesis_confidence、risk_if_wrong、verification_hint、hypothesis_status（candidate/needs_check/rejected/promoted）；仅从 evidence_ledger、smap、relations、mix、filt、pools 生成 1～3 条受约束候选（path_continuation_candidate、interaction_target_candidate、occluded_object_candidate、container_candidate）；风险闸门：dominant==safety 或 runtime_domain 为 degraded/frozen 时不得 promoted，verification_hint 必填；frame.hypothesis_layer 与 runtime_ctx 首条写入；Viewer 展示。当前仅做最小候选解释层；未实现学习型假设排序、长期 hypothesis ledger、假设升级为事实的完整流程、经验沉淀联动。**recheck_planner**（**补证规划 M0**）：RecheckPlannerResult：recheck_action、recheck_reason、recheck_target、recheck_priority、recheck_blocked、recheck_block_reason、recheck_applied；从 hypothesis_layer 首条 verification_hint 或 evidence_ledger 首条 suggested_next_check 生成；阻断条件：minimum_mode_active、runtime_domain_state==frozen、scene_gate_action==freeze_to_minimum_mode、high_level_output_suppressed、human_check_pending；未阻断时 recheck_environment/recheck_close_range 对接 local_goal_recheck_mode/type，look_forward/shift_view_* 写入 view_behavior_hint；frame.recheck_planner 与 runtime_ctx 写入；Viewer 展示。当前仅做最小补证执行入口；未实现复杂多步规划、学习型补证策略、经验反馈调 planner、完整对象级主动搜索。**object_temporal_ledger**（**对象时空账本 M0/M1.5**）：**M1.5**：ObjectTemporalLedger（focus_object_entry、events、ledger_reason、ledger_state_summary）；ObjectTemporalEntry：object_label、last_confirmed_location、last_confirmed_ts、current_candidate_location、current_candidate_ts、candidate_location_type、current_container_candidate、current_container_confidence、container_state、container_last_event_ts、visibility_status、current_hypothesis_summary、ledger_confidence、user_confirmed_location、user_confirmed_ts；LedgerEvent：event_type（container_opened/container_closed/object_candidate_in_container/user_confirmed_location/user_denied_location + M1 事件集合）、timestamp、summary；单对象优先；**last_confirmed_* 与容器候选分离**（容器逻辑只更新 current_candidate_* 与容器字段，不覆盖 last_confirmed_*）；最小容器逻辑：容器打开候选、容器关闭候选、对象进入容器候选（object_inside_candidate / object_inside_confirmed 占位）；用户否认可触发容器候选回退与降置信度；输入来自 smap、evidence_ledger、hypothesis_layer、recheck_planner、pools、focus_object_label、ctx 上一帧 last_confirmed_* 与容器状态字段 + 用户确认/否认；frame.object_temporal_ledger 与 runtime_ctx（object_last_confirmed_location、object_last_confirmed_ts、object_current_candidate_location、object_candidate_location_type、object_container_candidate、object_container_confidence、object_container_state、object_container_last_event_ts、object_visibility_status、object_ledger_confidence）写入；Viewer 展示最后可信/当前候选/候选类型/容器状态/容器候选置信度/最近事件/状态摘要。当前仍为单对象优先；未实现复杂容器视觉识别、多对象全场账本、复杂 re-id、长期持久化与经验沉淀。**object_search_interaction**（**交互式寻物 M0/M1/M1.5**）：**M1**：ObjectSearchInteractionResult 含 search_subtask_state、search_waiting_user_input、search_terminal_status、search_can_resume_main_task、search_summary_for_task_chain、last_user_response_*、search_result_level 等；用户回复注入驱动状态流转。**M1.5**：新增 interaction_flow_type（container_check_flow/occlusion_clear_flow/pocket_check_flow/last_location_flow/description_bootstrap_flow）、interaction_step_index、interaction_expected_user_input、interaction_timeout_ms、interaction_timeout_triggered、fallback_action、fallback_reason、next_search_step_summary、search_resolution_path、interaction_retry_count；三类典型流（容器检查/遮挡清理/口袋检查）显式化；等待用户输入+超时+fallback 最小闭环；next_search_step_summary 与 search_resolution_path 供 Viewer/经验系统；frame 与 runtime_ctx 同步 M1.5 字段；Viewer 展示 flow/timeout/fallback/path。当前已支持最小任务流增强；未实现完整对话管理器、开放世界搜索、多对象并发寻物、经验沉淀与学习型策略。**task_arbitration**（**任务仲裁 M0**）：TaskArbitrationResult：foreground_task_type、candidate_task_types、arbitration_action（preempt/interrupt_then_resume/merge_into_bundle/run_in_background/defer/continue_current）、arbitration_reason、risk_priority_level、environment_overlap_level、resource_conflict_level、user_interruption_cost、arbitration_applied；仅读取 goal、state、skeleton_mix、object_search_interaction、recheck_planner、object_temporal_ledger 与 ctx 可选 incoming_task_*；五维规则型判断（风险、环境重合、资源冲突、用户打扰、当前主任务）；与模块映射（Object Search 活跃→object_search、Recheck 活跃→recheck、minimum_mode/frozen→safety_guard、观察→observation）；frame.task_arbitration 与 runtime_ctx 写入；Viewer 展示。当前仅做最小任务仲裁层；未实现完整意图池、多任务执行器、正式改 Task Chain。**task_bundle**（**联合任务包 M0**）：TaskBundleResult：bundle_id、bundle_zone、bundle_task_types、bundle_dominant_skeleton、bundle_shared_focus、bundle_reason、bundle_status（proposed/active/blocked/closed）、bundle_created、bundle_applied、bundle_block_reason；仅当 task_arbitration.arbitration_action==merge_into_bundle 时生成；读取 task_arbitration、skeleton_mix、local_goal_spatial_map、object_search_interaction、recheck_planner、object_temporal_ledger、incoming_task_*；同环境合并、共享骨架与共享焦点摘要；守底阻断时 bundle_applied=False、bundle_status=blocked；frame.task_bundle 与 runtime_ctx 写入；Viewer 展示。当前仅做最小联合任务包结构；未实现 bundle 执行图、正式改 Task Chain、多 bundle 并存与调度、学习型合并策略。**task_chain_bridge**（**任务链桥接 M0**）：TaskChainBridgeResult：task_chain_foreground_summary、task_chain_state、task_chain_substate、task_chain_blocked、task_chain_block_reason、task_chain_can_resume、task_chain_bundle_state、task_chain_source_modules、task_chain_summary_text、task_chain_bridge_applied；仅读取 task_arbitration、task_bundle、object_search_interaction、state、current_foreground_task_type；将 arbitration/bundle/search 映射为任务链可读状态（active/paused/waiting_user/blocked/bundled/done/cancelled）；foreground/substate/bundle_state/can_resume/summary_text 规则型生成；frame.task_chain_bridge 与 runtime_ctx 写入；Viewer 展示。当前仅做任务链摘要桥接层；未正式改 Task Chain 主体、未实现 task dispatcher、多 bundle 调度、完整任务恢复器。**experience_evolution**（**经验演化 M0**）：ExperienceEvolutionResult（candidates: List[ExperienceCandidate]）；ExperienceCandidate：experience_type（object_search_path_pattern/container_candidate_pattern/occlusion_resolution_pattern/pocket_check_pattern/recheck_effectiveness_pattern）、source_module、source_path、source_summary、supporting_events_count、contradiction_count、user_confirmed_count、fallback_count、confidence_trend（up/flat/down）、evolution_status（candidate/watchlist/promotable/blocked/rejected）、evolution_reason、promotion_blocked、promotion_block_reason、evolution_hint_for_future；仅读取 evidence_ledger、hypothesis_layer、recheck_planner、object_temporal_ledger、object_search_interaction、state、用户确认/否认；经验候选来源规则与审计规则（单次成功不升格、多次支撑+低冲突+用户确认可 promotable、fallback/否认过多 blocked/rejected、高风险语境不升格）；不反写 hypothesis/object_ledger/recheck；frame.experience_evolution 与 runtime_ctx 首条摘要写入；Viewer 展示。当前仅做经验约束层/审计层。**M1**：同类经验候选聚合（experience_group_key、aggregated_source_paths、repeated_pattern_count）、contradiction_sources、watchlist_reason、promotable_score、evolution_confidence_band、future_use_scope、审计报告式 reason；snapshot_for_next 供下一帧聚合；未实现长期经验库、自动策略更新、跨会话沉淀、经验层反写主策略。 | 路径增量、relative_velocity_cm_s、ttc_ms、effective_spatial_resolution_cm 仍为宪法预留。骨架过滤 M0 不做：对象级复杂过滤、广告专项、记忆/遗忘/假设层联动、detector/OCR 调度改造。骨架记忆分池 M0 不做：数据库/持久化、复杂 TTL/Task-End/Value Decay/Evidence Replacement、长期证据门槛、情感记忆、attention_weight、Hypothesis Layer 联动、detector/OCR 主链改造。空间遗忘 M0 不做：Value Decay、Evidence Replacement、Stable/Anchor 复杂清理、情感记忆遗忘、Hypothesis Layer 联动、detector/OCR/动态策略主链改造、数据库/持久化。证据账本 M0 不做：完整场景推理、Hypothesis Layer、学习型证据权重、复杂多 claim 竞争、detector/OCR/动态策略主链改造、数据库/持久化。假设层 M0 不做：完整场景推理引擎、学习型假设排序、经验系统、长期 hypothesis ledger、detector/OCR/动态策略主链改造、对象级完整因果追踪、开放世界无限候选、数据库/持久化。补证规划 M0 不做：多步 planner、学习型策略、经验沉淀联动、开放式探索、detector/OCR/动态策略主链重构、数据库/持久化、新全局状态机。对象时空账本 M1.5 不做：多对象全场账本、复杂 re-id、持久化数据库、经验沉淀、复杂容器视觉识别。交互式寻物 M1.5 不做：正式合并 Task Chain、完整对话管理器、开放世界搜索、多对象并发寻物、经验沉淀与学习型策略。任务仲裁 M0 不做：完整意图池、多任务执行器、正式改 Task Chain、学习型编排、数据库/持久化。联合任务包 M0 不做：bundle 执行图、正式改 Task Chain、多 bundle 并存与调度、学习型合并策略、数据库/持久化。任务链桥接 M0 不做：正式改 Task Chain 主体、task dispatcher、多 bundle 调度、完整任务恢复器、数据库/持久化、学习型编排。经验演化 M0/M1 不做：长期经验库、自动策略更新、跨会话经验沉淀、多对象经验图谱、经验层反写主策略、detector/OCR 主链改造。 |

## 主线接入 M0（Cognitive Runtime Mainline Integration M0）

- **当前版本**：主线接入 M0；摘要先行、软控制优先、硬边界保留。
- **已接入模块**：task_chain_bridge、task_arbitration、task_bundle、object_search_interaction、recheck_planner、experience_evolution（只读摘要）。
- **frame 字段**：`mainline_integration`（MainlineIntegrationResult：integration_enabled、integration_summary、integration_consumed_modules、integration_soft_actions、integration_blocked_actions、integration_observation_notes、integration_applied）。
- **runtime_ctx 字段**：mainline_integration_summary、mainline_integration_modules、mainline_integration_soft_actions、mainline_integration_blocked_actions、mainline_integration_applied。
- **当前只做**：摘要消费与软控制；recheck 未阻断时走已有 local_goal_recheck_* / view_behavior_hint；object_search 以 prompt/action 摘要进入主流程；experience 只读进入 observation_notes。
- **未做**：正式改 Task Chain 主体、正式重构主执行器、经验层反写策略、全量接管、假设层/object_temporal_ledger 硬控制、新大一统状态机。
- **Viewer**：展示「主线接入 / Mainline Integration (M0)」卡片。
- **详见**：docs/MAINLINE_INTEGRATION_M0_DELIVERY.md。

## 静态图输入桥 + 候选审计 M0（Static Image Input Bridge + Candidate Audit M0）

- **当前版本**：已支持静态图输入桥（环境变量 `STATIC_IMAGE_INPUT_PATH`）与最小候选审计。
- **frame 字段**：`visual_candidate_audit`（VisualCandidateAuditResult：input_source_type、input_source_path、**detector_mode**、**detector_model_name**、detector_candidate_count、detector_candidate_labels、**detector_probe_candidate_count**、**detector_probe_candidate_labels**、ocr_candidate_count、ocr_texts、scene_description_present、search_target_label、mapped_candidate_labels、candidate_audit_status、candidate_audit_reason）。
- **runtime_ctx 字段**：input_source_type、input_source_path、visual_candidate_audit_status、visual_candidate_audit_reason、visual_candidate_labels、visual_candidate_mapped_labels。
- **当前只做**：图片进主流程、候选显式打出、目标词与候选映射审计；未接入专门视觉模型、未做 bbox/region 深度分析、未做多图轮播与长期图片测试框架。
- **Viewer**：展示「静态图候选审计 / Visual Candidate Audit (M0)」卡片。
- **分析脚本**：tools/analyze_visual_candidate_audit.py。
- **详见**：docs/STATIC_IMAGE_INPUT_AND_CANDIDATE_AUDIT_M0_DELIVERY.md。

**⚠ 视觉层真实化约定**：**Detector（YOLO）** 已接入真实 YOLO11n（或 v8n/受控 demo_fallback），见 docs/REAL_YOLO_INTEGRATION_M0_DELIVERY.md；**OCR / 场景描述** 仍可能为演示桩。当 detector_mode=real_yolo 时，detector 产出可作为候选审计与 object search 的真实输入；当 detector_mode=demo_fallback 或 OCR 仍为 demo 时，其产出不得作为「全链路认知能力真实性」的最终依据。

## 坐标 / 方位表达旁路 M0（Spatial Expression Sidecar M0）

- **目标**：把真实视觉候选（bbox）转换为二维相对方位表达（human/debug），用于调试与表达质量验证。
- **不做**：深度/距离估计、厘米级精度、3D 世界模型、主决策接入（search/evidence/experience/arbitration/bundle 不消费该旁路层）。
- **frame 字段**：`spatial_expression_sidecar`（SpatialExpressionResult）
  - focus_target_label
  - focus_target_expression
  - focus_target_debug_expression
  - **focus_target_actionable_expression**（Level 2 口语化行动表达 M0）
  - **focus_target_actionable_debug_reason**
  - candidate_count
  - candidates（SpatialExpressionCandidate[]，可选 candidate_actionable_expression）
    - candidate_label / candidate_confidence
    - candidate_bbox_center_x_norm / candidate_bbox_center_y_norm
    - candidate_sector / candidate_relative_bearing_deg
    - candidate_horizontal_band / candidate_vertical_band
    - candidate_human_location_text / candidate_debug_location_text
    - candidate_is_focus_target / candidate_source_mode（main/probe/mapped_target）
  - sidecar_reason
- **runtime_ctx 摘要字段**（仅旁路）：
  - spatial_focus_expression / spatial_focus_debug_expression
  - spatial_candidate_labels / spatial_candidate_expressions
- **Viewer**：新增「坐标/方位表达旁路 / Spatial Expression Sidecar (M0)」卡片。
- **分析脚本**：tools/analyze_spatial_expression_sidecar.py。

## Spatial Expression → Search 文案接入 M0.5

- **定位**：表达增强，不是决策升级；仅将 sidecar 的 `focus_target_expression` 接入 Object Search Interaction 的**文案层**。
- **已支持**：用位置短语增强 `suggested_search_zone`、`next_search_step_summary`；无 sidecar 时完整回退到原逻辑。
- **ObjectSearchInteractionResult 新增**：`search_zone_from_sidecar`（bool）。
- **runtime_ctx 新增**：`object_search_location_phrase`、`object_search_zone_from_sidecar`。
- **不做**：真实距离、厘米级表述、动作控制升级；位置表达不进入 evidence/experience/arbitration/bundle 主判断。
- **详见**：docs/SPATIAL_EXPRESSION_TO_SEARCH_COPY_M0_5_DELIVERY.md。

## Level 2 口语化行动表达 M0（Actionable Conversational Spatial Expression M0）

- **定位**：在 Sidecar M0 + Search 文案 M0.5 基础上，新增 **Level 2 口语化行动表达**；日志层保留精确坐标与标尺，表达层形成 Level 1 + Level 2 双层。
- **frame 字段**：`spatial_expression_sidecar` 新增 `focus_target_actionable_expression`、`focus_target_actionable_debug_reason`；候选可选 `candidate_actionable_expression`。
- **生成**：仅基于已有真实字段（focus_target_expression、sector/band、current_container_candidate、interaction_flow_type、interaction_action）派生；仅近场/桌面/局部场景试点。
- **文案接入**：builder 在 build search 后调用 `build_focus_target_actionable_expression`，有 Level 2 时用其覆盖 suggested_search_zone、next_search_step_summary。
- **runtime_ctx**：spatial_focus_actionable_expression；object_search_actionable_zone、object_search_actionable_next_step（有 Level 2 时同步）。
- **不做**：厘米级距离、动作控制升级；不反写底层主事实；不改主状态机与 evidence/experience/arbitration/bundle。
- **详见**：docs/ACTIONABLE_CONVERSATIONAL_EXPRESSION_M0_DELIVERY.md。

## Action Hint Copy M0（从推理到引导，再到确认）

- **定位**：仅文案级动作提示（先看哪里、先检查什么、先移开什么、再确认什么）；不做动作控制、不改主状态机。
- **frame 字段**：`action_hint_copy`（ActionHintCopyResult：action_hint_stage、action_hint_summary、action_hint_primary、action_hint_followup、action_hint_confirmation、action_hint_reason、action_hint_applied）。
- **生成**：在 object_search_interaction 与 Level 2 更新之后，由 action_hint_copy.build_action_hint_copy 只读 search、sidecar、ledger、evidence、hypothesis、recheck 生成；不反写上述模块。
- **规则**：容器流/遮挡流/一般搜索/ target_unclear 写死主提示+后续提示+确认提示；主提示中的位置用 Level 1（focus_target_expression）。
- **runtime_ctx**：object_search_action_hint_primary、object_search_action_hint_followup、object_search_action_hint_confirmation、object_search_action_hint_stage。
- **不做**：动作控制、运动控制、任务执行器、主状态机/arbitration/bundle 升级。
- **详见**：docs/ACTION_HINT_COPY_M0_DELIVERY.md。

## Confirmation Input Bridge M0（用户确认输入桥 M0）

- **定位**：将用户对引导的反馈接回系统，形成 推理→引导→用户反馈→系统推进；只做输入桥 + 最小状态推进。
- **frame 字段**：`confirmation_input_bridge`（ConfirmationInputBridgeResult：confirmation_input_type、confirmation_input_raw_text、confirmation_input_source、confirmation_bridge_reason、confirmation_bridge_applied、confirmation_bridge_target_flow、confirmation_bridge_next_effect）。
- **输入**：显式注入（runtime_ctx.search_confirmation_input_type / search_confirmation_input_raw_text 或环境变量 CONFIRMATION_INPUT_TYPE / CONFIRMATION_INPUT_RAW_TEXT）+ 可选文本规则映射（窄规则）。
- **离散类型**：confirmed_yes、confirmed_no、opened_container、occlusion_cleared、checked_and_not_found、target_found、target_not_found、cancelled、unknown。
- **推进**：按 flow 写死 next_effect；mark_target_found / cancel_search 时本帧改写 search_terminal_status、search_can_resume_main_task。
- **runtime_ctx**：注入用 search_confirmation_input_*；桥接结果 confirmation_input_type、confirmation_input_raw_text、confirmation_bridge_next_effect、confirmation_bridge_target_flow、confirmation_bridge_applied；有输入时一次性清空注入。
- **不做**：完整 NLU、多轮对话引擎、动作执行器、任务链重写。
- **详见**：docs/CONFIRMATION_INPUT_BRIDGE_M0_DELIVERY.md。

## Confirmation Whitebox Trace M0（确认输入白盒轨迹 M0）

- **定位**：对白盒化 `confirmation_input_bridge` 的确认映射与推进进行正式解释：为什么映射成该 confirmation_input_type、为什么 next_effect 是这个、为什么没选其它类型/推进，并产出**用户可见解释层**（短句映射，不直出内部 JSON）。
- **frame 字段**：`confirmation_whitebox_trace`（ConfirmationWhiteboxTraceResult：reasoning_steps、weight_allocation、exclusion_log、interaction_trace、**user_visible_explanation**、whitebox_summary、whitebox_applied）。
- **输入（只读）**：confirmation_input_bridge /（可选）action_hint_copy / object_search_interaction / grid_search_expansion / recheck_planner。
- **约束**：不改 Confirmation Input Bridge 主逻辑；不做 NLU 升级；用户可见层为解释映射层，不得直出 weight_components 等内部 JSON。
- **详见**：docs/CONFIRMATION_WHITEBOX_TRACE_M0_DELIVERY.md。

## Local Task Space Grid M0（局部任务空间格 M0）

- **定位**：局部、二维、任务相关的 3x3 网格（left/center/right × back/mid/front），作为组织层把 focus/容器候选/遮挡/候选标签挂到统一空间骨架上；不替代底层 bbox/sidecar 主事实。
- **frame 字段**：`local_task_space_grid`（LocalTaskSpaceGridResult：cells、focus_target_cell_id、container_candidate_cell_id、occlusion_cell_ids、recommended_search_cell_id、grid_summary、grid_applied）。
- **输入**：只读 spatial_expression_sidecar / object_search_interaction / object_temporal_ledger（必要时可扩展只读 evidence/hypothesis/vca）；不反写这些模块。
- **不做**：全局地图、3D、SLAM、持久化/跨帧沉淀；不用于替代 L1/L2/Action Hint 文案（本轮仅调试/组织层接入）。
- **runtime_ctx 摘要**：task_grid_focus_cell、task_grid_container_cell、task_grid_recommended_search_cell、task_grid_summary。

## Local Task Space Grid M0.5（轻消费层）

- **定位**：Grid 从展示层升级为轻消费层；仅用于文案补位（组合输出），仍不进入主判断、不替代 sidecar/L1/L2。
- **新增字段**：recommended_search_cell_human_label、recommended_search_adjacent_cells、grid_followup_hint；每格可含 adjacent_cell_ids。
- **消费规则**：风格 A：`{原文案}（{格标签}）`，保持原 zone/next_step/action_hint 主体不变；无 Grid 时完全回退。
- **详见**：docs/LOCAL_TASK_SPACE_GRID_M0_5_DELIVERY.md。

## Grid-driven Search Expansion M0（基于 Grid 的扩搜建议层）

- **定位**：建议层，不是控制层；产出 primary/secondary 搜索格与原因，用于 Search/Action Hint 的附加建议，不进入硬控制。
- **frame 字段**：`grid_search_expansion`（GridSearchExpansionResult：primary/secondary、strategy、reason、summary、hint、applied）。
- **轻接入**：可将 expansion_hint 作为附加建议追加到 next_search_step_summary 与 action_hint_followup；不得替代原语义。
- **不做**：不改 object_search_interaction 主状态机、不改 detector/recheck 执行逻辑、不做路径规划/持久化。\n- **详见**：docs/GRID_DRIVEN_SEARCH_EXPANSION_M0_DELIVERY.md。

## Grid Search Whitebox Trace M0（扩搜建议层白盒轨迹）

- **定位**：白盒化结果是正式结果的一部分（frame/viewer/runtime_ctx/jsonl），不是终端 print；覆盖推理过程、权重分配、排除逻辑、互动过程。
- **frame 字段**：`grid_search_whitebox_trace`（GridSearchWhiteboxTraceResult：reasoning_steps、weight_allocation、exclusion_log、interaction_trace、whitebox_summary、whitebox_applied）。
- **约束**：不改变 grid_search_expansion 结果，不改 object_search_interaction 主状态机，不做执行控制；规则权重为显式规则分值，不是学习权重。
- **详见**：docs/GRID_SEARCH_WHITEBOX_TRACE_M0_DELIVERY.md。

## Recheck Whitebox Trace M0（补证链路白盒轨迹）

- **定位**：对白盒化 `recheck_planner` 的补证建议链路进行正式解释：为什么需要补证、为什么选当前补证动作、为什么没选别的、阻断来自哪里、用户反馈如何影响补证语义（仅解释）。
- **frame 字段**：`recheck_whitebox_trace`（RecheckWhiteboxTraceResult：reasoning_steps、weight_allocation、exclusion_log、interaction_trace、whitebox_summary、whitebox_applied）。
- **输入（只读）**：recheck_planner / hypothesis_layer / evidence_ledger / object_search_interaction / confirmation_input_bridge / action_hint_copy /（可选）local_task_space_grid / state（minimum_mode、scene_gate、human_check 等阻断来源）。
- **约束**：不新增补证动作；不改 `recheck_planner` 主逻辑与阻断规则；不改 `object_search_interaction` 主状态机；不做控制层升级；规则权重为显式规则分值，不是学习权重。
- **交付状态**：实现 + 测试均通过（自动化测试 4/4、实跑 smoke、JSONL 审计通过；具备完全通过口径）。
- **详见**：docs/RECHECK_WHITEBOX_TRACE_M0_DELIVERY.md（含 11. 本轮结论）。

## Action Hint Whitebox Trace M0（引导话术白盒轨迹）

- **定位**：对 `action_hint_copy` 的主提示/后续/确认话术建立正式白盒轨迹，解释为什么主提示是这句、为什么 followup/confirmation 是这句、为什么没选另一条提示路径、flow/sidecar/grid/confirmation 如何影响话术；并产出**用户可见解释层**（短句映射，不直出内部 JSON），供未来线上与用户交互。
- **frame 字段**：`action_hint_whitebox_trace`（ActionHintWhiteboxTraceResult：reasoning_steps、weight_allocation、exclusion_log、interaction_trace、**user_visible_explanation**、whitebox_summary、whitebox_applied）。
- **输入（只读）**：action_hint_copy、object_search_interaction、spatial_expression_sidecar、grid_search_expansion、confirmation_input_bridge、local_task_space_grid、evidence_ledger、hypothesis_layer。
- **约束**：不改 Action Hint 主逻辑；不做对话引擎/NLG 重构/控制器升级；用户可见层为解释映射层，不得直出 weight_components 等内部 JSON。
- **详见**：docs/ACTION_HINT_WHITEBOX_TRACE_M0_DELIVERY.md。

---

## Whitebox Trace Schema Freeze M0（统一白盒模板冻结）

### A. 白盒输出约束（写死）

后续凡进入 Luna 正式建议/推进链路的模块，只要涉及：
- 结果推荐 / 选择
- 排除逻辑
- 用户反馈驱动推进

则必须具备**白盒轨迹输出能力**（进入 frame/viewer/runtime_ctx/jsonl），不得仅以 print/临时日志替代。

### A'. 白盒分层原则（写死）

- **白盒必须可审计**：内部调试、审计、经验治理用，保留完整内容（reasoning_steps、weight_allocation、exclusion_log、interaction_trace、raw summary）。
- **其中一部分必须可用户可见**：用于未来线上与用户交互，帮助用户理解“为什么我这么判断、我优先看哪里、为什么没选另一个方向、你刚才的反馈让我改了什么判断”。
- **用户可见白盒是“解释映射层”**：不得把 weight_components 等原始 JSON 直出给用户；必须产出一组**用户可见解释字段**（短句、可理解），真实映射内部白盒原因，但不泄露内部分值/结构细节。

即：**内部白盒层**（完整 trace）与 **用户可见白盒层**（解释短句）并存；用户可见层是解释映射，不是原始日志直出。

### B. 最小白盒结构（五块骨架）

- reasoning_steps
- weight_allocation
- exclusion_log
- interaction_trace
- whitebox_summary / whitebox_applied

### C. 当前白盒状态（写死）

- **已完成正式白盒化**：Grid Search Expansion（grid_search_whitebox_trace）、Recheck Planner（recheck_whitebox_trace）、**Action Hint（action_hint_whitebox_trace，含用户可见解释层）**。  
- **尚未接入**：其余模块未白盒化，但后续应优先复用统一模板（见 docs/WHITEBOX_TRACE_SCHEMA_FREEZE_M0.md）。  

## Luna Reasoning Console M0（推理控制台 M0）

**定位（写死）**：Reasoning Console 是未来 Luna 的**开箱找问题中心**，也是所有推理/白盒/可视化/错判归因的**统一入口**。  

**硬约束（必须遵守）**：

> 后续任何新功能，只要存在判断、排除、推荐、用户反馈影响推进、解释层输出，必须接入 Reasoning Console。不得另起新的独立白盒页/调试页/推理页。

**交付件**：`docs/REASONING_CONSOLE_M0_DELIVERY.md`。  
**入口脚本**：`tools/reasoning_console_server.py`（读取 DecisionMonitor JSONL，只读聚合与展示，不反写主逻辑）。

## Reasoning Structure Tree M0（推理与决策结构树 M0）

**定位（写死）**：结构树是白盒之上的总组织结构，用于组织线索/假设/动作/反馈/排除/收敛路径，服务推理可视化、错判排查与后续优化。  

**硬约束（必须遵守）**：

> 后续任何新功能，只要产生新的推理分支、排除路径、用户反馈驱动路径或结果收敛路径，都应逐步接入 Reasoning Structure Tree；不得长期只存在于模块内部而不进入总结构树。

**交付件**：`docs/REASONING_STRUCTURE_TREE_M0_DELIVERY.md`。  
**实现**：`decision_monitor/reasoning_structure_tree.py`（规则版聚合树；Reasoning Console 负责展示）。

## Experience / Evidence Whitebox Trace M0（成长链白盒：证据×假设×经验治理）

**原则（写死）**：

> 证据、假设与经验治理层不得长期停留在模块内部解释；后续凡涉及 evidence / hypothesis / experience 的判断、排除、治理结果，必须接入统一白盒模板与 Reasoning Structure Tree。

**交付件**：

- `docs/EVIDENCE_HYPOTHESIS_WHITEBOX_TRACE_M0_DELIVERY.md`
- `docs/EXPERIENCE_GOVERNANCE_WHITEBOX_TRACE_M0_DELIVERY.md`


---

## Phase 2 已冻结能力清单与边界（Closure & Freeze）

- **收口主文档**：docs/MAINLINE_2_PHASE2_FINAL_CLOSURE.md。
- **接口冻结**：docs/PHASE2_INTERFACE_FREEZE.md（视觉候选、空间表达、Search 文案、Action Hint、Confirmation Input、Search 终端推进）。
- **状态总表**：docs/PHASE2_STATUS_MATRIX.md。
- **已通过且接口已冻结**：静态图输入桥 + 候选审计 M0、真实视觉接入 M0、Spatial Expression Sidecar M0、Search 文案 M0.5、Level 2 口语化行动表达 M0、Action Hint Copy M0、Confirmation Input Bridge M0；以及 Skeleton Mix/Filter、Spatial Memory/Forgetting、Evidence Ledger、Hypothesis Layer、Recheck Planner、Object Temporal Ledger、Object Search Interaction、Task Arbitration/Bundle/Bridge、Experience Evolution、Mainline Integration 等本阶段基线。当前语义边界以各模块 delivery 与 CONTRACT 本节为准。

### Demo / Fallback / 真实模式约定（写死）

- **demo mode 产出**不得作为认知真实性验证依据；仅当 detector_mode=real_yolo（或项目约定的真实模式）时，detector 产出可作为候选审计与 object search 的真实输入依据。
- **real_yolo / demo_fallback** 必须可审计（detector_mode、detector_model_name 写入 frame）。
- **probe 候选**不得污染主候选语义；main 与 probe 分离，probe 仅用于扩展候选集合与 sidecar 输入，不替代主路语义。
- **Level 2 / Action Hint / Confirmation** 仅为表达层与输入桥，不等于动作控制、路径规划或执行器；不得以“已通过”声称动作控制/执行器已完成。

### 后续扩展约束（写死）

- **Local Task Space Grid / 局部环境模型**不得绕开当前 sidecar、search、action_hint、confirmation 已冻结接口；新模块应复用 PHASE2_INTERFACE_FREEZE 所列字段与语义。
- **新模块**不得直接反写底层主事实（如精确坐标、band、sector 等），除非在 CONTRACT 与 PHASE2_INTERFACE_FREEZE 中**显式修订**。
- 下一阶段默认入口为 **Local Task Space Grid M0**（或项目约定等价入口）；进入前提为本阶段接口冻结完成。
