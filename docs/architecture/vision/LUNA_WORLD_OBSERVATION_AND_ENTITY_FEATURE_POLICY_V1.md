# Luna — World Observation and Entity Feature Policy v1

**Phase**：`Phase-World-Observation-and-Entity-Feature-Policy-v1-001`  
**性质**：policy / schema / contract / boundary only  
**边界**：不实现 `World Observation runtime`，不调用视觉模型，不接 `camera`，不接 `OCR provider`，不接地图 API / 高德 API，不接 tracking runtime，不接 optical flow runtime，不调用 `Supervision / ByteTrack / OC-SORT`，不写 `Memory` / `WorldModel` / `Fact` / `Library`，不做 `entity resolution`，不做 `fact admission`，不做 `memory consolidation`，不做 `library experience commit`，不做 `object identity fact commit`，不做 `emotional attachment fact commit`，不生成 `Scene Delta`，不提交 `Task State`，不触发 `Navigation Action`

## 阶段定位

本阶段用于正式冻结 Luna 视角强化主线里的“后台世界观察与世界实体特征候选 policy”。它承接：

`MidPlatformPerceptionWorkOrder`  
↓  
`SceneSketchCandidate`  
↓  
`VisualFocusPlan`  
↓  
`VisualFocusSlot`  
↓  
`VisualObservationLifecyclePolicy`

并继续定义：

`WorldObservationLayerPolicy`  
↓  
`WorldObservationCandidate`  
↓  
`WorldEntityFeatureCandidate`  
↓  
`ObjectIdentityCandidate / TemporaryFacilityCandidate / EmotionalAttachmentCandidate`  
↓  
`WorldModelHandoffCandidate / MemoryHandoffCandidate / LibraryHandoffPlaceholder`

本阶段回答：

1. `World Observation Layer` 在当前视觉主线中的边界是什么。
2. 后台世界观察如何低频生成候选，而不进入实时行动链。
3. `WorldObservationCandidate` 如何表达道路、地点、设施、场景变化、路线经验等候选。
4. `WorldEntityFeatureCandidate` 如何表达 `object / place / event / relation / facility / temporary facility` 等实体特征。
5. `ObjectIdentityCandidate` 如何只作为长期对象身份候选，不写事实。
6. `Temporary / Mobile Social Facility` 如何 TTL 化。
7. `EmotionalAttachmentCandidate` 如何只作为候选，不写情感事实。
8. `WorldModel / Memory / Library handoff placeholder` 如何保留但不执行。
9. 世界观察候选如何进入 `active / stale / expired / archived_candidate` 延伸生命周期。
10. 如何避免 `World Observation` 退化成 `full background recording`。
11. 如何继续保持 `entity resolution / fact admission / memory consolidation / library governance deferred`。

## 输入 roots

本阶段正式依赖：

- `_eval_out/task_aware_visual_focus_policy_v1_smoke_v0/`
- `_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0/`
- `_eval_out/return_to_vision_mainline_planning_v1_smoke_v0/`
- `_eval_out/return_to_vision_mainline_preplan_v1/`
- `_eval_out/ocr_mainline_final_closure_v1_smoke_v0/`
- `_eval_out/minimal_runtime_integration_closure_v1_smoke_v0/`

并引用：

- `docs/architecture/vision/LUNA_TASK_AWARE_VISUAL_FOCUS_POLICY_V1.md`
- `docs/architecture/midplatform/LUNA_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_V1.md`
- `docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PLANNING_V1.md`
- `docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PREPLAN_V1.md`
- `docs/architecture/ocr/LUNA_OCR_MAINLINE_FINAL_CLOSURE_V1.md`
- `docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CLOSURE_V1.md`
- `docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md`

可选复用文档若不存在，只能标记 `optional_missing`，不得失败，不得伪造能力。

## Core Object 1: WorldObservationLayerPolicy

`WorldObservationLayerPolicy` 定义底层世界观察层，只允许作为后台、低频、候选材料层存在。

关键字段：

- `policy_id`
- `scope`
- `allowed_observation_targets`
- `forbidden_observation_targets`
- `background_budget_ref`
- `privacy_policy_ref`
- `freshness_policy_ref`
- `ttl_policy_ref`
- `worldmodel_handoff_boundary_ref`
- `value_filtering_policy_ref`
- `source_chain`

必须明确：

- `background / low-frequency only`
- `not real-time action path`
- `not navigation authority`
- `not speech output source`
- `not WorldModel writer`
- `not Memory writer`
- `not Library writer`
- `only generates candidates / handoff placeholders`
- `resource budget controlled by MidPlatform`
- `privacy filtering controlled by MidPlatform`
- `STC / TTL / freshness / source_chain` 复用 OCR / MidPlatform
- `full_background_recording_allowed=false`

## Core Object 2: WorldObservationCandidate

`WorldObservationCandidate` 是世界观察候选，不是事实，不是动作，不是导航 authority。

