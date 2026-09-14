# Luna Evaluation — Controlled Execution DryRun v1

**Phase**：`Phase-Main-Project-Structure-Migration-Controlled-Execution-DryRun-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_controlled_execution_dryrun_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_controlled_execution_dryrun_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_controlled_execution_dryrun_v1.py
```

## 通过条件

- Controlled Execution Planning 上游 GO
- `armed_batch_count=0`；`batch_execution_count=0`；`executed_test_count=0`
- `execution_window_opened=false`；`owner_approval_executed=false`
- B0–B7 全部 candidate-only 语义为 true
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- Verifier ≥ 360 checks（smoke **426**）
