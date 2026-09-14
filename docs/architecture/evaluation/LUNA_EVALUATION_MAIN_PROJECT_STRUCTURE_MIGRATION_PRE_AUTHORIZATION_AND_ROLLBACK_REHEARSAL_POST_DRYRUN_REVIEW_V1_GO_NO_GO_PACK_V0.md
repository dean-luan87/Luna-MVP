## GO

- DryRun GO；gap_hard_block 三类缺口 + package 缺失审查通过
- `ready_for_closure=true`；`armed_batch_count=0`；无权限释放

## NO-GO

- DryRun 未 GO 或 `armed_batch_count>0` / `ready_for_real_migration=true`
- `gap_hard_block_review_pass=false`

## Smoke

- **Output**: `_eval_out/main_project_structure_migration_pre_authorization_and_rollback_rehearsal_post_dryrun_review_v1_smoke_v0/`
- **Next**: `Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Closure-v1-001`