关键字段：

- `world_observation_id`
- `source_visual_focus_slot_id`
- `source_scene_sketch_id`
- `source_visual_observation_ref`
- `observation_type`
- `observed_entity_type`
- `location_context_ref`
- `pose_or_view_context_ref`
- `task_context_ref`
- `time_window_ref`
- `freshness_status`
- `ttl_policy_ref`
- `confidence`
- `uncertainty`
- `privacy_tags`
- `value_score_ref`
- `conflict_refs`
- `visual_refs`
- `ocr_refs`
- `map_refs`
- `memory_refs`
- `current_action_allowed=false`
- `fact_status=not_fact`
- `write_allowed=false`
- `source_chain`

`observation_type` 至少覆盖：

- `route_structure_candidate`
- `road_surface_candidate`
- `walkable_path_candidate`
- `entrance_or_exit_candidate`
- `public_facility_candidate`
- `shopfront_or_signage_candidate`
- `temporary_facility_candidate`
- `environmental_pattern_candidate`
- `scene_change_candidate`
- `safety_risk_point_candidate`
- `user_relevant_place_candidate`
- `recurring_observation_candidate`

## Core Object 3: WorldObservationValueFilteringPolicy

该 policy 用于防止后台世界观察退化为全量记录。

高价值候选：

- `route_structure`
- `common_path`
- `entrance_or_exit`
- `public_facility`
- `shopfront_or_station`
- `temporary_facility`
- `scene_change`
- `safety_risk_point`
- `user_repeated_interaction_object`
- `user_confirmed_important_place_or_object`
- `OCR / map / memory conflict point`

低价值候选：

- `unrelated_background_pedestrian`
- `one-off_low_confidence_noise`
- `unlocalized_transient_background_object`
- `distant_unrelated_vehicle`
- `repeated_low_value_frame`
- `high_privacy_low_task_value_content`

必须明确：

- `full_background_recording_allowed=false`
- 高价值候选才允许进入 `archive / handoff` 链
- 低价值背景噪声可直接 `discard`
- 高隐私低任务价值内容优先丢弃或限制

## Core Object 4: WorldEntityFeatureCandidate

`WorldEntityFeatureCandidate` 表达世界中的实体特征候选，不等于实体事实。

`entity_type` 至少覆盖：

- `ObjectCandidate`
- `PlaceCandidate`
- `EventCandidate`
- `RelationCandidate`
- `FacilityCandidate`
- `SocialFacilityCandidate`
- `TemporaryFacilityCandidate`
- `RouteStructureCandidate`
- `EnvironmentalPatternCandidate`

属性分层：

- `universal_attributes`
- `task_specific_attributes`
- `user_profiled_attributes`
- `social_context_attributes`
- `emotional_attributes`
- `operational_attributes`
- `uncertainty_and_conflict`

必须明确：

- `user_profiled_attributes` 只能来自用户授权 / 配置 / 历史确认，不得由视觉默认推断敏感身份
- `emotional_attributes` 只能是候选，不得写成情感事实
- `entity feature candidate` 不等于实体事实
- 本阶段不做 `entity resolution`

## Core Object 5: ObjectIdentityCandidate

`ObjectIdentityCandidate` 是长期对象身份候选，只允许进入未来 `Memory / WorldModel` 专项治理。

关键字段：

- `object_identity_candidate_id`
- `entity_feature_candidate_ref`
- `entity_type`
- `visual_signature_refs`
- `location_context_refs`
- `ocr_refs`
- `user_alias_refs`
- `historical_interaction_refs`
- `confidence`
- `conflict_refs`
- `requires_review`
- `requires_user_confirmation`
- `fact_status=not_fact`
- `identity_fact_allowed=false`
- `source_chain`

必须明确：

- 单次观察不得生成 `identity fact`
- 当前阶段不做 `Object Identity runtime`
- 家庭物品需要 `privacy filtering`

## Core Object 6: TemporaryMobileSocialFacilityPolicy

候选类型：

- `TemporaryFacilityCandidate`
- `MobileFacilityCandidate`
- `TransientSceneStructureCandidate`
- `RecurringTemporaryPatternCandidate`

覆盖示例：

- 临时摊位
- 流动商贩
- 临时施工围挡
- 临时排队点
- 临时服务台
- 临时活动摊位
- 临时交通管制
- 临时路障
- 临时公告
- 临时公交 / 地铁改道提示
- 临时市场 / 夜市
- 临时人群聚集

核心原则：

- 临时设施默认 `TTL` 短
- 可用于当前任务 / 安全候选
- 不默认写长期 `WorldModel`
- 多次同地 / 同时间窗出现，只能升级为 `recurring temporary pattern candidate`
- `fixed_poi_commit_allowed=false`
- 必须与 `static POI` 区分

## Core Object 7: EmotionalAttachmentCandidatePolicy

`EmotionalAttachmentCandidate` 只表达情感挂载候选，不写事实。

关键字段：

