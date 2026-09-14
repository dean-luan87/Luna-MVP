# Luna Evaluation — Execution Control and Test Harness Planning v1

**Phase**：`Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Planning-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_execution_control_and_test_harness_planning_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_execution_control_and_test_harness_planning_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_execution_control_and_test_harness_planning_v1.py
```

## 通过条件

- `batch_count=8`；`abort_condition_count>=12`；`post_migration_test_count=31`；`harness_group_count>=5`；`verifier_suite_count>=8`
- 全部 execution 禁止 flag 为 false
- `ready_for_execution_control_dryrun=true`；`ready_for_real_migration=false`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_PLANNING_READY_FOR_DRYRUN`
- Verifier ≥ 300 checks（smoke 305）
