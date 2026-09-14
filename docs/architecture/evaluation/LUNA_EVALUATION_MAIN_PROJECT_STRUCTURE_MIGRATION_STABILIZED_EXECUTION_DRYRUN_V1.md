# Luna Evaluation — Main Project Structure Migration Stabilized Execution DryRun v1

**输出**：`_eval_out/main_project_structure_migration_stabilized_execution_dryrun_v1_smoke_v0/`

## Run

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_stabilized_execution_dryrun_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_stabilized_execution_dryrun_v1.py
```

## Expected

- Execution Planning GO 被正确读取（14 类 planning 产物存在）
- B0–B7 dry-run trace 完整；各矩阵（gates / manifest / rollback / verifier / abort / guards / domain）均 pass
- `execution_dryrun_only=true` 且 `simulated=true`
- 无真实 file operation；无 batch arming；无 verifier rerun 执行；无 rollback rehearsal execution
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_EXECUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Stabilized-Execution-Post-DryRun-Review-v1-001`

