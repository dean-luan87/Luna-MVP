# Luna Evaluation — Controlled Frame File Stat Guarded Closure v1

**Phase**：`Phase-Controlled-Frame-File-Stat-Guarded-Closure-v1-001`  
**输出目录**：`_eval_out/controlled_frame_file_stat_guarded_closure_v1_smoke_v0/`

## 目标

验证 closure-only 产物结构、输入 roots 加载状态、边界冻结与 non-claims 完整性，并确认该 closure **不启用**真实 `stat/exists/open/read/hash`。

## 运行命令（smoke）

运行 runner：

```bash
python tools/evaluation/vision/run_controlled_frame_file_stat_guarded_closure_v1.py
```

运行 verifier：

```bash
python tools/evaluation/vision/verify_controlled_frame_file_stat_guarded_closure_v1.py
```

## 关键产物清单

`_eval_out/controlled_frame_file_stat_guarded_closure_v1_smoke_v0/` 必须包含：

- `summary.json`
- `input_root_matrix.json`
- `controlled_frame_file_stat_guarded_closure_summary.json`
- `completed_phase_matrix.json`
- `validated_capability_summary.json`
- `disabled_file_operation_summary.json`
- `disabled_runtime_summary.json`
- `closure_boundary_freeze.json`
- `file_stat_non_claims_register.json`
- `deferred_capability_pool.json`
- `governance_debt_carryover.json`
- `closure_readiness_gate.json`
- `next_phase_recommendation.json`
- `no_file_operation_boundary_report.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## 通过判定

verifier 必须输出：

- `verdict=GO`
- `final_decision=CONTROLLED_FRAME_FILE_STAT_GUARDED_CLOSED_FOR_CURRENT_MAINLINE`
- `recommended_next_phase=Phase-Post-File-Stat-Roadmap-Decision-v1-001`

