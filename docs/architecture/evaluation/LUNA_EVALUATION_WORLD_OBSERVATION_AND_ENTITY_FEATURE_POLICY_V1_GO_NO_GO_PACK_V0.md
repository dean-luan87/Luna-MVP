# Luna — GO / NO_GO Pack: World Observation and Entity Feature Policy v1

## GO 条件

- `task_aware_visual_focus_input_loaded=true`
- `midplatform_perception_orchestration_input_loaded=true`
- `return_to_vision_planning_input_loaded=true`
- `preplan_input_loaded=true`
- `world_observation_layer_policy_defined=true`
- `world_observation_candidate_schema_defined=true`
- `world_observation_value_filtering_policy_defined=true`
- `world_entity_feature_candidate_schema_defined=true`
- `object_identity_candidate_schema_defined=true`
- `temporary_mobile_social_facility_policy_defined=true`
- `emotional_attachment_candidate_policy_defined=true`
- `worldmodel_memory_library_placeholder_policy_defined=true`
- `world_observation_feedback_policy_defined=true`
- `scenario_matrix_generated=true`
- `scenario_count>=8`
- `full_background_recording_allowed=false`
- `world_observation_runtime_enabled=false`
- `worldmodel_handoff_candidate_allowed=true`
- `memory_handoff_candidate_allowed=true`
- `library_handoff_placeholder_allowed=true`
- `object_identity_fact_allowed=false`
- `emotional_attachment_fact_allowed=false`
- `fixed_poi_commit_allowed=false`
- `entity_resolution_deferred=true`
- `fact_admission_deferred=true`
- `memory_consolidation_deferred=true`
- `library_experience_governance_deferred=true`
- `worldmodel_write_allowed=false`
- `memory_write_allowed=false`
- `library_write_allowed=false`
- `handoff_candidate_not_fact=true`
- `placeholder_not_runtime=true`
- `no_runtime_executed=true`
- `no_new_runtime_enabled=true`
- `world_observation_runtime_enabled=false`
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
- `boundary_ok=true`
- `future_midplatform_function_governance_required=true`
- `no_duplicate_governance_module_allowed=true`
- `final_decision=WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_READY_FOR_SELECTIVE_TRACKING_ADAPTER_POLICY`
- `recommended_next_phase=Phase-Selective-Tracking-Adapter-Policy-v1-001`

## NO_GO 条件

- 未加载 `Task-Aware Visual Focus Policy`
- 未加载 `MidPlatform Perception Orchestration Policy`
- 未加载 `Return-To-Vision Mainline Planning`
- 未加载 `preplan`
- 未定义 `WorldObservationLayerPolicy / WorldObservationCandidate`
- 未定义 `WorldObservationValueFilteringPolicy`
- 未定义 `WorldEntityFeatureCandidate / ObjectIdentityCandidate`
- 未定义 `TemporaryMobileSocialFacilityPolicy / EmotionalAttachmentCandidatePolicy`
- 未定义 `WorldModel / Memory / Library` handoff-only 边界
- 场景矩阵少于 8 个
- 允许 `full background recording`
- 建议本阶段直接接 `camera / OCR provider / tracking / map API`
- 建议本阶段调用 `Supervision / ByteTrack / OC-SORT`
- 建议本阶段执行 `entity resolution / fact admission / memory consolidation`
- 建议本阶段直接写 `WorldModel / Memory / Fact / Library`
- 未记录 `governance debt`
- 未固定下一阶段

## 判定语义

### GO

说明后台世界观察与实体特征候选主链已经正式成立，可以继续切入：

- `Phase-Selective-Tracking-Adapter-Policy-v1-001`

### NO_GO

说明当前仍停留在 `world observation / entity feature policy review`，必须先补齐 schema、value filtering、scenario matrix、handoff boundary 或治理债务登记。

## 明确边界

即使 `GO`，本阶段也 **不等于**：

- 已接 `camera`
- 已接 `OCR provider`
- 已接 `tracking runtime`
- 已接 `map API`
- 已提交 `OCRRequest`
- 已执行 `Supervision / ByteTrack / OC-SORT`
- 已执行 `entity resolution / fact admission / memory consolidation`
- 已写入 `WorldModel / Memory / Fact / Library`
- 已提交 `object identity fact`
- 已提交 `emotional attachment fact`
- 已把临时设施升级为固定 `POI`

本阶段 `GO` 只表示：

- `WorldObservationLayerPolicy` 已冻结
- `WorldObservationCandidate → WorldEntityFeatureCandidate → ObjectIdentity / TemporaryFacility / EmotionalAttachment → WML handoff placeholder` 链已定义
- 后台观察仍然只是 candidate / placeholder
- `WorldModel / Memory / Library` 继续保持 `handoff-only / placeholder-only`
