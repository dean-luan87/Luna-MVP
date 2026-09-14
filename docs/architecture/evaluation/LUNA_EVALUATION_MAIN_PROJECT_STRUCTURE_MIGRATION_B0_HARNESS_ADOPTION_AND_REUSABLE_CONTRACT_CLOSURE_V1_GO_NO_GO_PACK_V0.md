# GO/NO-GO Pack — Main Project Structure Migration B0 Harness Adoption and Reusable Contract Closure v1

## 必须确认（GO）

- `verifier=GO`
- `boundary_ok=true`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_AND_REUSABLE_CONTRACT_CLOSED_READY_FOR_B0_PREFLIGHT_VIA_HARNESS`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-B0-Preflight-Via-Harness-v1-001`
- `source_path_mode` 若为 `workspace_fallback`，`standard_eval_out_write_pending_on_local_repro=true` 必须被正确记录

## 禁止事项（必须为 false）

- `harness_generated_now`
- `harness_enforced_now`
- `harness_runtime_integrated_now`
- `preflight_executed_now`
- `batch_armed_now`
- `batch_execution_started_now`
- `execution_window_opened_now`
- 所有 `actual_file_*_executed`
- `runtime_refactor_executed_now`
- `old_phase_deleted_now` / `old_phase_deprecated_now`
- `verifier_modified_now` / `phase_template_modified_now`

## 复用机制收口（必须存在）

- `reusable_batch_preflight_harness_contract_closure_v1.json`
- `future_batch_usage_guide_v1.json`
- `batch_config_template_v1.json`
- `anti_recursion_rules_freeze_v1.json`

