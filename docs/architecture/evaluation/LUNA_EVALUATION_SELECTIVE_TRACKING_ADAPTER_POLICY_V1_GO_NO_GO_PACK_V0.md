# Luna — GO / NO_GO Pack: Selective Tracking Adapter Policy v1

## GO 条件

- `world_observation_entity_feature_input_loaded=true`
- `task_aware_visual_focus_input_loaded=true`
- `midplatform_perception_orchestration_input_loaded=true`
- `return_to_vision_planning_input_loaded=true`
- `preplan_input_loaded=true`
- `selective_tracking_adapter_policy_defined=true`
- `tracking_request_candidate_schema_defined=true`
- `tracklet_candidate_schema_defined=true`
- `tracking_budget_policy_defined=true`
- `tracking_target_admission_policy_defined=true`
- `road_surface_tracking_policy_defined=true`
- `pedestrian_vehicle_tracking_policy_defined=true`
- `crowd_flow_tracking_policy_defined=true`
- `traffic_light_crossing_tracking_policy_defined=true`
- `tracking_adapter_candidate_registry_defined=true`
- `tracking_lifecycle_policy_defined=true`
- `tracking_feedback_policy_defined=true`
- `scenario_matrix_generated=true`
- `scenario_count>=10`
- `tracking_authority_owner=MidPlatform`
- `full_scene_tracking_allowed=false`
- `all_moving_objects_tracking_allowed=false`
- `all_person_tracking_allowed=false`
- `all_vehicle_tracking_allowed=false`
- `crowd_flow_follow_action_allowed=false`
- `traffic_light_crossing_action_allowed=false`
- `tracking_request_candidate_only=true`
- `tracklet_candidate_not_fact=true`
- `external_tracking_adapters_future_candidate_only=true`
- `worldmodel_handoff_candidate_allowed=true`
- `memory_handoff_candidate_allowed=true`
- `library_handoff_placeholder_allowed=true`
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
- `tracking_runtime_enabled=false`
- `supervision_imported=false`
- `supervision_invoked=false`
- `bytetrack_imported=false`
- `bytetrack_invoked=false`
- `ocsort_imported=false`
- `ocsort_invoked=false`
- `sort_invoked=false`
- `botsort_invoked=false`
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
- `final_decision=SELECTIVE_TRACKING_ADAPTER_POLICY_READY_FOR_VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN`
- `recommended_next_phase=Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001`

## NO_GO 条件

- 未加载 `World Observation and Entity Feature Policy`
- 未加载 `Task-Aware Visual Focus Policy`
- 未加载 `MidPlatform Perception Orchestration Policy`
- 未加载 `Return-To-Vision Mainline Planning`
- 未加载 `preplan`
- 未定义 `SelectiveTrackingAdapterPolicy / TrackingRequestCandidate / TrackletCandidate`
- 未定义 tracking budget / admission / lifecycle / feedback policy
- 未定义 `RoadSurface / PedestrianVehicle / CrowdFlow / TrafficLightCrossing` tracking policy
- 未定义 `TrackingAdapterCandidateRegistry`
- 场景矩阵少于 10 个
- 允许 `full scene` 或 `all moving objects` tracking
- 建议本阶段直接接 `Supervision / ByteTrack / OC-SORT / optical flow runtime`
- 建议本阶段直接触发 tracking runtime
- 建议本阶段直接导航
- 建议本阶段直接写 `WorldModel / Memory / Fact / Library`
- 未记录 `governance debt`
- 未固定下一阶段

## 判定语义

### GO

说明 Selective Tracking Adapter Policy 已正式成立，可以继续切入：

- `Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001`

### NO_GO

说明当前仍停留在 selective tracking policy review，必须先补齐 admission、budget、adapter registry、scenario matrix、boundary 或治理债务登记。

## 明确边界

即使 `GO`，本阶段也 **不等于**：

- 已接 `camera`
- 已接 `OCR provider`
- 已接 tracking runtime
- 已接 `map API`
- 已导入 `Supervision / ByteTrack / OC-SORT`
- 已执行 `optical flow runtime`
- 已提交 `OCRRequest`
- 已执行 `entity resolution / fact admission / memory consolidation`
- 已写入 `WorldModel / Memory / Fact / Library`
- 已生成真实导航指令

本阶段 `GO` 只表示：

- `SelectiveTrackingAdapterPolicy` 已冻结
- `TrackingRequestCandidate → TrackletCandidate → TrackingFeedbackCandidate` 链已定义
- tracking authority 继续由 `MidPlatform` 持有
- 外部 tracking adapter 继续保持 `future_candidate`
- tracking 结果继续保持 `candidate-only / no-fact / no-write`
