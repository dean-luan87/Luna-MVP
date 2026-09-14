# Luna Evaluation — Controlled Frame File Existence Check Guarded DryRun v1

**Phase**：`Phase-Controlled-Frame-File-Existence-Check-Guarded-DryRun-v1-001`  
**输出目录**：`_eval_out/controlled_frame_file_existence_check_guarded_dryrun_v1_smoke_v0/`

## 目标

本评测只验证：

- required 输入 roots 全部 loaded（可只读加载历史 JSON）
- dry-run 产物齐全（schema + scenario matrix + results + boundary reports）
- 场景覆盖 ≥22，且关键 blocked/restricted/future_allowed 分支都存在
- **强边界** 仍冻结：不调用 exists/stat/open/read/hash/exif/probe/runtime/write/action/speech
- 最终推荐下一阶段为 `Phase-Controlled-Frame-File-Existence-Check-Guarded-Post-DryRun-Review-v1-001`

## 运行命令（smoke）

运行 runner：

```bash
python tools/evaluation/vision/run_controlled_frame_file_existence_check_guarded_dryrun_v1.py
```

运行 verifier：

```bash
python tools/evaluation/vision/verify_controlled_frame_file_existence_check_guarded_dryrun_v1.py
```

## 关键产物清单

`_eval_out/controlled_frame_file_existence_check_guarded_dryrun_v1_smoke_v0/` 必须包含：

- `summary.json`
- `input_root_matrix.json`
- `dryrun_case_schema.json`
- `simulated_file_existence_check_request_stub_schema.json`
- `file_existence_gate_decision_candidate_schema.json`
- `path_scope_dryrun_decision_candidate_schema.json`
- `file_existence_authorization_decision_candidate_schema.json`
- `file_existence_audit_trace_candidate_schema.json`
- `file_existence_failure_mode_decision_candidate_schema.json`
- `file_existence_rollback_decision_candidate_schema.json`
- `existence_check_to_file_metadata_mapping_decision_candidate_schema.json`
- `file_existence_check_guarded_dryrun_result_schema.json`
- `controlled_frame_file_existence_check_guarded_dryrun_scenario_matrix.json`
- `controlled_frame_file_existence_check_guarded_dryrun_results.json`
- `file_existence_gate_decision_results.json`
- `path_scope_dryrun_decision_results.json`
- `authorization_decision_results.json`
- `audit_trace_results.json`
- `failure_mode_decision_results.json`
- `rollback_decision_results.json`
- `existence_to_file_metadata_mapping_results.json`
- `file_existence_check_boundary_matrix.json`
- `governance_debt_register.json`
- `next_phase_recommendation.json`
- `no_file_operation_boundary_report.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## 通过判定

verifier 必须输出：

- `verifier=GO`
- `final_decision=CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Controlled-Frame-File-Existence-Check-Guarded-Post-DryRun-Review-v1-001`

