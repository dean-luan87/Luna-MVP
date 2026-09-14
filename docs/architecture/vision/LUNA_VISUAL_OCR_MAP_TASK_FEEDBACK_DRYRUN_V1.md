# Luna — Visual OCR Map Task Feedback DryRun v1

**Phase**：`Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001`  
**性质**：dry-run / candidate / no-runtime / no-write only  
**边界**：不接真实 runtime，不调用 `camera`，不调用视觉模型，不调用 `OCR provider`，不提交 `OCRRequest`，不调用地图 API / 高德 API，不调用 tracking runtime，不调用 optical flow runtime，不导入或调用 `Supervision / ByteTrack / OC-SORT`，不写 `Memory` / `WorldModel` / `Fact` / `Library`，不做 `entity resolution`，不做 `fact admission`，不做 `memory consolidation`，不做 `library experience commit`，不生成 `Scene Delta`，不提交 `Task State`，不触发 `Navigation Action`，不调用 `Speech Gate / VOP / TTS`

## 阶段定位

本阶段把前面几条 policy 首次在中台层串起来，但仍然只做 dry-run：

任务信息  
+ 中台感知工作单  
+ 视觉焦点候选  
+ OCR activation candidate  
+ tracking request candidate  
+ map / memory context hint  
↓  
`TaskFeedbackCandidate / SafetyFeedbackCandidate`

本阶段回答：

1. 中台感知工作单能否驱动视觉焦点候选。
2. `VisualFocusSlot` 能否生成 `OCR activation request candidate`。
3. `VisualFocusSlot` 能否生成 `tracking request candidate`。
4. `map / route / location / memory hint` 如何参与任务反馈。
5. `tracking request / tracklet candidate` 如何进入 feedback，而不是直接行动。
6. `OCR activation candidate` 如何进入 feedback，而不是提交 `OCRRequest`。
7. `WorldObservation / EntityFeature` 如何进入 handoff feedback，而不是写 `WorldModel`。
8. 视觉 / OCR / 地图 / 记忆冲突如何生成 `conflict / correction feedback`。
9. 低质量视角如何生成 `ActiveViewAdjustment feedback`。
10. 过街、找商店、找东西、拥挤遮挡等场景能否形成正确候选。
11. dry-run 链路是否保持 `no-runtime / no-write / no-fact`。

## 输入 roots

本阶段正式依赖：

- `_eval_out/selective_tracking_adapter_policy_v1_smoke_v0/`
- `_eval_out/world_observation_and_entity_feature_policy_v1_smoke_v0/`
- `_eval_out/task_aware_visual_focus_policy_v1_smoke_v0/`
- `_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0/`
- `_eval_out/return_to_vision_mainline_planning_v1_smoke_v0/`
- `_eval_out/return_to_vision_mainline_preplan_v1/`
- `_eval_out/ocr_mainline_final_closure_v1_smoke_v0/`
- `_eval_out/minimal_runtime_integration_closure_v1_smoke_v0/`

并引用：

- `docs/architecture/vision/LUNA_SELECTIVE_TRACKING_ADAPTER_POLICY_V1.md`
- `docs/architecture/vision/LUNA_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_V1.md`
- `docs/architecture/vision/LUNA_TASK_AWARE_VISUAL_FOCUS_POLICY_V1.md`
- `docs/architecture/midplatform/LUNA_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_V1.md`
- `docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PLANNING_V1.md`
- `docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PREPLAN_V1.md`
- `docs/architecture/ocr/LUNA_OCR_MAINLINE_FINAL_CLOSURE_V1.md`
- `docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CLOSURE_V1.md`
- `docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md`

## Core Object 1: VisualOcrMapTaskFeedbackDryRunCase

关键字段：

- `dryrun_case_id`
- `case_type`
- `simulated_task_context`
- `simulated_task_phase`
- `simulated_scene_sketch_ref`
- `simulated_visual_focus_plan_ref`
- `simulated_visual_focus_slots`
- `simulated_view_quality_ref`
- `simulated_map_context_hint`
- `simulated_memory_context_hint`
- `simulated_ocr_activation_candidate`
- `simulated_tracking_request_candidate`
- `simulated_world_observation_candidate`
- `expected_feedback_candidates`
- `expected_boundary_flags`
- `source_chain`

## Core Object 2: FeedbackFusionCandidate

该对象把视觉 / OCR activation / tracking / map hint / memory hint / world observation 候选合成为中台反馈候选。

关键字段：

- `feedback_fusion_candidate_id`
- `source_case_id`
- `related_task_id`
- `task_phase`
- `visual_refs`
- `ocr_activation_refs`
- `tracking_refs`
- `map_hint_refs`
- `memory_hint_refs`
- `world_observation_refs`
- `conflict_refs`
- `correction_refs`
- `confidence`
- `freshness_status`
- `uncertainty`
- `requires_arbitration=true`
- `speech_allowed=false`
- `action_allowed=false`
- `fact_status=not_fact`
- `source_chain`

## Core Object 3: TaskFeedbackCandidate

`feedback_type` 至少覆盖：

