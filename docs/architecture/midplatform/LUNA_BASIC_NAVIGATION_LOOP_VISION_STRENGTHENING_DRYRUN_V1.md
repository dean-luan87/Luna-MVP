# Luna — Basic Navigation Loop Vision Strengthening DryRun v1

**Phase**：`Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001`  
**性质**：dry-run / candidate / boundary verification only  
**边界**：不执行真实导航，不调用 `camera`，不调用视觉模型，不调用 `OCR provider`，不提交 `OCRRequest`，不调用地图 API / 高德 API，不调用 tracking runtime，不调用 optical flow runtime，不导入或调用 `Supervision / ByteTrack / OC-SORT`，不写 `Memory` / `WorldModel` / `Fact` / `Library`，不做 `entity resolution`，不做 `fact admission`，不做 `memory consolidation`，不做 `library experience commit`，不生成 `Scene Delta`，不提交 `Task State`，不触发 `Navigation Action`，不调用 `Speech Gate / VOP / TTS`，不输出真实用户可听语音

## 阶段定位

本阶段把刚刚跑通的 `Visual-OCR-Map-Task Feedback` 候选链重新接回基础导航闭环：

视觉 / OCR / 地图 / 记忆 / 追踪候选反馈  
↓  
中台任务状态候选  
↓  
`Safety-Task Arbitration`  
↓  
`Navigation Guidance Candidate`  
↓  
`Text-only / dry output candidate`

本阶段回答：

1. `Visual-OCR-Map-Task feedback candidate` 能否进入基础导航闭环。
2. `SafetyFeedbackCandidate` 如何优先进入 `Safety-Task Arbitration`。
3. `TaskFeedbackCandidate` 如何影响 `NavigationGuidanceCandidate`。
4. `OCRActivationFeedbackCandidate` 如何保持 request candidate，不提交 `OCRRequest`。
5. `TrackingFeedbackCandidate` 如何保持 candidate，不触发 tracking runtime。
6. `MapMemoryContextFeedbackCandidate` 如何作为 context hint，而不是行动权威。
7. `ConflictCorrectionFeedbackCandidate` 如何触发保守 guidance / 用户确认 / 重新观察。
8. `ActiveViewAdjustmentFeedbackCandidate` 如何生成 dry output candidate，而不直接播报。
9. `crossing_uncertain / crowd_flow / low_quality_view` 等高风险场景如何保守降级。
10. dry-run 是否仍保持 `no-runtime / no-write / no-action / no-speech` 边界。

## 输入 roots

本阶段正式依赖：

- `_eval_out/visual_ocr_map_task_feedback_dryrun_v1_smoke_v0/`
- `_eval_out/selective_tracking_adapter_policy_v1_smoke_v0/`
- `_eval_out/world_observation_and_entity_feature_policy_v1_smoke_v0/`
- `_eval_out/task_aware_visual_focus_policy_v1_smoke_v0/`
- `_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0/`
- `_eval_out/basic_navigation_guidance_loop_stabilization_test_v1_smoke_v0/`
- `_eval_out/safety_task_arbitration_policy_v1_smoke_v0/`
- `_eval_out/minimal_runtime_integration_closure_v1_smoke_v0/`
- `_eval_out/ocr_mainline_final_closure_v1_smoke_v0/`

如存在，也加载：

- `_eval_out/basic_navigation_guidance_loop_dryrun_v1_smoke_v0/`
- `_eval_out/navigation_guidance_speech_adapter_v1_smoke_v0/`
- `_eval_out/voice_interruption_governance_dryrun_v1_smoke_v0/`
- `_eval_out/voice_command_ownership_gate_policy_v1_smoke_v0/`
- `_eval_out/minimal_runtime_integration_text_only_output_post_trial_review_v1_smoke_v0/`

## Core Object 1: NavigationVisionStrengtheningDryRunCase

关键字段：

- `dryrun_case_id`
- `case_type`
- `source_feedback_case_ref`
- `related_task_id`
- `task_phase`
- `incoming_feedback_candidates`
- `safety_feedback_refs`
- `task_feedback_refs`
- `ocr_activation_feedback_refs`
- `tracking_feedback_refs`
- `map_memory_context_feedback_refs`
- `conflict_correction_feedback_refs`
- `active_view_adjustment_feedback_refs`
- `expected_arbitration_path`
- `expected_guidance_candidate`
- `expected_output_candidate`
- `expected_boundary_flags`
- `source_chain`

## Core Object 2: NavigationFeedbackIntakeCandidate

该对象把 `Visual-OCR-Map-Task feedback` 进入导航闭环前做 intake。

关键字段：

- `intake_candidate_id`
- `source_dryrun_case_id`
- `feedback_refs`
- `intake_status`
- `accepted_feedback_types`
- `delayed_feedback_types`
- `suppressed_feedback_types`
- `requires_safety_task_arbitration`
- `requires_user_confirmation`
- `requires_view_adjustment`
- `requires_ocr_later`
- `requires_tracking_later`
- `fact_status=not_fact`
- `action_allowed=false`
- `source_chain`

## Core Object 3: VisionAwareNavigationGuidanceCandidate

`guidance_type` 至少覆盖：

