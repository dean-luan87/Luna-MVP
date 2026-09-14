# Luna Evaluation — Main Project Structure Migration Stabilized Batch Authorization DryRun v1

**输出**：`_eval_out/main_project_structure_migration_stabilized_batch_authorization_dryrun_v1_smoke_v0/`

## Run

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_stabilized_batch_authorization_dryrun_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_stabilized_batch_authorization_dryrun_v1.py
```

## Expected

- Batch Authorization Planning GO 被正确读取（必要产物齐全）
- B0–B7 scope / gates / window / rerun auth / rollback auth / file-op boundary / guard / non-claims 均可消费（dry-run pass）
- `batch_authorization_dryrun_only=true` 且 `simulated=true`
- request/grant/arming/execution 全为 false
- 若输入来自 workspace fallback，则 `summary.source_path_mode=workspace_fallback`
- final decision 指向 Post-DryRun Review

