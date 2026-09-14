# Luna Evaluation — Main Project Structure Migration Stabilized Execution Planning v1

**输出**：`_eval_out/main_project_structure_migration_stabilized_execution_planning_v1_smoke_v0/`

## Run

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_stabilized_execution_planning_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_stabilized_execution_planning_v1.py
```

## Expected

- Resume Planning GO 已正确读取
- `execution_planning_only=true`；所有 `actual_file_*_executed=false`
- B0–B7 完整；每批 manifest / rollback / verifier / abort / domain isolation / protected / eval_out guard
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_EXECUTION_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Stabilized-Execution-DryRun-v1-001`
