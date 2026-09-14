# Luna Evaluation — Main Project Structure Migration Stabilized Batch Authorization Post-DryRun Review v1

**输出**：`_eval_out/main_project_structure_migration_stabilized_batch_authorization_post_dryrun_review_v1_smoke_v0/`

## Run

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_stabilized_batch_authorization_post_dryrun_review_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_stabilized_batch_authorization_post_dryrun_review_v1.py
```

## Expected

- Batch Authorization DryRun verifier=GO，且边界可信
- 15 类 review 产物生成
- request/grant/arming/execution 全部 false；无真实 file operation
- 若 source_path_mode=workspace_fallback，则 `standard_eval_out_write_pending_on_local_repro=true`
- final decision 指向 Controlled Batch Execution Authorization Planning（不是直接执行）

