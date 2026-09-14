# Luna Evaluation — Controlled Frame File Existence Check Guarded Post-DryRun Review v1

**Phase**：`Phase-Controlled-Frame-File-Existence-Check-Guarded-Post-DryRun-Review-v1-001`  
**输出目录**：`_eval_out/controlled_frame_file_existence_check_guarded_post_dryrun_review_v1_smoke_v0/`

## 目标

本评测只验证 review-only 产物结构、输入 roots 加载状态、强边界冻结，以及 closure readiness 决策输出。

## 运行命令（smoke）

运行 runner：

```bash
python tools/evaluation/vision/run_controlled_frame_file_existence_check_guarded_post_dryrun_review_v1.py
```

运行 verifier：

```bash
python tools/evaluation/vision/verify_controlled_frame_file_existence_check_guarded_post_dryrun_review_v1.py
```

## 关键产物清单

`_eval_out/controlled_frame_file_existence_check_guarded_post_dryrun_review_v1_smoke_v0/` 必须包含：

- `summary.json`
- `input_root_matrix.json`
- `file_existence_guarded_dryrun_input_root_review.json`
- `file_existence_scenario_coverage_review.json`
- `file_existence_gate_decision_review.json`
- `path_scope_decision_review.json`
- `authorization_decision_review.json`
- `audit_trace_review.json`
- `failure_mode_review.json`
- `rollback_review.json`
- `existence_to_file_metadata_mapping_review.json`
- `file_operation_boundary_review.json`
- `runtime_write_action_speech_boundary_review.json`
- `file_existence_check_closure_readiness_decision.json`
- `governance_debt_review.json`
- `next_phase_recommendation.json`
- `no_file_operation_boundary_report.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## 通过判定

verifier 必须输出：

- `verifier=GO`
- `final_decision=CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`
- `recommended_next_phase=Phase-Controlled-Frame-File-Existence-Check-Guarded-Closure-v1-001`

