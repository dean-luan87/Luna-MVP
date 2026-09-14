# Luna Evaluation — Rollback Rehearsal DryRun v1

**Phase**：`Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_rollback_rehearsal_dryrun_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_rollback_rehearsal_dryrun_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_rollback_rehearsal_dryrun_v1.py
```

## 通过条件

- Rollback Rehearsal DryRun Planning 上游 GO
- `sandbox_simulated=true`；`sandbox_created_now=false`；`branch_created_now=false`
- B0–B7 路径均已 `*_simulated=true`；`restore_path_map_generated_now=false`
- `verifier_rerun_executed_now=false`；`evidence_generated_now=false`；`rollback_success_claim_allowed=false`
- `ready_for_post_dryrun_review=true`；Verifier ≥ 380 checks（baseline 320）

## Smoke 结果

- **verifier**: GO
- **checks**: 456/380
- **Next**: `Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Post-DryRun-Review-v1-001`
