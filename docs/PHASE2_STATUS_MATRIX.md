# Phase 2 模块状态总表（Status Matrix）

快速查阅用；偏表格化，非长 prose。

**完整形态上位总纲**：`docs/LUNA_MAINLINE_SHAPE_BLUEPRINT.md` — Luna 8 条链、4 层级、数据流、越权边界、快/慢链、评分哲学与 reserve 位；约束主线/白盒/日志/后处理/图书馆记忆/治理等后续专题设计，**非实现说明书**。

**决策运行主链专题（M0 定稿）**：`docs/DECISION_MAINLINE_ARCHITECTURE.md` — 数据源调度层与主链关系、六阶段、四态、recheck/clarification/fallback/recovery、回流与任务链接口、主线—白盒—日志主链侧义务；**非代码实现文档**。

**白盒观察链专题（M0 定稿）**：`docs/WHITEBOX_OBSERVATION_ARCHITECTURE.md` — 五层结构、主链/调度层关系、溯源与评分分工、记忆调用可解释、事件语义类别、与日志/总结/后处理边界；**非 UI/schema 实现文档**。

**日志落地与总结分层专题（M0 定稿）**：`docs/TRACE_LOGGING_AND_SUMMARY_PIPELINE.md` — 黑匣子三层、运行总结链、日志/总结严格分离、summary-first、后处理接 summary/trace、记忆双重要求、同链校验；**非 JSON/schema/文件格式实现文档**。

**图书馆/记忆/治理专题（M0 定稿）**：`docs/LIBRARY_MEMORY_AND_GOVERNANCE_ARCHITECTURE.md` — 后处理/图书馆/记忆边界与主流转、治理非第二主脑、observe/watch/defer/block 统一动作语义、reserve 归位与权限边界；**非算法/写库实现文档**。

**工程映射表（M0）**：`docs/LUNA_MAINLINE_ENGINEERING_MAPPING.md` — 五份架构文档与当前仓库（`decision_monitor`/工具链/日志）对齐：已实现、reserve、缺口、主线—白盒—日志判断、下一阶段优先级；**非新架构、非实现方案**。

**Mainline Rebaseline & Gap Review（M0）**：`docs/MAINLINE_REBASELINE_GAP_REVIEW_M0.md` — 主线工程多轮补齐（调度/Trace×Summary/任务链/记忆调用等）后的**阶段基线与缺口复盘**；更新 P0/P1/P2 判断与第十批真实场景回归前置条件；**非**新架构文档。

**数据源调度层工程设计（M0）**：`docs/INFORMATION_SOURCE_SCHEDULING_ARCHITECTURE.md` — P0 缺口专项：六类源、五维调度、分层优先级、主导源与切换语义、与主链/白盒/日志接口、最小落地顺序；**非代码/schema/算法**。

**Scheduled Source State 最小接入（M0）**：`docs/SCHEDULED_SOURCE_STATE_MINIMAL_INSERT_M0.md` — `scheduled_source_state` 已最小接入主链入口、白盒第二层与日志聚合链；复杂调度算法仍未展开。

**Source Scheduling × Whitebox 同链增强（M0.1）**：`docs/SOURCE_SCHEDULING_WHITEBOX_ALIGNMENT_M0_1.md` — 在 M0 基础上增强白盒第二层解释力（原因/事件/告警），并在结构树/时间轴/聚合链形成更强可追溯表达。

**Trace × Summary 工程分层（M0.2）**：`docs/TRACE_SUMMARY_SEPARATION_M0_2.md` — Raw Trace / Structured Event / Summary Reference 最小工程分层；`run_summary_reference` 进入 frame/JSONL/聚合/Console/Viewer。

**任务链 × 主链整合架构（M0 工程设计）**：`docs/TASKCHAIN_MAINLINE_INTEGRATION_ARCHITECTURE.md` — 任务链与主链边界、经调度层进入主链、回流闭环、白盒/日志/总结同链义务；**非**任务引擎/任务中心实现文档。

**Task Chain State Snapshot 最小接入（M0）**：`docs/TASK_CHAIN_STATE_SNAPSHOT_MINIMAL_INSERT_M0.md` — `task_chain_state_snapshot` 进入 frame/调度层/白盒/日志与 `run_summary_reference`；**非**完整任务引擎。

**Task Chain Position Explanation（M0.1）**：`docs/TASK_CHAIN_POSITION_EXPLANATION_ALIGNMENT_M0_1.md` — 任务链位置 reason/warn/时间轴事件与 `task_chain_progress_summary` 增强；**非**任务引擎重构。

