# GO/NO-GO Pack — Main Project Structure Migration B0 Preflight Via Harness v1

## 必须确认（GO）

- `verifier=GO`
- `boundary_ok=true`
- `b0_preflight_executed_now=true`
- `harness_contract_reused=true`
- `all_fixed_checks_pass=true`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_B0_PREFLIGHT_VIA_HARNESS_READY_FOR_CONTROLLED_EXECUTION`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-B0-Controlled-Execution-v1-001`
- `source_path_mode=workspace_fallback` 时 `standard_eval_out_write_pending_on_local_repro=true`

## 禁止事项（必须为 false）

- `harness_extraction_reopened_now` / `harness_adoption_reopened_now`
- `b0_armed_now` / `batch_armed_now`
- `b0_execution_started_now` / `batch_execution_started_now`
- `execution_window_opened_now`
- 所有 `actual_file_*_executed`
- `verifier_rerun_executed_now` / `rollback_rehearsal_executed_now` / `post_migration_tests_executed_now`
- `runtime_refactor_executed_now` / `old_phase_deleted_now` / `old_phase_deprecated_now`

## 必须存在

- `b0_preflight_result_v1.json`
- `b0_batch_config_instance_v1.json`
- `b0_preflight_migration_refactor_opportunity_scan_v1.json`（`extract_now_allowed=false`）
