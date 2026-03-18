# Phase 2 模块状态总表（Status Matrix）

快速查阅用；偏表格化，非长 prose。

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

**主链消费**：该模块产出是否被主流程（含 search/arbitration/mainline）直接消费。  
**仍预留**：该模块在本阶段未实现或明确不做的能力。
