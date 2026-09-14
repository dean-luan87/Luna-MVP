# Luna Evaluation — Main Project Structure Migration Controlled Batch Execution Authorization Planning v1

**输出**：`_eval_out/main_project_structure_migration_controlled_batch_execution_authorization_planning_v1_smoke_v0/`

## Run

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_controlled_batch_execution_authorization_planning_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_controlled_batch_execution_authorization_planning_v1.py
```

## Expected

- Batch Authorization Post-DryRun Review GO 被正确读取
- 17 类 planning 产物生成
- B0–B7 controlled execution authorization scope matrix 完整
- allowlist/blocklist、verifier rerun plan、rollback rehearsal requirement、abort policy、post-migration test plan 都是 planning-only（均不执行）
- request/grant/arming/execution 全部 false；所有 `actual_file_*_executed=false`
- 若 workspace fallback，则 `standard_eval_out_write_pending_on_local_repro=true`
- final decision 指向 Controlled Batch Execution Authorization DryRun

