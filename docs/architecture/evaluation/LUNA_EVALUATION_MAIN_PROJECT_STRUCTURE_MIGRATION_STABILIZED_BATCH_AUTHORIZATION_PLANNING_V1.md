# Luna Evaluation — Main Project Structure Migration Stabilized Batch Authorization Planning v1

**输出**：`_eval_out/main_project_structure_migration_stabilized_batch_authorization_planning_v1_smoke_v0/`

## Run

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_stabilized_batch_authorization_planning_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_stabilized_batch_authorization_planning_v1.py
```

## Expected

- Post-DryRun Review GO 被正确读取
- 15 类 authorization planning 产物生成
- B0–B7 authorization scope matrix 完整（单域、guard 条件、request/grant 均为 false）
- request/grant schema planning、pre-authorization gate matrix、execution window planning 等均为 planning-only
- 无真实 file operation、无 batch arming、无 verifier rerun、无 rollback rehearsal execution
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_BATCH_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Stabilized-Batch-Authorization-DryRun-v1-001`

