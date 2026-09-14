## GO

- Roadmap Route A 已选中；本 phase 完成 7 owner / operator ack / package / rehearsal / arming / blockers 规划
- `real_migration_execution_allowed=false`；`batch_arming_allowed_now=false`；`rollback_rehearsal_executed_now=false`
- `ready_for_pre_authorization_dryrun=true`

## NO-GO

- 上游 roadmap 未 GO 或 `owner_confirmed_now=true` / `rollback_rehearsal_executed_now=true`
- `ready_for_real_migration=true` 或 `arming_allowed_now=true`

## Smoke

- **Output**: `_eval_out/main_project_structure_migration_pre_authorization_and_rollback_rehearsal_planning_v1_smoke_v0/`
- **Next**: `Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-DryRun-v1-001`