- `route_alignment_hint`
- `continue_walking_candidate`
- `slow_down_candidate`
- `hold_still_candidate`
- `look_left_right_candidate`
- `active_view_adjustment_hint`
- `destination_approach_hint`
- `target_search_hint`
- `crossing_uncertain_hint`
- `crowd_flow_caution_hint`
- `obstacle_caution_hint`
- `map_visual_conflict_hint`
- `ocr_later_needed_hint`
- `tracking_later_needed_hint`

核心要求：

- `requires_safety_task_arbitration` 可为真
- `requires_speech_gate=true`
- `action_instruction_allowed=false`
- `navigation_action_allowed=false`

## Core Object 4: NavigationSafetyArbitrationBridgeCandidate

该对象只生成 `bridge candidate / dry-run result`，不调用真实 `Safety-Task Arbitration runtime`。

关键字段：

- `bridge_candidate_id`
- `source_guidance_candidate_id`
- `safety_feedback_refs`
- `task_feedback_refs`
- `arbitration_priority`
- `suppress_task_guidance`
- `delay_task_guidance`
- `allow_safety_guidance_candidate`
- `requires_confirmation`
- `requires_reobserve`
- `fact_status=not_fact`
- `action_allowed=false`
- `source_chain`

## Core Object 5: NavigationOutputCandidateDryRun

`output_mode` 可包括：

- `TEXT_ONLY_DRY_PREVIEW`
- `STRUCTURED_LOG_ONLY`
- `DRY_SPEECH_PREVIEW`
- `NO_OUTPUT_SUPPRESSED`
- `SAFETY_HOLD_PROMPT_CANDIDATE`
- `ACTIVE_VIEW_ADJUSTMENT_PROMPT_CANDIDATE`

必须明确：

- `speech_gate_required=true`
- `speech_allowed=false`
- `tts_allowed=false`
- `vop_allowed=false`
- `user_heard_assumed=false`
- `action_instruction_allowed=false`

## Core Object 6: NavigationVisionStrengtheningBoundaryDecision

每个 dry-run case 必须明确：

- `intake_boundary_ok`
- `arbitration_boundary_ok`
- `guidance_boundary_ok`
- `output_boundary_ok`
- `runtime_boundary_ok`
- `write_boundary_ok`
- `speech_boundary_ok`
- `action_boundary_ok`
- `violations`

## Dry-Run 场景矩阵

本阶段至少覆盖 12 个场景：

1. `route_walking_clear_path_guidance`
2. `route_walking_near_field_obstacle`
3. `approaching_destination_signage_candidate`
4. `shop_search_right_side_view_adjustment`
5. `object_search_home_privacy_sensitive`
6. `crowded_path_crowd_flow_caution`
7. `crossing_uncertain_red_green_light`
8. `visual_map_memory_conflict_navigation`
9. `low_quality_view_hold_still`
10. `temporary_facility_route_impact`
11. `tracking_later_needed_dynamic_obstacle`
12. `ocr_later_needed_readable_sign`

其中必须继续保持：

- clear path 只生成 `continue_walking_candidate`，不触发真实动作
- 近场障碍场景必须 safety priority，并延迟 task guidance
- 接近目标只生成 `destination_approach_hint + ocr_later_needed_hint`
- 商店搜索视角偏移时优先 `active_view_adjustment_hint`
- 家庭找物场景只允许 task candidate，不允许 identity fact
- 拥挤遮挡场景只允许 `crowd_flow_caution_hint`
- 过街不确定场景只允许 `crossing_uncertain_hint`
- 冲突场景只允许 `map_visual_conflict_hint + reobserve/confirm`
- 低质量视角只允许 `hold_still_candidate`
- 临时设施只能形成 `temporary route caution`
- dynamic obstacle 只允许 `tracking_later_needed_hint`
- readable sign 只允许 `ocr_later_needed_hint`

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
- `safety_task_arbitration_runtime_invoked=false`
- `speech_gate_invoked=false`
- `vop_invoked=false`
- `tts_invoked=false`
- `user_heard_assumed=false`
- `task_state_committed_now=false`
- `navigation_action_triggered=false`
- `route_modified=false`
- `scene_delta_generated=false`
- `world_model_written=false`
- `memory_written=false`
- `library_written=false`
- `fact_written=false`
- `entity_resolution_runtime_invoked=false`
- `fact_admission_runtime_invoked=false`
- `memory_consolidation_invoked=false`
- `library_experience_commit_invoked=false`

## Final Verdict

当 runner / verifier 全部通过时，本阶段正式结论为：

- `final_decision=BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `phase verdict=GO`
- `recommended_next_phase=Phase-Basic-Navigation-Loop-Vision-Strengthening-Post-DryRun-Review-v1-001`

这表示：

- 第一轮“视觉增强导航闭环”已完成 dry-run
- 仍然只停留在 `candidate / dry-run / boundary verification`
- 下一阶段只做 `Post-DryRun Review`

当前状态更新：

- `Phase-Basic-Navigation-Loop-Vision-Strengthening-Post-DryRun-Review-v1-001 = GO`
- `Phase-Basic-Navigation-Loop-Vision-Strengthening-Closure-v1-001 = GO`
- 当前推荐下一阶段：`Phase-Post-Vision-Strengthening-Roadmap-Decision-v1-001`
