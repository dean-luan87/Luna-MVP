# Luna Evaluation — Execution Control and Test Harness Post-DryRun Review v1

**Phase**：`Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Post-DryRun-Review-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_execution_control_and_test_harness_post_dryrun_review_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_execution_control_and_test_harness_post_dryrun_review_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_execution_control_and_test_harness_post_dryrun_review_v1.py
```

## 通过条件

- DryRun 上游 GO；`armed_batch_count=0`；关键 abort 均 `blocks_execution=true`
- `canonical_abort_mapping_applied=true`；`correction_semantic_impact=no_permission_granted`
- 31 测试绑定、`executed_test_count=0`；12 verifier 编排、未执行；rollback rehearsal required 未执行
- 全部 execution 禁止 flag 为 false；`ready_for_closure=true`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`
- Verifier ≥ 320 checks（smoke **320**）
