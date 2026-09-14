## GO

- Planning GO；owner/ack/rehearsal/package 缺口均模拟且硬阻断 migration + arming
- `armed_batch_count=0`；`all_batches_not_armed=true`
- `ready_for_post_dryrun_review=true`

## NO-GO

- Planning 未 GO 或 dry-run 中出现 `armed_batch_count>0`
- `owner_confirmed_now=true` / `rollback_rehearsal_executed_now=true` / `ready_for_real_migration=true`

## Smoke

- **Output**: `_eval_out/main_project_structure_migration_pre_authorization_and_rollback_rehearsal_dryrun_v1_smoke_v0/`
- **Next**: `Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Post-DryRun-Review-v1-001`