**Memory Invocation Explanation（M0.3）**：`docs/MEMORY_INVOCATION_EXPLANATION_M0_3.md` — `memory_invocation_explanation` 与 Summary 记忆行；**非**记忆写入/图书馆真接入。

**Mainline State / Phase Explicitness（M0.4）**：`docs/MAINLINE_STATE_PHASE_EXPLICITNESS_M0_4.md` — `mainline_state_snapshot`、白盒树/时间轴、`run_summary_reference.mainline_state_summary`；**非**主链重写/完整状态机。

**Summary × Post-Processing Boundary Contract（M0.5）**：`docs/SUMMARY_POST_PROCESSING_BOUNDARY_CONTRACT_M0_5.md` — `post_processing_summary_entry`、回溯提示、与 reserve 交叉引用；**非**后处理算法/图书馆真接入。

**Mainline Narrative Alignment（M0.6）**：`docs/MAINLINE_NARRATIVE_ALIGNMENT_M0_6.md` — `mainline_narrative_alignment`、`summary_brief` 骨架统一、`post_processing_summary_entry.narrative_readable` 对齐；**非**新增证据层/算法层。

**Narrative / Evidence Tension Review（M0）**：`docs/NARRATIVE_EVIDENCE_TENSION_REVIEW_M0.md` — 叙事—证据五维张力只读审计（`narrative_evidence_tension_review`），**不**改 benchmark/triage、**不**裁决主链。

**Tension Audit Calibration Review（M0）**：`docs/TENSION_AUDIT_CALIBRATION_REVIEW_M0.md` — 基于 M1.3 全量结果的 tension 分布校准与去噪（`tools/analyze_tension_audit_m13.py`）；**不**改代码与 hard-fail。

**Tension Review Template / Soft-Fail Candidate Spec（M0）**：`docs/TENSION_REVIEW_TEMPLATE_AND_SOFT_FAIL_SPEC_M0.md` — 五维 tension 使用层级、配对规则、人工 review 模板与第十四批前口径；**不**写入 benchmark/triage。

**Tension Severity Profile Spec（M0）**：`docs/TENSION_SEVERITY_PROFILE_SPEC_M0.md` — 原始观测档位 → `none`/`watch`/`review`/`critical_candidate` 工程风险画像；单轮/多轮与部分维适用边界；**不**改评测与实现。

**Mainline Engineering Baseline Freeze（M0.6）**：`docs/MAINLINE_ENGINEERING_BASELINE_FREEZE_M0_6.md` — 当前主线工程阶段冻结口径；用于回第十批真实场景前统一验收，不替代架构文档。

**M0.6 收纳精度（Audit Follow-up）**：冻结口径额外写死字段/事件锚点与排除项：`mainline_narrative_brief`、`post_processing_summary_entry.narrative_readable`、`summary_post_processing_entry_id`、source/task/memory/mainline 时间轴事件族；并明确 smoke/benchmark 产物不纳入能力基线。

**Real Scenario Pack M1.0（第十批回归）**：`docs/REAL_SCENARIO_PACK_M1_0_DELIVERY.md` — 冻结基线后的首次压测；结果需按 `baseline_covered_defect` / `baseline_excluded_requirement` / `reserve_only_finding` 三类归档。

**Targeted Fix Sprint M1.0.x（第十批定点收口）**：`docs/TARGETED_FIX_SPRINT_M1_0_X.md` — 面向 `R53/R54/R55/R56` 的最小定点修复；post-fix 整包 `58/58`，`blocked_without_resolution` 清零，triage 热点清空。

**Real Scenario Pack M1.1（第十一批扩包）**：`docs/REAL_SCENARIO_PACK_M1_1_DELIVERY.md` — 在冻结基线首轮验证后继续扩压；新增 `R59–R64`，整包 `64` case 中 `R60/R61/R64` 暴露新的 `baseline_covered_defect`（`blocked_without_resolution`），热点模块回到 `recheck_planner`。

**Real Scenario Pack M1.2（第十二批扩包）**：`docs/REAL_SCENARIO_PACK_M1_2_DELIVERY.md` — 在 `M1.0`/`M1.0.x` 与 `M1.1`/`M1.1.x` 稳定基线上继续扩压（跨层一致性、长链稳态、叙事—证据张力）；整包 `70` case 全通过，未新增 harness 级 `blocked_without_resolution`。

**Real Scenario Pack M1.3（第十三批扩包）**：`docs/REAL_SCENARIO_PACK_M1_3_DELIVERY.md` — 冻结基线 + `narrative_evidence_tension_review` 审计层下的首次扩包；整包 `76` case 全通过，pack 摘要附带 `tension_audit`（**不**参与 hard-fail）。

