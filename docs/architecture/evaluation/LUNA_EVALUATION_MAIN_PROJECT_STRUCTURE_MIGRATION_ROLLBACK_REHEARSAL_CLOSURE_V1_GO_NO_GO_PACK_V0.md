## GO

- Planning→DryRun→Post-Review 链已冻结；`rollback_rehearsal_chain_closed=true`
- 无 sandbox/branch/evidence/verifier rerun 真实执行；success claim 阻断

## NO-GO

- 任一上游 phase 未 GO 或执行权限被误释放

## Smoke

- **Output**: `_eval_out/main_project_structure_migration_rollback_rehearsal_closure_v1_smoke_v0/`
- **verifier**: GO（276/260 checks）
- **final_decision**: `MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_CLOSED_FOR_CURRENT_MAINLINE`
- **Next**：`Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Roadmap-Decision-v1-001`
