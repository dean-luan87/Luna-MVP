# Luna — Controlled Frame Input Planning v1

**Phase**：`Phase-Controlled-Frame-Input-Planning-v1-001`  
**性质**：planning / schema / boundary / readiness only  
**边界**：不实现 `camera runtime`，不读取真实相机，不调用视觉模型，不调用 `OCR provider`，不提交 `OCRRequest`，不调用地图 API / 高德 API，不调用 GPS runtime，不调用 tracking runtime，不调用 optical flow runtime，不导入或调用 `Supervision / ByteTrack / OC-SORT`，不写 `Memory` / `WorldModel` / `Fact` / `Library`，不做 `entity resolution`，不做 `fact admission`，不做 `memory consolidation`，不做 `library experience commit`，不生成 `Scene Delta`，不提交 `Task State`，不触发 `Navigation Action`，不调用 `Speech Gate / VOP / TTS`，不输出真实用户可听语音

## 目标

本阶段定义 Luna 视觉主线中的 `Controlled Frame Input Planning`。

它只回答：

- 帧从哪里来
- 能不能进入视觉链
- 如何标记来源、timestamp、source_chain、device context、privacy tags
- 如何进入 `ViewQualityGate`
- 如何进入 `SceneSketchCandidate`
- 如何进入 `VisualFocusPlan`
- 如何进入 `OCR activation candidate`
- 如何进入 `tracking request candidate`
- 如何进入 `WorldObservationCandidate`
- 什么条件下 frame input 被拒绝
- 什么条件下 frame input 只能用于测试
- 如何为后续 `Controlled Frame Input DryRun` 做准备

必须明确：

- `Controlled Frame Input Planning` 不等于 `camera runtime`
- 当前不接 `live camera`
- 当前不打开摄像头
- 当前不读取真实设备流
- 当前不做真实帧推理

## ControlledFrameInputPlanningPolicy

允许的 frame source：

- `static_test_image`
- `pre_recorded_video_frame`
- `simulation_frame`
- `synthetic_frame`
- `archived_frame_candidate`
- `controlled_uploaded_frame`

当前禁止的 frame source：

- `live_camera_placeholder`
- `device_camera_placeholder`
- `external_stream_placeholder`

必须明确：

- `live_camera_placeholder allowed_now=false`
- `device_camera_placeholder allowed_now=false`
- `external_stream_placeholder allowed_now=false`

## FrameSourceCandidate

`FrameSourceCandidate` 用于表达帧来源，而不是直接读取 runtime。

必须带：

- `source_type`
- `source_origin`
- `source_trust_level`
- `frame_access_mode`
- `allowed_now`
- `runtime_required`
- `privacy_risk`
- `test_only`
- `task_use_allowed_candidate`
- `world_observation_use_allowed_candidate`
- `fact_status=not_fact`

## ControlledFrameInputCandidate

`ControlledFrameInputCandidate` 必须带：

- `frame_source_candidate_ref`
- `frame_id`
- `frame_timestamp`
- `monotonic_seq`
- `source_time_ref`
- `location_context_ref`
- `pose_or_view_context_ref`
- `device_context_ref`
- `task_context_ref`
- `privacy_tags`
- `quality_status_candidate`
- `freshness_status`
- `ttl_policy_ref`
- `frame_hash_placeholder`
- `storage_policy`
- `downstream_allowed_targets`
- `runtime_action_allowed=false`
- `fact_status=not_fact`

允许的 downstream target：

- `view_quality_candidate`
- `scene_sketch_candidate`
- `visual_focus_plan_candidate`
- `ocr_activation_candidate`
- `tracking_request_candidate`
- `world_observation_candidate`
- `debug_visualization_candidate`

## Frame Intake Gate

允许条件：

- source allowed
- `source_chain` present
- `timestamp` present
- `privacy tags` present
- `task context` present or explicitly taskless background context
- quality status computable or `unknown-but-marked`
- no live runtime required
- no write side effect
- no direct output side effect

拒绝条件：

- unknown source
- missing `source_chain`
- missing `timestamp`
- live camera attempt
- external stream attempt
- privacy tags missing
- task context missing without background policy
- frame tries to trigger runtime
- frame tries to write fact
- frame tries to bypass `MidPlatform`