**Real Scenario Pack M1.4（第十四批扩包）**：`docs/REAL_SCENARIO_PACK_M1_4_DELIVERY.md` — 冻结基线 + tension 审计 + **`TENSION_SEVERITY_PROFILE_SPEC_M0` 画像语言**（`tools/tension_severity_profile_map.py` / pack `severity_audit`）；新增 `R77–R82`，整包 `82` case 全通过；**不**将 severity 接入 hard-fail。

**Real Scenario Pack M1.5（第十五批扩包）**：`docs/REAL_SCENARIO_PACK_M1_5_DELIVERY.md` — **`RESUME_PROGRESS_SUMMARY_ALIGNMENT_M0` 摘要链补强后**的验证性扩包；新增 `R83–R88`，整包 `88` case 全通过；**`critical_candidate` 与 `pc∧lg` high** 较 `m14` 上升（辅助观察，**非** harness fail）。

**Real Scenario Pack M1.6（第十六批扩包）**：`docs/REAL_SCENARIO_PACK_M1_6_DELIVERY.md` — 冻结基线 + tension/severity + **`SF-1′` advisory** 同帧观察（`advisory_sf1_prime_audit`）；新增 `R89–R94`，整包 `94` case 全通过；**不接** advisory gate、**不改** harness。

**Real Scenario Pack M1.7（第十七批扩包）**：`docs/REAL_SCENARIO_PACK_M1_7_DELIVERY.md` — 在 `m16` 基线上新增 `R95–R100`，整包 `100` case 全通过；持续验证 advisory 与 `critical_candidate` **同集合（本批 11=11）**；**不接** gate、**不改** triage/benchmark。

**Real Scenario Pack M1.8（第十八批扩包）**：`docs/REAL_SCENARIO_PACK_M1_8_DELIVERY.md` — 新增 `R101–R106`，整包 `106` case 全通过；重点验证 tightening 后 `nt` 在真实扩包中的稳定性与协同性（`nt` 分布出现 `low/medium`，且不参与 hard-fail）；`advisory` 与 `critical_candidate` 仍同集合（12=12）。

**M1.x Baseline Consolidation Review（阶段收束）**：`docs/M1X_BASELINE_CONSOLIDATION_REVIEW.md` — 对 M1.x 主线做阶段性收口：闭环/未闭环清单、边界、阶段判断与下一阶段优先级（不扩场景、不改规则、不接 gate）。

**Critical Candidate Pattern Review M0**：`docs/CRITICAL_CANDIDATE_PATTERN_REVIEW_M0.md` — 基于 `m15` **7** 例 `critical_candidate` 的模式复盘（结构化：`logs/critical_candidate_pattern_m15.json`、`tools/analyze_critical_candidate_patterns_m15.py`）；**不**改规则、**不**接 soft-fail。

**Soft-Fail Candidate Draft M0**：`docs/SOFT_FAIL_CANDIDATE_DRAFT_M0.md` — 将主模式 **`resume_fragility_with_global_main_stall`** 写为 **SF-1′** 人审 / advisory 条款（**`TENSION_REVIEW_TEMPLATE_AND_SOFT_FAIL_SPEC_M0.md` §4** 交叉引用）；**不接**自动 gate、**不改** benchmark。

**Soft-Fail Candidate Validation Pack M0**：`docs/SOFT_FAIL_CANDIDATE_VALIDATION_PACK_M0.md` — 用固定矩阵 + **`tools/validate_soft_fail_candidate_clause_m0.py`** 验证 **SF-1′** 边界（`logs/soft_fail_candidate_validation_m0.json`）；**不**扩默认整包、**不**接规则。

**Advisory / Review Gate Draft M0**：`docs/ADVISORY_REVIEW_GATE_DRAFT_M0.md` — **SF-1′** 的 **review / advisory 使用草案**（提示权、无裁决权）；推荐接入顺序：文档模板 → Console → post-processing 预留；**不接** benchmark / hard-fail / triage。

**Advisory Observation Integration M0**：`docs/ADVISORY_OBSERVATION_INTEGRATION_M0.md` — 将 **SF-1′** 从 pack/文档推进到 **frame 顶层 + JSONL + aggregator + Console/Viewer 可见** 的最小工程接入；**仅提示权**，不参与判定。

