# Luna Evaluation — Controlled Frame Sample Planning v1 GO / NO-GO Pack v0

**Phase**：`Phase-Controlled-Frame-Sample-Planning-v1-001`  
**判定目标**：允许进入 `Phase-Controlled-Frame-Sample-DryRun-v1-001`（仍为 manifest-level）

## GO 条件（必须同时满足）

- 输入 roots 全部 required=loaded 且 summary `final_decision` 匹配主线前置阶段
- policy/schema 全部生成且 summary 标记为 true：
  - `controlled_frame_sample_planning_policy_defined`
  - `controlled_frame_sample_manifest_schema_defined`
  - `sample_source_policy_defined`
  - `file_boundary_policy_defined`
  - `privacy_precheck_policy_defined`
  - `manual_review_gate_policy_defined`
  - `sample_usage_policy_defined`
  - `sample_to_frame_candidate_mapping_policy_defined`
- 场景矩阵：
  - `scenario_matrix_generated=true`
  - `scenario_count>=14`
  - 必含 14 个 scenario_id（allowed/restricted/blocked/review）
- 计数阈值：
  - `allowed_sample_candidate_count>=4`
  - `restricted_sample_candidate_count>=4`
  - `blocked_sample_candidate_count>=4`
  - `manual_review_required_case_count>=4`
- 强边界（summary 必须为 false）：
  - `file_content_read / image_content_read / video_content_read`
  - `file_opened / image_opened / video_opened`
  - `video_decoded / frame_extracted`
  - `camera_invoked / visual_model_invoked`
  - `map_api_invoked / gaode_api_invoked / gps_runtime_invoked`
  - `ocr_provider_invoked / ocrrequest_submitted`
  - `tracking_runtime_invoked / optical_flow_runtime_invoked`
  - `crossing_runtime_invoked`
  - `speech_gate_invoked / vop_invoked / tts_invoked`
  - `task_state_committed_now / navigation_action_triggered`
  - `scene_delta_generated / route_modified`
  - `world_model_written / memory_written / library_written / fact_written`
- manifest-only 不变式（summary 必须为 true）：
  - `manifest_only_processing=true`
  - `sample_manifest_not_sample_processing=true`
  - `privacy_precheck_required=true`
  - `manual_review_gate_required_for_sensitive_samples=true`
  - `sample_to_frame_candidate_mapping_without_content_read=true`
  - `no_runtime_executed=true`
  - `no_new_runtime_enabled=true`
  - `boundary_ok=true`
  - `violations=[]`
- readiness：
  - `final_decision=CONTROLLED_FRAME_SAMPLE_PLANNING_READY_FOR_CONTROLLED_FRAME_SAMPLE_DRYRUN`
  - `recommended_next_phase=Phase-Controlled-Frame-Sample-DryRun-v1-001`

## NO-GO 典型触发

- 缺少 required input root 或前置 phase `final_decision` 不匹配
- 任意边界字段出现 true（打开文件 / 解码 / 抽帧 / runtime / 写入）
- 场景矩阵不足 14 或缺少关键 blocked/restricted/review 场景
- `privacy_precheck_required=false` 或 `manual_review_gate_required_for_sensitive_samples=false`

## Verifier 门槛

verifier 必须：

- `checks_total>=180`
- `min_checks_required=180`
- `baseline_requirement=140`
- 通过时输出 `verdict=GO` 并写入 `_eval_out/.../verifier_report.json`