- `route_alignment_feedback`
- `destination_approach_feedback`
- `target_search_feedback`
- `target_confirmation_feedback`
- `object_search_feedback`
- `shopfront_search_feedback`
- `view_adjustment_needed`
- `map_memory_conflict_feedback`
- `ocr_activation_needed`
- `tracking_needed`
- `world_observation_handoff_feedback`

核心要求：

- 任务反馈只作为 candidate
- `requires_speech_gate=true`
- `action_allowed=false`
- 不等于导航动作

## Core Object 4: SafetyFeedbackCandidate

`safety_type` 至少覆盖：

- `near_field_obstacle`
- `vehicle_approach`
- `pedestrian_approach`
- `crossing_uncertain`
- `traffic_light_uncertain`
- `route_surface_occluded`
- `crowd_flow_risk`
- `view_quality_poor`

核心要求：

- `requires_safety_task_arbitration=true`
- `speech_allowed=false until gate`
- `action_allowed=false`

## Core Object 5: OCRActivationFeedbackCandidate

关键要求：

- 该候选不提交 `OCRRequest`
- 不调用 `OCR provider`
- 只是把 OCR activation need 回传中台

## Core Object 6: TrackingFeedbackCandidate

关键要求：

- `candidate_only=true`
- `tracking_runtime_allowed=false`
- `full_scene_tracking_allowed=false`
- `action_allowed=false`
- 不等于 tracking runtime 执行

## Core Object 7: MapMemoryContextFeedbackCandidate

该对象只表达 map / memory hint 对当前任务阶段的支持或冲突，不得写事实，不得直接行动。

## Core Object 8: ConflictCorrectionFeedbackCandidate

该对象只表达 `map / memory / visual / OCR` 冲突及 correction candidate，不做 fact update。

## Core Object 9: ActiveViewAdjustmentFeedbackCandidate

该对象只表达视角质量差时的用户引导候选，例如：

- `center_target`
- `hold_still`

核心要求：

- `speech_gate_required=true`
- `action_allowed=false`

## Core Object 10: DryRunBoundaryDecision

每个 dry-run case 必须明确：

- `runtime_boundary_ok`
- `write_boundary_ok`
- `action_boundary_ok`
- `speech_boundary_ok`
- `worldmodel_boundary_ok`
- `memory_boundary_ok`
- `library_boundary_ok`
- `violations`

## Dry-Run 场景矩阵

本阶段至少覆盖 10 个场景：

1. `navigation_route_walking_clear_path`
2. `navigation_approaching_destination_with_signage`
3. `shop_search_right_side_storefront`
4. `object_search_home_keys`
5. `home_familiar_object_interaction`
6. `crowded_path_occluded_surface`
7. `crossing_uncertain_traffic_light`
8. `temporary_mobile_vendor_near_route`
9. `visual_map_memory_conflict`
10. `low_quality_view_requires_hold_still`

其中必须继续保持：

- 清晰路径场景只生成 `route_alignment_feedback`
- 接近目标且有标识时只生成 `destination_approach_feedback + OCRActivationFeedbackCandidate`
- 商店搜索时允许 `ActiveViewAdjustment feedback`
- 家庭找物场景必须带 `privacy filtering required`
- 熟悉物体交互只允许 `world_observation_handoff_feedback`
- 拥挤遮挡场景只能给 `crowd_flow risk / route_surface_occluded`
- 过街不确定场景不输出过街动作指令
- 临时设施场景必须 `TTL required`
- 地图 / 记忆 / 视觉冲突只生成 `conflict/correction feedback`
- 低质量视角必须 `hold_still`，并抑制任务视觉反馈

## Runtime / Write Boundary

本阶段必须保持：

- `dryrun_only=true`
- `no_runtime_executed=true`
- `no_new_runtime_enabled=true`
- `camera_invoked=false`
- `map_api_invoked=false`
- `ocr_provider_invoked=false`
- `ocrrequest_submitted=false`
- `tracking_runtime_invoked=false`
- `optical_flow_runtime_invoked=false`
- `supervision_imported=false`
- `supervision_invoked=false`
- `bytetrack_imported=false`
- `bytetrack_invoked=false`
- `ocsort_imported=false`
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
- `tts_invoked=false`

## Final Verdict

当 runner / verifier 全部通过时，本阶段正式结论为：

- `final_decision=VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN_READY_FOR_BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING`
- `phase verdict=GO`
- `recommended_next_phase=Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001`

这表示：

- 视觉 / OCR / 地图 / 记忆 / tracking candidate / 任务反馈 dry-run 链首次在中台层串起来
- 仍然只是 `dry-run / candidate / no-runtime / no-write`
- 下一阶段进入基础导航闭环的视觉强化 dry-run

当前状态更新：

- `Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001 = GO`
- `Phase-Basic-Navigation-Loop-Vision-Strengthening-Post-DryRun-Review-v1-001 = GO`
- `Phase-Basic-Navigation-Loop-Vision-Strengthening-Closure-v1-001 = GO`
- 当前推荐下一阶段：`Phase-Post-Vision-Strengthening-Roadmap-Decision-v1-001`
