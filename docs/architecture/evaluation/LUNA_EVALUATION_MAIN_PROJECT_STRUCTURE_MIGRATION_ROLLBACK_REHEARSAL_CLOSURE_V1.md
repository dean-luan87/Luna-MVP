# Luna Evaluation — Rollback Rehearsal Closure v1

**Phase**：`Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Closure-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_rollback_rehearsal_closure_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_rollback_rehearsal_closure_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_rollback_rehearsal_closure_v1.py
```

## 通过条件

- Post-Review / DryRun / Planning 上游 GO；`rollback_rehearsal_chain_closed=true`
- `completed_phase_count>=3`；全部执行权限仍为 false
- Verifier ≥ 260 checks（baseline 220）

## Smoke 结果

- **verifier**: GO
- **checks**: 276/260
- **Next**: `Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Roadmap-Decision-v1-001`