**Severity Signal Gap Review M0**：`docs/SEVERITY_SIGNAL_GAP_REVIEW_M0.md` — 基于 `m14` 与 `logs/severity_signal_gap_m14_analysis.json` 复盘 **review 多而 `critical_candidate` 为 0**、`lg` 梯度与 `nt` 塌缩原因；**不**改 benchmark / 规则；只读分析脚本 `tools/analyze_severity_signal_gap_m14.py`。

**Local-Global Progress Gradient Tightening M0**：`docs/LOCAL_GLOBAL_PROGRESS_GRADIENT_TIGHTENING_M0.md` — 仅收紧 **`local_global_progress_tension`** 启发式（`decision_monitor/narrative_evidence_tension_review.py`），消除 **`resume=` 字段名假阳性**、引入 **`low`** 档；前后对比 `logs/local_global_gradient_analysis_m14.json`（`logs/real_scenario_pack_m14_pre_lg_gradient.json` → 当前 `m14`）；**未**动 `nt` / benchmark。

**Resume / Closure Signal Alignment Review M0**：`docs/RESUME_CLOSURE_SIGNAL_ALIGNMENT_REVIEW_M0.md` — 只读审查 **resume / closure / main progress** 在 **`run_summary_reference` / TCS / inputs** 的**同帧对齐**与**压缩损失**；产物 `logs/resume_closure_signal_alignment_m14.json`（`tools/analyze_resume_closure_signal_alignment_m14.py`）；**未**改主链与 tension 规则。

**Resume Progress Summary Alignment M0**：`docs/RESUME_PROGRESS_SUMMARY_ALIGNMENT_M0.md` — **ctx → inputs → TCS → run_summary** 摘要链补强（`InputsLayer` 场景字段、`resume_main_progress_alignment_summary`、`task_chain_progress_summary` 显式 token）；**不**改 benchmark/recheck；整包 `m14` 可出现 **`pc∧lg` high** 与 **`critical_candidate`**；单测 `tests/test_resume_progress_summary_alignment.py`。

**Narrative-Trace Support Heuristic Tightening M0**：`docs/NARRATIVE_TRACE_SUPPORT_HEURISTIC_TIGHTENING_M0.md` — 仅收紧 **`narrative_trace_support_tension`（nt）** 启发式：移除“事件多即 none”的失敏门槛，引入 timeline **key anchors**，使 nt 在 `m17` 上出现少量 `watch/review` 梯度；**不**改 benchmark/triage。

**NT Coordination Review M0**：`docs/NT_COORDINATION_REVIEW_M0.md` — 基于 `m18` 复盘 nt 与 `pc/lg` 的协同边界（结构化：`logs/nt_coordination_m18_analysis.json`）：确认 nt 已可用但职责偏“薄证据观察”，不与所有高风险维强绑定；阶段建议为 M0 收口后回到扩包观察。

