# Luna Evaluation — Controlled Frame Sample DryRun v1 GO / NO-GO Pack v0

**Phase**：`Phase-Controlled-Frame-Sample-DryRun-v1-001`  
**判定目标**：允许进入 `Phase-Controlled-Frame-Sample-Post-DryRun-Review-v1-001`

## GO 条件（必须同时满足）

- 输入 roots required 全部 loaded 且 `controlled_frame_sample_planning_input_loaded=true`
- schema 全部生成且 summary 标记为 true：
  - `dryrun_case_schema_defined`
  - `sample_manifest_metadata_stub_schema_defined`
  - `sample_source_decision_candidate_schema_defined`
  - `file_boundary_decision_candidate_schema_defined`
  - `privacy_precheck_decision_candidate_schema_defined`
  - `manual_review_decision_candidate_schema_defined`
  - `sample_usage_decision_candidate_schema_defined`
  - `sample_to_frame_candidate_mapping_stub_schema_defined`
  - `controlled_frame_sample_dryrun_result_schema_defined`
- 场景：
  - `scenario_matrix_generated=true`
  - `scenario_count>=16`
  - 必含 16 个 scenario_id（含 medical/workplace 两个新增）
- 计数：
  - `dryrun_results_generated=true`
  - `allowed_sample_candidate_count>=4`
  - `restricted_sample_candidate_count>=5`
  - `blocked_sample_candidate_count>=4`
  - `manual_review_required_case_count>=5`
- 文件/内容边界（必须为 false）：
  - `file_opened/image_opened/video_opened`
  - `file_content_read/image_content_read/video_content_read`
  - `video_decoded/frame_extracted`
  - `real_file_hash_computed`
- manifest-only 不变式（必须为 true）：
  - `manifest_metadata_only=true`
  - `sample_manifest_loaded=true`
  - `manifest_only_processing=true`
  - `sample_manifest_not_sample_processing=true`
- 禁止下游生成/动作/写入（必须为 false）：
  - `visual_observation_generated/scene_sketch_generated/ocr_activation_result_generated/tracking_result_generated`
  - `navigation_action_triggered/crossing_runtime_invoked`
  - `world_model_written/memory_written/library_written/fact_written`
- readiness：
  - `final_decision=CONTROLLED_FRAME_SAMPLE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
  - `recommended_next_phase=Phase-Controlled-Frame-Sample-Post-DryRun-Review-v1-001`

## NO-GO 典型触发

- 任意场景出现“打开文件/解码/抽帧/计算真实 hash”
- 允许从样例直接生成视觉观察/scene sketch/OCR/tracking 结果
- `missing_source_chain` / `missing_privacy_precheck` / `unknown_source` 未被阻断
- `manual_review_gate_required_for_sensitive_samples=false`

## Verifier 门槛

verifier 必须：

- `checks_total>=200`
- `min_checks_required=200`
- `baseline_requirement=160`
- 写入 `_eval_out/.../verifier_report.json`

