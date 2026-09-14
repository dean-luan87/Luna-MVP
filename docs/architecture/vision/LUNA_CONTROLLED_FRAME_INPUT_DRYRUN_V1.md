# Luna — Controlled Frame Input DryRun v1

**Phase**：`Phase-Controlled-Frame-Input-DryRun-v1-001`  
**性质**：dry-run / metadata simulation / candidate chain validation / boundary verification only  
**边界**：不读取真实图像内容，不打开摄像头，不读取真实设备流，不调用视觉模型，不调用 `OCR provider`，不提交 `OCRRequest`，不调用地图 API / 高德 API，不调用 GPS runtime，不调用 tracking runtime，不调用 optical flow runtime，不导入或调用 `Supervision / ByteTrack / OC-SORT`，不写 `Memory` / `WorldModel` / `Fact` / `Library`，不做 `entity resolution`，不做 `fact admission`，不做 `memory consolidation`，不做 `library experience commit`，不生成 `Scene Delta`，不提交 `Task State`，不触发 `Navigation Action`，不调用 `Speech Gate / VOP / TTS`，不输出真实用户可听语音，不执行 `dual-device runtime / dual-model runtime / failover runtime / multi-input fusion runtime`

## 目标

本阶段正式执行 `Controlled Frame Input` 的严格 dry-run。

它只回答：

1. controlled frame metadata 能否通过 intake gate  
2. 不同 frame source 的 allowed / blocked 判断是否正确  
3. `source_chain / timestamp / privacy tags` 是否成为硬门槛  
4. frame quality 如何影响 downstream handoff  
5. privacy-sensitive frame 如何被限制  
6. stale / expired frame 是否只能进入 archive candidate  
7. frame -> OCR 是否必须经 `VisualFocus`  
8. frame -> tracking 是否必须经 `VisualFocus / MidPlatform`  
9. frame -> `WorldObservation` 是否必须经对应 policy  
10. frame 是否被阻止直接进入 `NavigationAction / SpeechOutput / WorldModel / Memory / Fact`  
11. `live_camera / device_camera / external_stream` 是否仍被拒绝  
12. dual-device placeholder 是否仍然只是 placeholder

## Dry-Run Input Scope

本阶段只允许以下受控来源：

- `static_test_image`
- `pre_recorded_video_frame`
- `simulation_frame`
- `controlled_uploaded_frame`

当前明确拒绝：

- `live_camera_placeholder`
- `device_camera_placeholder`
- `external_stream_placeholder`

并且必须保持：

- `frame_content_loaded=false`
- `actual_image_read=false`
- `visual_model_invoked=false`

## Core Objects

### ControlledFrameInputDryRunCase

用于表达单个 dry-run case，必须带：

- `dryrun_case_id`
- `case_type`
- `simulated_frame_source`
- `simulated_frame_metadata`
- `expected_intake_decision`
- `expected_quality_decision`
- `expected_privacy_decision`
- `expected_freshness_decision`
- `expected_downstream_handoff`
- `expected_boundary_flags`
- `source_chain`

### SimulatedFrameMetadata

只表达 metadata，不装载真实图像内容。必须带：

- `frame_id`
- `source_type`
- `source_origin`
- `frame_timestamp`
- `monotonic_seq`
- `source_chain`
- `privacy_tags`
- `task_context_ref`
- `location_context_ref`
- `pose_or_view_context_ref`
- `device_context_ref`
- `simulated_quality_profile`
- `freshness_profile`
- `ttl_policy_ref`
- `storage_policy_candidate`
- `frame_content_loaded=false`
- `actual_image_read=false`
- `visual_model_invoked=false`

### FrameIntakeDecisionCandidate

用于冻结 intake gate 的 dry-run 结论。必须带：

- `intake_decision_id`
- `source_case_id`
- `frame_id`
- `intake_status`
- `accepted_for_downstream_candidate`
- `blocked_reason`
- `required_missing_fields`
- `live_runtime_blocked`
- `privacy_gate_required`
- `source_chain_valid`
- `timestamp_valid`
- `fact_status=not_fact`
- `source_chain`

支持的拒绝状态至少包括：

- `rejected_missing_source_chain`
- `rejected_missing_timestamp`
- `rejected_missing_privacy_tags`
- `rejected_live_camera`
- `rejected_device_camera`
- `rejected_external_stream`

### FrameQualityDecisionCandidate

必须显式给出：

- `quality_level`
- `scene_sketch_allowed_candidate`
- `visual_focus_allowed_candidate`
- `ocr_activation_allowed_candidate`
- `tracking_request_allowed_candidate`
- `world_observation_allowed_candidate`
- `active_view_adjustment_recommended`
- `safety_only_recommended`
- `reject_reason`

质量等级冻结为：

- `GOOD`
- `DEGRADED`
- `POOR`
- `BLOCKED`
- `UNKNOWN_MARKED`

### FramePrivacyDecisionCandidate

必须表达：

- privacy tags 是否存在
- privacy risk level
- downstream 是否允许
- 是否需要 restricted use
- `long_term_storage_allowed=false`
- `worldmodel_handoff_allowed_candidate=false`
- `memory_handoff_allowed_candidate=false`

### FrameFreshnessDecisionCandidate

必须表达：

- `freshness_status`
- `ttl_policy_ref`
- `current_action_allowed=false`
- `archive_candidate_allowed`
- `stale_blocks_task_feedback`
- `expired_blocks_current_action`

