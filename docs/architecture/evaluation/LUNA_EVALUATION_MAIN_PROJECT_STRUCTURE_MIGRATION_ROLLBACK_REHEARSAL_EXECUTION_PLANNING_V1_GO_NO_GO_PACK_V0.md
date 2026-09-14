## GO

- 真实 rehearsal 准入门、授权、窗口、restore/verifier/evidence/failure/success gate 已定义
- 全部执行权限仍为 false；`ready_for_rollback_rehearsal_execution_dryrun=true`

## NO-GO

- sandbox/branch/evidence 在 planning 阶段被误标为已创建或已执行

## Smoke

- **Output**: `_eval_out/main_project_structure_migration_rollback_rehearsal_execution_planning_v1_smoke_v0/`
- **verifier**: GO（443/340 checks）
- **final_decision**: `MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_PLANNING_READY_FOR_DRYRUN`
- **Next**：`Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-DryRun-v1-001`
