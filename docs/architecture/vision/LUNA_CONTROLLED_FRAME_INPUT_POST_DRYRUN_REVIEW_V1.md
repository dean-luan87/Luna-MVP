# Luna — Controlled Frame Input Post-DryRun Review v1

**Phase**：`Phase-Controlled-Frame-Input-Post-DryRun-Review-v1-001`  
**性质**：review / audit / closure readiness only  
**边界**：不新增能力，不实现 runtime，不读取真实图像内容，不打开摄像头，不读取真实设备流，不调用视觉模型，不调用 `OCR provider`，不提交 `OCRRequest`，不调用地图 API / 高德 API，不调用 GPS runtime，不调用 tracking runtime，不调用 optical flow runtime，不导入或调用 `Supervision / ByteTrack / OC-SORT`，不写 `Memory` / `WorldModel` / `Fact` / `Library`，不做 `entity resolution`，不做 `fact admission`，不做 `memory consolidation`，不做 `library experience commit`，不生成 `Scene Delta`，不提交 `Task State`，不触发 `Navigation Action`，不调用 `Speech Gate / VOP / TTS`，不输出真实用户可听语音，不执行 `dual-device runtime / dual-model runtime / failover runtime / multi-input fusion runtime`

## 目标

本阶段正式审查 `Controlled Frame Input Planning + Controlled Frame Input DryRun` 是否稳定。

它只回答：

1. planning 是否已被 dry-run 覆盖  
2. 14 个 dry-run 场景是否完整  
3. allowed / rejected / restricted / stale archive-only 判断是否正确  
4. `source_chain / timestamp / privacy_tags` 是否为硬门槛  
5. quality gate 是否正确影响 downstream handoff  
6. privacy-sensitive frame 是否被限制  
7. stale / expired frame 是否被阻止用于 current action  
8. frame -> OCR 是否仍必须经 `VisualFocus`  
9. frame -> tracking 是否仍必须经 `VisualFocus / MidPlatform`  
10. frame -> `WorldObservation` 是否仍必须经 policy  
11. frame 是否被阻止直接进入 `NavigationAction / SpeechOutput / WorldModel / Memory / Fact`  
12. `live_camera / device_camera / external_stream` 是否仍被拒绝  
13. dual-device placeholder 是否仍只是 placeholder  
14. 是否可以进入 `Controlled Frame Input Closure`

## Core Review Objects

### ControlledFrameDryRunInputRootReview

用于审查本阶段所依赖的 roots 是否齐全，必须带：

- `review_id`
- `required_roots`
- `loaded_roots`
- `optional_missing_roots`
- `missing_required_roots`
- `input_root_status`
- `source_chain`

### ControlledFrameScenarioCoverageReview

用于审查 dry-run 场景是否完整覆盖，必须固定：

- `reviewed_scenario_count>=14`
- `expected_scenario_count=14`
- `missing_scenarios=[]`
- `allowed_source_cases_present=true`
- `rejected_source_cases_present=true`
- `restricted_privacy_cases_present=true`
- `stale_archive_only_cases_present=true`
- `dual_device_placeholder_case_present=true`

### FrameIntakeGateReview

必须审查：

- `accepted_candidate_count>=5`
- `rejected_candidate_count>=6`
- `restricted_candidate_count>=1`
- `stale_archive_only_candidate_count>=1`
- `source_chain_required_verified=true`
- `timestamp_required_verified=true`
- `privacy_tags_required_verified=true`
- `live_camera_blocked_verified=true`
- `device_camera_blocked_verified=true`
- `external_stream_blocked_verified=true`
- `unknown_source_blocked_verified=true`

### FrameQualityGateReview

必须确认：

- `GOOD` 质量下可进入正常 downstream candidate
- `DEGRADED` 质量下 downstream 被限制
- `BLOCKED` case 不可进入 task-grade downstream
- 需要时允许 `active_view_adjustment_candidate`
- `quality_fact_written=false`

### FramePrivacyTaggingReview

必须确认：

- privacy-sensitive case 已被审查
- `privacy_tags_required_for_downstream=true`
- `restricted_use_verified=true`
- `long_term_write_blocked=true`
- `face_identity_inference_allowed=false`
- `emotion_inference_allowed=false`

### FrameSTCFreshnessReview

必须确认：

- `timestamp_required=true`
- `monotonic_seq_reviewed=true`
- stale case 已被审查
- `expired_or_stale_current_action_blocked=true`
- `archive_candidate_allowed=true`
- `stc_freshness_reuse_required=true`
- `no_new_stc_module_created=true`

### FrameDownstreamHandoffReview

必须确认：

- frame 可进入 `ViewQuality / SceneSketch / VisualFocus` 候选
- `frame_to_ocr_requires_visual_focus=true`
- `frame_to_tracking_requires_visual_focus=true`
- `frame_to_world_observation_requires_policy=true`
- `frame_to_navigation_action_allowed=false`
- `frame_to_speech_output_allowed=false`
- `frame_to_worldmodel_write_allowed=false`
- `frame_to_memory_write_allowed=false`
- `frame_to_fact_write_allowed=false`

### DualDevicePlaceholderReview

本阶段只审查 placeholder 仍为 placeholder，不进入任何 runtime。

必须确认：

- `dual_device_redundant_perception_placeholder_loaded=true`
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

### RuntimeWriteActionSpeechBoundaryReview

必须继续保持：

- `frame_content_loaded=false`
- `actual_image_read=false`
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
- `scene_delta_generated=false`
- `world_model_written=false`
- `memory_written=false`
- `library_written=false`
- `fact_written=false`

### ControlledFrameInputClosureReadinessDecision

本阶段只产出 closure readiness，不进入 controlled sample planning。

必须固定：

- `post_dryrun_review_verdict=GO`
- `blockers=[]`
- `ready_for_closure=true`
- `ready_for_controlled_sample_planning=false`
- `recommended_next_phase=Phase-Controlled-Frame-Input-Closure-v1-001`
- `final_decision=CONTROLLED_FRAME_INPUT_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`

## 审查结论

本阶段审查确认：

- `Planning` 中定义的 intake / quality / privacy / STC/freshness / downstream handoff 边界，已经被 `DryRun` 覆盖
- 14 个 dry-run 场景完整覆盖了 allowed / rejected / restricted / stale / placeholder 五类情况
- `source_chain / timestamp / privacy_tags` 仍是 metadata dry-run 的硬门槛
- privacy-sensitive 与 stale 场景都被保守降级，没有出现越权 downstream
- dual-device placeholder 仍然只是 placeholder review，不进入 hardware stage

## Final Verdict

当 runner / verifier 全部通过时，本阶段正式结论为：

- `final_decision=CONTROLLED_FRAME_INPUT_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`
- `phase verdict=GO`
- `recommended_next_phase=Phase-Controlled-Frame-Input-Closure-v1-001`

这表示：

- `Controlled Frame Input` 已形成 `planning + dry-run + post-dryrun review` 三层闭环
- 当前建议先进入 `Closure` 收口
- 当前仍然不进入 controlled sample planning
- 当前仍然不读取真实图像内容
- 当前仍然不打开摄像头
- 当前仍然不进入 live camera / hardware / dual-device runtime

当前状态更新：

- `Phase-Controlled-Frame-Input-Closure-v1-001 = GO`
- `final_decision=CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE`
- `Phase-Post-Controlled-Frame-Input-Roadmap-Decision-v1-001 = GO`
- `final_decision=POST_CONTROLLED_FRAME_INPUT_ROADMAP_DECISION_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY`
- 当前推荐下一阶段：`Phase-Crossing-Decision-Safety-Governance-Policy-v1-001`
