# Luna Evaluation — Execution Control and Test Harness DryRun v1

**Phase**：`Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-DryRun-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_execution_control_and_test_harness_dryrun_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_execution_control_and_test_harness_dryrun_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_execution_control_and_test_harness_dryrun_v1.py
```

## 通过条件（验收四要点）

- `armed_batch_count=0`；B1–B6 owner approval missing 阻断 arming；B7 前序测试未执行阻断 arming
- 关键 abort（protected asset / HR / DnAE / runtime / WM-Memory-Fact / whitebox / owner approval / missing harness-verifier-checkpoint）`blocks_execution=true`
- `post_migration_test_count=31`；`executed_test_count=0`；`post_migration_tests_executed=false`
- `verifier_suite_count>=12`；`verifier_suite_executed=false`；`rollback_rehearsal_executed=false`
- 全部 execution 禁止 flag 为 false；`boundary_ok=true`；`violations=[]`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- Verifier ≥ 340 checks（smoke **354**）