## Frame Quality Gate

质量维度：

- `blur`
- `brightness`
- `exposure`
- `occlusion`
- `motion_blur`
- `camera_shake`
- `target_distance`
- `angle_quality`
- `resolution_sufficiency`
- `frame_stability`
- `privacy_sensitivity`

质量等级：

- `GOOD`
- `DEGRADED`
- `POOR`
- `BLOCKED`
- `UNKNOWN_MARKED`

每个等级都要定义：

- `scene_sketch_allowed_candidate`
- `visual_focus_allowed_candidate`
- `ocr_activation_allowed_candidate`
- `tracking_request_allowed_candidate`
- `world_observation_allowed_candidate`
- `active_view_adjustment_recommended`
- `safety_only_recommended`
- `reject_reason`

## Privacy Tagging

必须定义以下 privacy tags：

- `human_face_visible`
- `bystander_presence`
- `license_plate_visible`
- `private_space_candidate`
- `home_context_candidate`
- `medical_context_candidate`
- `school_or_child_context_candidate`
- `workplace_context_candidate`
- `screen_or_document_visible`
- `personal_item_visible`
- `commercial_sensitive_candidate`

原则：

- privacy tag missing -> frame blocked from downstream
- privacy filtering owned by `MidPlatform`
- frame collection != frame long-term storage
- frame usable for task != frame eligible for `WorldModel/Memory`
- private/home/medical/school/workplace contexts require restricted policy
- no face recognition
- no identity inference
- no emotional inference

## STC / Freshness

`FrameSTCFreshnessPolicy` 必须复用现有 STC / TTL / freshness 语义：

- `timestamp_required=true`
- `monotonic_seq_required=true`
- `location_context_optional_but_marked=true`
- `pose_or_view_context_optional_but_marked=true`
- `source_chain_required=true`
- `stc_freshness_reuse_required=true`
- `current_action_allowed_when_stale=false`
- `archive_candidate_allowed=true`

这表示：

- stale / expired frame 不可用于当前 action
- 但可进入 archive/debug/review 候选

## Downstream Handoff

允许：

- `Frame -> ViewQualityCandidate`
- `Frame -> SceneSketchCandidate`
- `Frame -> VisualFocusPlan candidate`
- `Frame -> OCRActivationCandidate only via VisualFocus`
- `Frame -> TrackingRequestCandidate only via VisualFocus/MidPlatform`
- `Frame -> WorldObservationCandidate only via WorldObservation policy`
- `Frame -> Debug/Review artifact if no privacy conflict`

禁止：

- `Frame -> OCR provider directly`
- `Frame -> tracking runtime directly`
- `Frame -> map API`
- `Frame -> NavigationAction`
- `Frame -> SpeechOutput`
- `Frame -> WorldModel write`
- `Frame -> Memory write`
- `Frame -> Fact write`
- `Frame -> SceneDelta`

必须明确：

- `frame_to_ocr_requires_visual_focus=true`
- `frame_to_tracking_requires_visual_focus=true`
- `frame_to_world_observation_requires_policy=true`
- `frame_to_navigation_action_allowed=false`
- `frame_to_speech_output_allowed=false`
- `frame_to_worldmodel_write_allowed=false`
- `frame_to_memory_write_allowed=false`
- `frame_to_fact_write_allowed=false`

## Dual-Device / Dual-Lane Redundant Perception Placeholder

当前仅为未来硬件阶段预留双设备 / 双模型 / 双通道冗余感知框架。该框架未来用于降低单模型压力、增强安全冗余和故障降级能力。但当前不接真实硬件、不执行 failover、不做多输入融合、不做 dual-model runtime。所有内容均为 placeholder / future hook。

本阶段只预留以下占位对象：

- `PerceptionInputChannelPlaceholder`
- `PerceptionDeviceHealthPlaceholder`
- `PerceptionLaneFailoverPlaceholder`
- `DualInputConsistencyPlaceholder`

它们只用于表达未来可能的：