| 模块名 | 当前版本 | 是否通过 | 是否冻结 | 输入 | 输出 | 主链消费 | 仍预留 |
|--------|----------|----------|----------|------|------|----------|--------|
| 静态图输入桥 + 候选审计 | M0 | 是 | 是 | 图片/候选/目标词 | visual_candidate_audit | 是 | OCR/scene 全真实化 |
| 真实视觉接入（YOLO） | M0 | 是 | 是 | 帧/配置 | detector_*、mapped_* | 是 | demo 不作为真实性依据 |
| Spatial Expression Sidecar | M0 | 是 | 是 | 候选 bbox/映射 | focus_target_expression、actionable、debug | 否（旁路） | 深度/距离 |
| Spatial Expression → Search 文案 | M0.5 | 是 | 是 | sidecar | suggested_search_zone、next_search_step_summary | 是 | — |
| Level 2 口语化行动表达 | M0 | 是 | 是 | sidecar、search、ledger | focus_target_actionable_* | 是（文案） | 厘米级/动作控制 |
| Local Task Space Grid | M0 / M0.5 | 是 | 是 | sidecar、search、object_ledger | focus/container/occlusion/recommended cell + human_label + adjacent + followup_hint | 否（组织层） | 跨帧/持久化/3D |
| Grid-driven Search Expansion | M0 | 是 | 是 | local_task_space_grid、search | primary/secondary + strategy + hint | 否（建议层） | 执行器/路径规划/控制 |
| Grid Search Whitebox Trace | M0 | 是 | 是 | grid_search_expansion + action_hint + confirmation | reasoning/weights/exclusion/interaction | 否（审计层） | 全系统白盒化 |
| Whitebox Trace Schema Freeze | M0 | 是 | 是 | Grid Search Whitebox Trace 作为样板 | 统一五块骨架模板（reason/weight/excl/interaction/summary） | — | 全系统模块接入推进 |
| Object Search Interaction | M0/M1/M1.5 | 是 | 是 | ledger、evidence、hypothesis、recheck、ctx | interaction_*、suggested_zone、next_step_summary | 是 | 完整对话/多对象 |
| Action Hint Copy | M0 | 是 | 是 | search、sidecar、ledger 等 | action_hint_primary/followup/confirmation | 是（表达） | 动作控制 |
| Confirmation Input Bridge | M0 | 是 | 是 | search、注入 type/raw | confirmation_*、next_effect | 是（终端态改写） | 完整 NLU/多轮 |
| Object Temporal Ledger | M0/M1.5 | 是 | 是 | smap、evidence、hypothesis、ctx | focus_object_entry、events | 是 | 多对象/持久化 |
| Evidence Ledger | M0 | 是 | 是 | smap、relations、mix、filt、pools 等 | entries、claim、suggested_next_check | 是 | 学习型权重/长期 |
| Hypothesis Layer | M0 | 是 | 是 | evidence、smap 等 | hypotheses、verification_hint | 是 | 学习型排序/长期 |
| Recheck Planner | M0 | 是 | 是 | hypothesis、evidence、state | recheck_action/reason/target | 是 | 多步 planner |
| Recheck Whitebox Trace | M0 | 是 | 是 | recheck_planner + action_hint + confirmation + state | reasoning/weights/exclusion/interaction | 否（审计层） | 其他补证模块接入 |
| Action Hint Whitebox Trace | M0 | 是 | 是 | action_hint_copy + search + grid + confirmation + sidecar | reasoning/weights/exclusion/interaction + user_visible_explanation | 否（审计层） | 用户可见层线上对接 |
| Confirmation Whitebox Trace | M0 | 是 | 是 | confirmation_input_bridge + action_hint + search +（可选）recheck/grid | reasoning/weights/exclusion/interaction + user_visible_explanation | 否（审计层） | NLU/多轮对话 |
| Task Arbitration | M0 | 是 | 是 | goal、state、search、recheck 等 | arbitration_action、foreground_task_type | 是 | 多任务执行器 |
| Task Bundle | M0 | 是 | 是 | arbitration、smap、search 等 | bundle_* | 是 | bundle 执行图 |
| Task Chain Bridge | M0 | 是 | 是 | arbitration、bundle、search | task_chain_* | 是 | 正式 Task Chain 主体 |
| Experience Evolution | M0/M1 | 是 | 是 | ledger、hypothesis、search、state 等 | candidates、snapshot | 只读 | 长期库/反写策略 |
| Mainline Integration | M0 | 是 | 是 | bridge、arbitration、bundle、search 等 | integration_* | 是 | 全量接管 |
| Skeleton Mix | M0 | 是 | 是 | goal、scene、state 等 | dominant_skeleton、weights | 是 | 学习型权重 |
| Skeleton Filter | M0 | 是 | 是 | skeleton_mix | keep/suppress、granularity | 是 | 与 detector 主链联动 |
| Spatial Memory Pools | M0 | 是 | 是 | mix、filter、smap 等 | working/episode/stable/anchor | 是 | 持久化/Value Decay |
| Spatial Forgetting | M0 | 是 | 是 | pools、goal 等 | forgetting_* | 是 | Stable/Anchor 深化 |
| LocalGoalSpatialMap | M0/M1/M1.5 | 是 | 是 | goal、state、inputs 等 | 四类区域、标尺 | 是 | 3D/全局地图 |
| LocalGoalSpatialRelations | M2 | 是 | 是 | smap | relations | 是 | 复杂拓扑 |
| Scene Gate + 人工校准 | v1 | 是 | 是 | state、domain_guard 等 | goal_progress_paused、human_check_* | 是 | — |
| Reasoning Console | M0 | 是 | 是 | decision_monitor JSONL/frame | ReasoningConsoleSnapshot + API + UI | 工具入口 | 权限/回放/统计 |
| Reasoning Structure Tree | M0 | 是 | 是 | frame（聚合）+ whitebox + evidence/hypothesis | ReasoningStructureTreeResult | 控制台展示 | 剪枝/质量/精度优化 |
| Evidence / Hypothesis Whitebox Trace | M0 | 是 | 是 | evidence_ledger + hypothesis_layer + feedback | EvidenceHypothesisWhiteboxTraceResult | 白盒 + 树挂接 | 权重解释精度/剪枝策略 |
| Experience Governance Whitebox Trace | M0 | 是 | 是 | experience_evolution + feedback | ExperienceGovernanceWhiteboxTraceResult | 白盒 + 树挂接 | scope/contradiction/重复度治理完善 |
| Reasoning Tree Metrics | M0 | 是 | 是 | Reasoning Structure Tree | ReasoningTreeMetricsResult | 控制台指标区块 | 精度/覆盖面/趋势系统 |
| Reasoning Tree Quality Overlay | M0 | 是 | 是 | tree + metrics + 可选 feedback_loop | ReasoningTreeQualityOverlayResult | 控制台树区块内（与树一体） | 质量叠加在树上，非独立评分系统 |
| Reasoning Timeline View | M0 | 是 | 是 | frame（tree/metrics/quality/recheck/feedback/continuity/optimization） | ReasoningTimelineViewResult | 控制台结构树附近区块 | 复杂时序系统/回放器预留 |
| Optimization Hint / Tree Improvement Suggestion | M0 | 是 | 是 | tree + metrics + whitebox | OptimizationHintResult | 控制台建议区块 | 从诊断到优化建议 |
| Optimization Feedback Loop | M0 | 是 | 是 | hint + metrics + baseline | OptimizationFeedbackLoopResult | 控制台验证区块 | 建议→验证→沉淀候选 |
| Knowledge Dual-Channel Interface Reserve | M0 | 是 | 是 | hint + feedback_loop + metrics | KnowledgeDualChannelInterfaceResult | 控制台轻量区块 | 图书馆接入接口预留 |
| Strategy Injection Shadow | M0 | 是 | 是 | injection_slot + hint + feedback_loop + metrics + tree | StrategyInjectionShadowResult | 控制台轻量区块 | 影子验证：若未来注入策略，预估影响与风险（不执行注入） |
| Spatiotemporal Continuity Reserve | M0 | 是 | 是 | state + feedback + grid + metrics（摘要） | SpatiotemporalContinuityReserveResult | 控制台轻量区块 | 连续性影响摘要预留 |
| Environment & Task Context Reserve | M0 | 是 | 是 | search / metrics / continuity / confirmation / recheck / action_hint / timeline | EnvironmentTaskContextReserveResult | Console/Viewer 前提层 + 树根/树摘要/时间轴 | 复杂环境建模 / 任务引擎 |
| Memory vs Novel Information Channel | M0 | 是 | 是 | frame（只读：tree/metrics/vca/sidecar/ledger/feedback 等） | MemoryNovelInformationChannelResult | 控制台轻量区块 + 结构树/时间轴轻挂接 | 记忆治理/写库/检索/替换逻辑后续展开 |
| Memory Invocation Explanation | M0.3 | 是 | 否 | memory_novel + scheduled_source + task_chain + … | memory_invocation_explanation + 时间轴事件 + summary `mem=` | 否（解释层） | 记忆系统本体/写入/污染抵抗 |
| Mainline State / Phase Snapshot | M0.4 | 是 | 否 | frame（已有字段只读推导） | mainline_state_snapshot + 树 `state=`/`phase=` + 时间轴 + summary `mainline_state_summary` | 否（观测层） | 完整状态机/熔断/深结束语义 |
| Summary × Post-Processing Entry Contract | M0.5 | 是 | 否 | run_summary_reference（只读派生） | post_processing_summary_entry + reserve `summary_post_processing_entry_id` + 聚合 | 否（契约层） | 真实归类/图书馆/记忆写入 |
| Mainline Narrative Alignment | M0.6 | 是 | 否 | 同帧已落地对象（source/task/memory/mainline/summary/entry） | mainline_narrative_alignment + summary narrative brief + 聚合 readable | 否（表达对齐层） | 新证据层/新算法 |
| Decision Contamination Guard Reserve | M0 | 是 | 是 | frame（只读聚合） | decision_contamination_guard_reserve | Console/Viewer 占位区块 + 时间轴/树摘要 | 污染判定/溯源/图谱/清洗/议会实现 |
| Post-Processing Intelligence Reserve | M0 | 是 | 是 | frame（只读聚合） | post_processing_intelligence_reserve | Console/Viewer 占位区块 + 时间轴/树摘要 + runtime 摘要字段 | 真实归类/归因/筛选/图书馆与记忆写入 |
| Trace × Summary Separation（run_summary_reference） | M0.2 | 是 | 否 | 完整 frame（主链/时间轴/通道/调度等已有字段） | run_summary_reference + 三层 one-liner | 否（总结入口/观测） | 独立总结服务/图书馆真接入 |
| Task Chain State Snapshot | M0 / M0.1 | 是 | 否 | bridge/search/goal/arb/env task context | task_chain_state_snapshot + task_state 调度摘要 + 位置解释字段/时间轴事件 | 否（上下文源） | 任务引擎/熔断/归类深机制 |
| Scenario Benchmark & Evaluation Harness | M0 | 是 | 是 | 主线 frame（tree/metrics/quality/hint/loop） | ScenarioBenchmarkResult + summary | 工具脚本（CLI/JSON） | 大规模平台/多版本实验 |
| Real Scenario Pack | M0 / M0.8 | 是 | 是 | snapshot_json / ctx_json /（预留 image/trace） | ScenarioBenchmarkResult + real summary | 工具脚本（CLI/JSON） | 自动采样/大规模清洗/回归平台；第八批 `docs/REAL_SCENARIO_PACK_M0_7_M6_DELIVERY.md`；第九批 `docs/REAL_SCENARIO_PACK_M0_8_M7_DELIVERY.md` |
| Benchmark Triage Board | M0 | 是 | 是 | benchmark results JSON（ScenarioBenchmarkResult） | BenchmarkTriageBoardResult | 工具脚本（CLI/JSON） | 工单/派单/趋势大盘 |

