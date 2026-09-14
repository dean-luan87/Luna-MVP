# Luna Evaluation — Controlled Frame Sample Closure v1 GO / NO-GO Pack v0

**Phase**：`Phase-Controlled-Frame-Sample-Closure-v1-001`  
**判定目标**：允许进入 `Phase-Post-Controlled-Frame-Sample-Roadmap-Decision-v1-001`

## GO 条件（必须同时满足）

- 输入 roots required 全部 loaded：
  - `post_dryrun_review_input_loaded=true`
  - `dryrun_input_loaded=true`
  - `planning_input_loaded=true`
- closure 产物全部生成（summary 标记为 true）：
  - `completed_phase_matrix_generated`
  - `validated_capability_summary_generated`
  - `disabled_runtime_summary_generated`
  - `closure_boundary_freeze_generated`
  - `non_claims_register_generated`
  - `deferred_capability_pool_generated`
  - `governance_debt_carryover_generated`
  - `closure_readiness_gate_generated`
- 链路收口：
  - `controlled_frame_sample_planning_closed=true`
  - `controlled_frame_sample_dryrun_closed=true`
  - `controlled_frame_sample_post_review_closed=true`
  - `controlled_frame_sample_closed=true`
- 非主张（必须为 false）：
  - `real_image_readiness_claimed=false`
  - `real_video_readiness_claimed=false`
  - `visual_runtime_claimed=false`
  - `production_readiness_claimed=false`
  - `runtime_enablement_claimed=false`
- 文件/内容边界（必须为 false）：
  - `file_opened/image_opened/video_opened`
  - `file_content_read/image_content_read/video_content_read`
  - `video_decoded/frame_extracted`
  - `real_file_hash_computed`
- readiness：
  - `final_decision=CONTROLLED_FRAME_SAMPLE_CLOSED_FOR_CURRENT_MAINLINE`
  - `recommended_next_phase=Phase-Post-Controlled-Frame-Sample-Roadmap-Decision-v1-001`

## Verifier 门槛

verifier 必须：

- `checks_total>=180`
- `min_checks_required=180`
- `baseline_requirement=140`
- 写入 `_eval_out/.../verifier_report.json`

