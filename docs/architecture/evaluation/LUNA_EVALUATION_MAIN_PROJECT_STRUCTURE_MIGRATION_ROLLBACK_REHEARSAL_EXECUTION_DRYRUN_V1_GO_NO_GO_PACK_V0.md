## GO

- 执行 dry-run 链完整；全部真实执行权限 false；success claim blocked
- Gate matrix ≥16；verifier plan ≥12；failure trace ≥14

## NO-GO

- 创建真实 sandbox/branch、生成真实 restore map、subprocess verifier、真实 evidence
- 声明 rollback success 或释放 migration/arming
- final_decision 越级指向 real execution

## Smoke

- **Output**: `_eval_out/main_project_structure_migration_rollback_rehearsal_execution_dryrun_v1_smoke_v0/`
- **verifier**: GO（426/380 checks）
- **final_decision**: `MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **Next**：`Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Post-DryRun-Review-v1-001`