- 主输入设备 + 备份输入设备
- `Safety-World Lane` 输入设备 + `Task-Focus Lane` 输入设备
- 低功耗安全观察设备 + 高精度任务观察设备
- `RGB + depth / ToF / wide-angle / secondary camera`
- 主模型 + 备份模型
- 轻量安全模型 + 重型任务模型

但当前必须明确：

- `dual_device_runtime_allowed=false`
- `dual_model_runtime_allowed=false`
- `failover_runtime_allowed=false`
- `device_health_fact_allowed=false`
- `lane_failover_action_allowed=false`
- `automatic_hardware_switch_allowed=false`
- `multi_input_fusion_runtime_allowed=false`
- `hardware_stage_deferred=true`

这些占位不属于当前视觉主线 runtime，也不代表当前硬件实现已经开始。

## Scenario Matrix

本阶段覆盖至少 10 个场景：

1. `static_test_image_allowed_for_schema_test`
2. `pre_recorded_video_frame_allowed_for_controlled_dryrun`
3. `simulation_frame_allowed_for_sim_lab`
4. `uploaded_frame_requires_privacy_tags`
5. `live_camera_placeholder_blocked_now`
6. `external_stream_placeholder_blocked_now`
7. `low_quality_frame_degraded`
8. `privacy_sensitive_home_frame_restricted`
9. `stale_frame_archive_candidate_only`
10. `frame_to_ocr_requires_visual_focus`

这些场景共同确认：

- static / prerecorded / simulation frame 可以作为未来 dry-run 输入候选
- live camera / device camera / external stream 当前全部 blocked
- privacy tag 缺失时必须阻断 downstream
- OCR activation 只能通过 `VisualFocus`

## Readiness Gate

GO 条件：

- source policy defined
- frame candidate schema defined
- intake gate defined
- quality gate defined
- privacy tagging defined
- STC/freshness policy defined
- downstream handoff policy defined
- no live camera runtime
- no model runtime
- no write
- next phase clear

NO-GO 条件：

- live camera attempted
- unknown frame source allowed
- missing source_chain allowed
- privacy tags optional for downstream
- OCR provider allowed directly
- tracking runtime allowed directly
- `WorldModel/Memory/Fact` write allowed
- `NavigationAction` allowed
- `SpeechOutput` allowed

## Boundary

本阶段正式冻结：

- `planning_scope=controlled_frame_input_planning_only`
- `live_camera_allowed=false`
- `device_camera_allowed=false`
- `external_stream_allowed=false`
- `no_runtime_executed=true`
- `no_new_runtime_enabled=true`
- `camera_invoked=false`
- `camera_opened=false`
- `video_capture_invoked=false`
- `visual_model_invoked=false`
- `ocr_provider_invoked=false`
- `tracking_runtime_invoked=false`
- `navigation_action_triggered=false`
- `world_model_written=false`
- `memory_written=false`
- `library_written=false`
- `fact_written=false`

## Final Verdict

当 runner / verifier 全部通过时，本阶段正式结论为：

- `final_decision=CONTROLLED_FRAME_INPUT_PLANNING_READY_FOR_CONTROLLED_FRAME_INPUT_DRYRUN`
- `phase verdict=GO`
- `recommended_next_phase=Phase-Controlled-Frame-Input-DryRun-v1-001`

这表示：

- Luna 已具备“如何安全接入受控帧输入”的正式规则
- 仍然不接 `live camera`
- 仍然不打开摄像头
- 仍然不读取真实设备流
- 下一阶段如果进入 dry-run，也只能用 `static test image / pre-recorded frame / simulation frame`

当前状态更新：

- `Phase-Controlled-Frame-Input-DryRun-v1-001 = GO`
- `final_decision=CONTROLLED_FRAME_INPUT_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `Phase-Controlled-Frame-Input-Post-DryRun-Review-v1-001 = GO`
- `final_decision=CONTROLLED_FRAME_INPUT_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`
- `Phase-Controlled-Frame-Input-Closure-v1-001 = GO`
- `final_decision=CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE`
- 当前推荐下一阶段：`Phase-Post-Controlled-Frame-Input-Roadmap-Decision-v1-001`