**主链消费**：该模块产出是否被主流程（含 search/arbitration/mainline）直接消费。  
**仍预留**：该模块在本阶段未实现或明确不做的能力。

## 阶段收口（Reasoning Backbone Phase Closure）

- 一期收口基线文档：`docs/REASONING_BACKBONE_PHASE_CLOSURE_M1.md`

## 决策污染观察占位（Decision Contamination Guard Reserve）

- 交付：`docs/DECISION_CONTAMINATION_GUARD_RESERVE_M0.md`

## 后置信息处理占位（Post-Processing Intelligence Reserve）

- 交付：`docs/POST_PROCESSING_INTELLIGENCE_RESERVE_M0.md`

## 场景评测支架（Scenario Benchmark Harness）

- 场景基准包 + 评测支架：`docs/SCENARIO_BENCHMARK_EVALUATION_HARNESS_M0_DELIVERY.md`

## 真实场景基线重刷（Post-Fix Rebaseline M0）

- **定点 sprint（M0.1 Recheck / M0.2 Confirmation / M0.3 Hypothesis）之后**的统一整包重刷结论与 before/after 摘要：`docs/POST_FIX_REBASELINE_M0.md`。
- **产物（默认在 `logs/`，gitignore）**：`real_scenario_pack_postfix_m0.json`、`benchmark_triage_board_postfix_m0.json`；复现命令见该文档 §1。

