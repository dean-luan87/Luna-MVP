# GO/NO-GO Pack — Main Project Structure Migration B0 Controlled Execution v1

## 必须确认（GO）

- `verifier=GO`
- `boundary_ok=true`
- `b0_execution_completed_now=true`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_B0_CONTROLLED_EXECUTION_READY_FOR_POST_MIGRATION_REVIEW`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-B0-Post-Migration-Review-v1-001`
- before/after manifest 与 operation_trace 齐全

## 禁止事项（必须为 false）

- `actual_file_delete_executed` / `actual_file_overwrite_executed` / `actual_file_merge_executed` / `actual_file_copy_executed`
- `eval_out_modified_now` / `protected_asset_modified_now` / `hr_modified_now` / `dnae_modified_now`
- `runtime_refactor_executed_now` / `old_phase_deleted_now` / `old_phase_deprecated_now`
- `harness_extraction_reopened_now` / `harness_adoption_reopened_now`

## move/rename 语义

- `actual_file_move_executed=true` 仅当确实 move
- `actual_file_rename_executed=true` 仅当确实 rename
- stable placement 场景允许两者均为 false 且 execution 仍 GO
