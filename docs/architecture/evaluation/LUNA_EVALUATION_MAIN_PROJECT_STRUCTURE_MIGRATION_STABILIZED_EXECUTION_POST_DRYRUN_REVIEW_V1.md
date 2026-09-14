# Luna Evaluation — Main Project Structure Migration Stabilized Execution Post-DryRun Review v1

**输出**：`_eval_out/main_project_structure_migration_stabilized_execution_post_dryrun_review_v1_smoke_v0/`

## Run

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_stabilized_execution_post_dryrun_review_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_stabilized_execution_post_dryrun_review_v1.py
```

## Expected

- Execution DryRun GO 被正确读取；14 类 dry-run 产物存在
- B0–B7 trace completeness review pass
- gates/manifest/rollback/verifier(non-exec)/protected/eval_out/domain/abort/fileop(non-exec) reviews 全 pass
- `review_only=true` 且 `post_dryrun_review_only=true`
- 无真实 file operation / batch arming / verifier rerun / rollback rehearsal
- final decision 指向 Batch Authorization Planning（不直接进入 batch execution）