## 第二批真实场景修复后基线重刷（Post-Fix Rebaseline M0.1）

- **Real Scenario Pack M0.1 + Targeted Fix Sprint M0.5 之后**的 10-case 整包重刷与分诊对照：`docs/POST_FIX_REBASELINE_M0_1.md`。
- **产物（默认在 `logs/`，gitignore）**：`real_scenario_pack_postfix_m01.json`、`benchmark_triage_board_postfix_m01.json`。

## 备注（测试闭环）

- Action Hint Whitebox Trace（M0）：**单测 4/4 通过**（`tests/test_action_hint_whitebox_trace.py`）+ **smoke/JSONL 验证通过**（`tools/smoke_action_hint_whitebox_trace.py` 生成 `logs/smoke_action_hint_whitebox_trace_*.jsonl`，frame 含 `action_hint_whitebox_trace`）。
- Confirmation Whitebox Trace（M0）：**单测通过**（`tests/test_confirmation_whitebox_trace.py`）+ **smoke/JSONL 验证通过**（`tools/smoke_confirmation_whitebox_trace.py` 生成 `logs/smoke_confirmation_whitebox_trace_*.jsonl`，frame 含 `confirmation_whitebox_trace`）。
- Real Scenario Pack + Benchmark Triage（Post-Fix M0）：**整包已重刷**（6/6 `passed_cases`）；摘要与 R1/R5/R6 对照见 `docs/POST_FIX_REBASELINE_M0.md`。
- Real Scenario Pack M0.1（第二批真实场景扩充）：扩充阶段曾出现 `high_dead_branch_ratio=2`（见 `docs/REAL_SCENARIO_PACK_M0_1_DELIVERY.md`）；**M0.5 后 Post-Fix 重刷**整包 `none×10`、分诊清空，见 `docs/POST_FIX_REBASELINE_M0_1.md`。
- Real Scenario Pack M0.2/M1（第三批真实场景扩充）：16-case 整包已重跑；新问题分布为 `blocked_without_resolution=3`，当前 triage 热点迁移到 `recheck_planner`，见 `docs/REAL_SCENARIO_PACK_M0_2_M1_DELIVERY.md`。
- Post-Fix Rebaseline M0.2/M1（第三批修复后重刷）：M0.6 后 16-case 整包 `passed_cases=16`、`issue_type_distribution=none×16`，`R11/R14/R16` 已退出问题集合，见 `docs/POST_FIX_REBASELINE_M0_2_M1.md`。
- Real Scenario Pack M0.3/M2（第四批真实场景扩充）：22-case 整包已重跑；本轮出现 `blocked_without_resolution=6`，热点模块为 `recheck_planner`，见 `docs/REAL_SCENARIO_PACK_M0_3_M2_DELIVERY.md`。
- Post-Fix Rebaseline M0.3/M2（第四批修复后重刷）：M0.7 后整包 `passed_cases=22`、`issue_type_distribution=none×22`；分诊清空（`ranked_modules=[]`、`ranked_issues=[]`），见 `docs/POST_FIX_REBASELINE_M0_3_M2.md`。
- Real Scenario Pack M0.4/M3（第五批真实场景扩充）：28-case 整包已重跑；本轮 `blocked_without_resolution=6`，热点模块为 `recheck_planner`，见 `docs/REAL_SCENARIO_PACK_M0_4_M3_DELIVERY.md`。
- Post-Fix Rebaseline M0.4/M3（第五批修复后重刷）：M0.8 后整包 `passed_cases=28`、`issue_type_distribution=none×28`；分诊清空（`ranked_modules=[]`、`ranked_issues=[]`），见 `docs/POST_FIX_REBASELINE_M0_4_M3.md`。
- Real Scenario Pack M0.5/M4（第六批真实场景扩充）：34-case 整包重跑；本轮 `blocked_without_resolution=6`，`passed_cases=28`，分诊热点重新聚焦 `recheck_planner`，见 `docs/REAL_SCENARIO_PACK_M0_5_M4_DELIVERY.md`。
- Post-Fix Rebaseline M0.5/M4（第六批真实场景修复后重刷）：M0.9 后整包 `passed_cases=34`、`issue_type_distribution=none×34`；分诊清空（`ranked_modules=[]`、`ranked_issues=[]`），见 `docs/POST_FIX_REBASELINE_M0_5_M4.md`。
- Real Scenario Pack M0.6/M5（第七批真实场景扩充）：40-case 整包重跑；本轮 `blocked_without_resolution=6`，热点模块为 `recheck_planner`，见 `docs/REAL_SCENARIO_PACK_M0_6_M5_DELIVERY.md`。
- Post-Fix Rebaseline M0.6/M5（第七批真实场景修复后重刷）：M1.0 后整包 `passed_cases=40`、`issue_type_distribution=none×40`；分诊清空（`ranked_modules=[]`、`ranked_issues=[]`），见 `docs/POST_FIX_REBASELINE_M0_6_M5.md`。
- Real Scenario Pack M0.7 / M6（第八批真实场景扩充）：46-case 整包；扩包阶段曾出现 `blocked_without_resolution=6`（R41–R46），热点 `recheck_planner`，见 `docs/REAL_SCENARIO_PACK_M0_7_M6_DELIVERY.md`。
- Post-Fix Rebaseline M0.7 / M6（第八批 + M1.1 后重刷）：整包 `passed_cases=46`、`issue_type_distribution=none×46`；分诊在 issue/module 维度清空（`ranked_modules=[]`、`ranked_issues=[]`），见 `docs/POST_FIX_REBASELINE_M0_7_M6.md`；产物：`logs/real_scenario_pack_postfix_m07.json`、`logs/benchmark_triage_board_postfix_m07.json`。
- Real Scenario Pack M0.8 / M7（第九批真实场景扩充）：52-case 整包；扩包阶段曾出现 `blocked_without_resolution=6`（R47–R52），热点 `recheck_planner`，见 `docs/REAL_SCENARIO_PACK_M0_8_M7_DELIVERY.md`。
- Post-Fix Rebaseline M0.8 / M7（第九批 + M1.2 后重刷）：整包 `passed_cases=52`、`issue_type_distribution=none×52`；分诊在 issue/module 维度清空，见 **`docs/POST_FIX_REBASELINE_M0_8_M7.md`**（定点收口规则见 `docs/TARGETED_FIX_SPRINT_M1_2_RECHECK_M08_EXPECTED_BLOCKED.md`）；产物：`logs/real_scenario_pack_postfix_m08.json`、`logs/benchmark_triage_board_postfix_m08.json`。