### FrameDownstreamHandoffCandidate

用于表达 frame 候选是否能进入下游候选链。必须固定：

- `frame_to_ocr_requires_visual_focus=true`
- `frame_to_tracking_requires_visual_focus=true`
- `frame_to_world_observation_requires_policy=true`
- `frame_to_navigation_action_allowed=false`
- `frame_to_speech_output_allowed=false`
- `frame_to_worldmodel_write_allowed=false`
- `frame_to_memory_write_allowed=false`
- `frame_to_fact_write_allowed=false`

### ControlledFrameInputDryRunResult

用于汇总每个 case 的 dry-run 结果，必须带：

- `result_id`
- `source_case_id`
- `intake_decision_ref`
- `quality_decision_ref`
- `privacy_decision_ref`
- `freshness_decision_ref`
- `downstream_handoff_ref`
- `boundary_decision_ref`
- `dryrun_status`
- `violations`
- `source_chain`

### DualDevicePlaceholderDryRunReview

本阶段只复核 placeholder 是否存在与边界是否正确，不做任何 runtime。

必须保持：

- `dual_device_placeholder_loaded=true`
- `perception_input_channel_placeholder_present=true`
- `perception_device_health_placeholder_present=true`
- `perception_lane_failover_placeholder_present=true`
- `dual_input_consistency_placeholder_present=true`
- `dual_device_runtime_allowed=false`
- `dual_model_runtime_allowed=false`
- `failover_runtime_allowed=false`
- `automatic_hardware_switch_allowed=false`
- `multi_input_fusion_runtime_allowed=false`
- `hardware_stage_deferred=true`

## Scenario Matrix

本阶段覆盖 14 个 dry-run 场景：

1. `static_test_image_good_quality`
2. `prerecorded_video_frame_degraded_quality`
3. `simulation_frame_allowed`
4. `controlled_uploaded_frame_privacy_sensitive`
5. `missing_source_chain_rejected`
6. `missing_timestamp_rejected`
7. `missing_privacy_tags_rejected`
8. `live_camera_attempt_blocked`
9. `device_camera_attempt_blocked`
10. `external_stream_attempt_blocked`
11. `stale_frame_archive_only`
12. `frame_with_text_requires_visual_focus_for_ocr`
13. `frame_with_motion_requires_visual_focus_for_tracking`
14. `dual_device_placeholder_review_only`

这些场景共同确认：

- `static / prerecorded / simulation / controlled upload` 可以进入 metadata dry-run
- 缺少 `source_chain / timestamp / privacy_tags` 时必须拒绝
- `live_camera / device_camera / external_stream` 当前全部拒绝
- privacy-sensitive frame 必须 restricted
- stale / expired frame 不可用于 current action，只能 archive/review
- OCR activation 只能经 `VisualFocus`
- tracking request 只能经 `VisualFocus / MidPlatform`
- `WorldObservation` handoff 只能经对应 policy

## Boundary Freeze

本阶段正式冻结：

- `dryrun_scope=controlled_frame_input_dryrun_only`
- `no_runtime_executed=true`
- `no_new_runtime_enabled=true`
- `frame_content_loaded=false`
- `actual_image_read=false`
- `live_camera_allowed=false`
- `device_camera_allowed=false`
- `external_stream_allowed=false`
- `camera_invoked=false`
- `camera_opened=false`
- `video_capture_invoked=false`
- `visual_model_invoked=false`
- `map_api_invoked=false`
- `gaode_api_invoked=false`
- `gps_runtime_invoked=false`
- `ocr_provider_invoked=false`
- `ocrrequest_submitted=false`
- `tracking_runtime_invoked=false`
- `optical_flow_runtime_invoked=false`
- `supervision_invoked=false`
- `bytetrack_invoked=false`
- `ocsort_invoked=false`
- `dual_device_runtime_invoked=false`
- `dual_model_runtime_invoked=false`
- `failover_runtime_invoked=false`
- `multi_input_fusion_runtime_invoked=false`
- `speech_gate_invoked=false`
- `vop_invoked=false`
- `tts_invoked=false`
- `task_state_committed_now=false`
- `navigation_action_triggered=false`
- `route_modified=false`
- `scene_delta_generated=false`
- `world_model_written=false`
- `memory_written=false`
- `library_written=false`
- `fact_written=false`

## Final Verdict

当 runner / verifier 全部通过时，本阶段正式结论为：

- `final_decision=CONTROLLED_FRAME_INPUT_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `phase verdict=GO`
- `recommended_next_phase=Phase-Controlled-Frame-Input-Post-DryRun-Review-v1-001`

这表示：

- Luna 已完成 `Controlled Frame Input` 的 planning + dry-run 两层闭环
- Luna 已验证 frame metadata 可进入候选链，但尚未验证真实视觉能力
- 当前仍然不读取真实图像内容
- 当前仍然不打开摄像头
- 当前仍然不进入硬件阶段
- dual-device / dual-model / failover / multi-input fusion 仍然只是 placeholder
- 下一阶段只允许进入 `Post-DryRun Review`

当前状态更新：

- `Phase-Controlled-Frame-Input-Post-DryRun-Review-v1-001 = GO`
- `final_decision=CONTROLLED_FRAME_INPUT_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`
- `Phase-Controlled-Frame-Input-Closure-v1-001 = GO`
- `final_decision=CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE`
- 当前推荐下一阶段：`Phase-Post-Controlled-Frame-Input-Roadmap-Decision-v1-001`
