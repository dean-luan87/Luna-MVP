# Luna Evaluation — Controlled Frame File Existence Check Guarded Planning v1

**Phase**：`Phase-Controlled-Frame-File-Existence-Check-Guarded-Planning-v1-001`  
**输出目录**：`_eval_out/controlled_frame_file_existence_check_guarded_planning_v1_smoke_v0/`

## 目标

本评测只验证：

- 输入 roots 加载状态是否正确（required 必须 loaded；optional 允许 optional_missing）
- planning-only 产物与 schema/policy 是否齐全
- 场景矩阵覆盖是否满足（≥18）
- **强边界** 是否冻结（不调用 exists/stat/open/read/hash/exif/probe/runtime/write/action/speech）
- 最终推荐下一阶段是否为 `Phase-Controlled-Frame-File-Existence-Check-Guarded-DryRun-v1-001`

## 运行命令（smoke）

运行 runner：

```bash
python tools/evaluation/vision/run_controlled_frame_file_existence_check_guarded_planning_v1.py
```

运行 verifier：

```bash
python tools/evaluation/vision/verify_controlled_frame_file_existence_check_guarded_planning_v1.py
```

## 关键产物清单

`_eval_out/controlled_frame_file_existence_check_guarded_planning_v1_smoke_v0/` 必须包含：

- `summary.json`
- `input_root_matrix.json`
- `controlled_frame_file_existence_check_guarded_planning_policy.json`
- `file_existence_check_gate_policy.json`
- `allowed_path_scope_policy.json`
- `blocked_path_scope_policy.json`
- `file_existence_authorization_policy.json`
- `file_existence_audit_trace_policy.json`
- `file_existence_failure_mode_policy.json`
- `file_existence_rollback_policy.json`
- `file_existence_decision_candidate_schema.json`
- `existence_check_to_file_metadata_candidate_mapping_policy.json`
- `controlled_frame_file_existence_check_guarded_planning_scenario_matrix.json`
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
- `final_decision=CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase=Phase-Controlled-Frame-File-Existence-Check-Guarded-DryRun-v1-001`

