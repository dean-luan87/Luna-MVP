# Luna Evaluation — Rollback Rehearsal DryRun Planning v1

**Phase**：`Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-Planning-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_rollback_rehearsal_dryrun_planning_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_rollback_rehearsal_dryrun_planning_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_rollback_rehearsal_dryrun_planning_v1.py
```

## 通过条件

- Post-Pre-Authorization Roadmap（Route A）上游 GO
- Pre-Authorization Closure 链已冻结
- `scope_batch_count=8`；`mandatory_rollback_path_count>=6`
- `sandbox_created_now=false`；`restore_path_map_generated_now=false`
- `rollback_success_claim_allowed=false`；`dryrun_planning_cannot_claim_success=true`
- `ready_for_rollback_rehearsal_dryrun=true`；`ready_for_rollback_rehearsal_execution=false`
- Verifier ≥ 340 checks（baseline 280）

## Smoke 结果

- **verifier**: GO
- **checks**: 389/340
- **Next**: `Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-v1-001`
