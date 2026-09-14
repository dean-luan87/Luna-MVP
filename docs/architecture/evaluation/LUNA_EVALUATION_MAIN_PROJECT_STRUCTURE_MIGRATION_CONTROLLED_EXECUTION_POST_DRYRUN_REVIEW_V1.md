# Luna Evaluation — Controlled Execution Post-DryRun Review v1

**Phase**：`Phase-Main-Project-Structure-Migration-Controlled-Execution-Post-DryRun-Review-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_controlled_execution_post_dryrun_review_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_controlled_execution_post_dryrun_review_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_controlled_execution_post_dryrun_review_v1.py
```

## 通过条件

- Controlled Execution DryRun 上游 GO
- `armed_batch_count=0`；`executed_test_count=0`；`evidence_pack_generated_now=false`
- `ready_for_closure=true`；`ready_for_real_migration=false`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`
- Verifier ≥ 320 checks（smoke **331**）