- `emotional_attachment_candidate_id`
- `related_entity_feature_candidate_id`
- `attachment_type_candidate`
- `evidence_refs`
- `user_feedback_refs`
- `historical_interaction_refs`
- `confidence`
- `sensitivity_level`
- `requires_user_confirmation`
- `emotional_fact_allowed=false`
- `fact_status=not_fact`
- `source_chain`

必须明确：

- 不根据单次视觉观察推断用户情感
- 不对陌生人做情感挂载
- 情感挂载不写事实
- 后续交给情感引擎 / 记忆治理处理

## Core Object 8: WorldModelMemoryLibraryPlaceholderPolicy

当前只允许：

- `WorldModelHandoffCandidate`
- `MemoryHandoffCandidate`
- `LibraryHandoffPlaceholder`
- `ExperienceCandidatePlaceholder`

当前禁止：

- `entity_resolution_runtime`
- `fact_admission`
- `worldmodel_write`
- `memory_write`
- `library_experience_commit`
- `memory_consolidation`
- `object_identity_fact_commit`
- `emotional_attachment_fact_commit`
- `temporary_facility_long_term_promotion`
- `route_experience_commit`

必须继续保持：

- `entity_resolution_deferred=true`
- `fact_admission_deferred=true`
- `memory_consolidation_deferred=true`
- `library_experience_governance_deferred=true`
- `worldmodel_write_allowed=false`
- `memory_write_allowed=false`
- `library_write_allowed=false`
- `handoff_candidate_not_fact=true`
- `placeholder_not_runtime=true`

## Core Object 9: WorldObservationFeedbackPolicy

输出候选：

- `WorldObservationFeedbackCandidate`
- `EntityFeatureFeedbackCandidate`
- `TemporaryFacilityFeedbackCandidate`
- `ObjectIdentityFeedbackCandidate`
- `WorldModelHandoffCandidate`
- `MemoryHandoffCandidate`
- `LibraryHandoffPlaceholder`

核心原则：

- `feedback candidate` 不直接播报
- `speech_allowed=false until Speech Gate`
- `action_allowed=false`
- `fact_status=not_fact`
- `requires_arbitration_or_review=true`
- `source_chain required`

## 场景矩阵

本阶段场景矩阵固定至少覆盖 8 个场景：

1. `route_structure_observation`
2. `shopfront_entity_feature_candidate`
3. `home_familiar_object_candidate`
4. `temporary_mobile_vendor_candidate`
5. `recurring_temporary_pattern_candidate`
6. `emotional_attachment_candidate_placeholder`
7. `scene_change_candidate`
8. `low_value_background_discard`

其中必须继续保持：

- `shopfront` 只保留 `ocr refs placeholder`
- 家庭熟悉物体只允许 `ObjectIdentityCandidate placeholder`
- 临时设施 `TTL` 短且 `fixed_poi_commit_allowed=false`
- 重复出现的临时设施只允许 `RecurringTemporaryPatternCandidate`
- 场景变化只允许 `correction / handoff candidate`
- 低价值背景噪声允许 `discard_allowed=true`

## Runtime / Write Boundary

本阶段必须保持：

- `no_runtime_executed=true`
- `no_new_runtime_enabled=true`
- `world_observation_runtime_enabled=false`
- `camera_invoked=false`
- `map_api_invoked=false`
- `ocr_provider_invoked=false`
- `ocrrequest_submitted=false`
- `tracking_runtime_invoked=false`
- `optical_flow_runtime_invoked=false`
- `supervision_invoked=false`
- `bytetrack_invoked=false`
- `ocsort_invoked=false`
- `entity_resolution_runtime_invoked=false`
- `fact_admission_runtime_invoked=false`
- `memory_consolidation_invoked=false`
- `library_experience_commit_invoked=false`
- `world_model_written=false`
- `memory_written=false`
- `library_written=false`
- `fact_written=false`
- `scene_delta_generated=false`
- `task_state_committed_now=false`
- `navigation_action_triggered=false`
- `speech_gate_invoked=false`
- `vop_invoked=false`

## Final Verdict

当 runner / verifier 全部通过时，本阶段的正式结论是：

- `final_decision=WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_READY_FOR_SELECTIVE_TRACKING_ADAPTER_POLICY`
- `phase verdict=GO`
- `recommended_next_phase=Phase-Selective-Tracking-Adapter-Policy-v1-001`

这表示：

- `World Observation / Entity Feature policy` 已正式成立
- 当前只冻结 `policy / schema / contract / boundary`
- 下一阶段进入 `Selective Tracking Adapter Policy`
- 仍然不要接 runtime
- 仍然不要接 `camera / OCR provider / tracking / map API`
- 仍然不要写 `WorldModel / Memory / Fact / Library`

后续状态更新：

- `Phase-Selective-Tracking-Adapter-Policy-v1-001 = GO`
- `Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001 = GO`
- 当前推荐下一阶段：`Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001`
