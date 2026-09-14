# Luna Evaluation — Controlled Frame Sample Post-DryRun Review v1 GO / NO-GO Pack v0

**Phase**：`Phase-Controlled-Frame-Sample-Post-DryRun-Review-v1-001`  
**判定目标**：允许进入 `Phase-Controlled-Frame-Sample-Closure-v1-001`

## GO 条件（必须同时满足）

- 输入 roots required 全部 loaded：
  - `controlled_frame_sample_dryrun_input_loaded=true`
  - `controlled_frame_sample_planning_input_loaded=true`
- review 产物全部生成（summary 标记为 true）：
  - `input_root_review_generated`
  - `scenario_coverage_review_generated`
  - `sample_source_policy_review_generated`
  - `file_boundary_review_generated`
  - `privacy_precheck_review_generated`
  - `manual_review_gate_review_generated`
  - `sample_usage_policy_review_generated`
  - `sample_to_frame_mapping_review_generated`
  - `runtime_write_action_speech_boundary_review_generated`
  - `closure_readiness_decision_generated`
- 覆盖/计数：
  - `reviewed_scenario_count>=16`
  - `allowed_sample_candidate_count>=4`
  - `restricted_sample_candidate_count>=5`
  - `blocked_sample_candidate_count>=4`
  - `manual_review_required_case_count>=5`
- 文件/内容边界（必须为 false）：
  - `file_opened/image_opened/video_opened`
  - `file_content_read/image_content_read/video_content_read`
  - `video_decoded/frame_extracted`
  - `real_file_hash_computed`
- 策略边界验证（必须为 true/false 如下）：
  - `missing_source_chain_blocked_verified=true`
  - `missing_privacy_precheck_blocked_verified=true`
  - `live_camera_sample_blocked_verified=true`
  - `external_stream_sample_blocked_verified=true`
  - `privacy_precheck_required=true`
  - `manual_review_gate_required_for_sensitive_samples=true`
  - `sample_to_frame_candidate_mapping_without_content_read=true`
  - `visual_observation_generated/scene_sketch_generated/ocr_activation_result_generated/tracking_result_generated=false`
- readiness：
  - `ready_for_closure=true`
  - `ready_for_real_image_read=false`
  - `ready_for_runtime=false`
  - `final_decision=CONTROLLED_FRAME_SAMPLE_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`
  - `recommended_next_phase=Phase-Controlled-Frame-Sample-Closure-v1-001`

## Verifier 门槛

verifier 必须：

- `checks_total>=180`
- `min_checks_required=180`
- `baseline_requirement=140`
- 写入 `_eval_out/.../verifier_report.json`

