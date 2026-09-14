# Luna Evaluation — Rollback Rehearsal Execution Planning v1

**Phase**：`Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Planning-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_rollback_rehearsal_execution_planning_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_rollback_rehearsal_execution_planning_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_rollback_rehearsal_execution_planning_v1.py
```

## 通过条件

- Roadmap / Closure / dry-run 链上游 GO
- `rehearsal_execution_gate_item_count>=14`；执行权限全部为 false
- `ready_for_rollback_rehearsal_execution_dryrun=true`；`ready_for_rollback_rehearsal_execution=false`
- Verifier ≥ 340 checks（baseline 280）

## Smoke 结果

- **verifier**: GO
- **checks**: 443/340
- **Next**: `Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-DryRun-v1-001`

## 下游（已完成）

- Execution DryRun v1：GO（426/380）
- Execution Post-DryRun Review v1：GO（364/360）
- Execution Roadmap Decision v1：GO（356/260；Route A selected）
