# Luna Evaluation — Rollback Rehearsal Roadmap Decision v1

**Phase**：`Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Roadmap-Decision-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_rollback_rehearsal_roadmap_decision_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_rollback_rehearsal_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_rollback_rehearsal_roadmap_decision_v1.py
```

## 通过条件

- Closure 上游 GO；`rollback_rehearsal_chain_closed=true`
- `selected_route=Rollback Rehearsal Execution Planning`
- 不释放 rehearsal execution / 迁移 / batch arming
- Verifier ≥ 220 checks（baseline 180）

## Smoke 结果

- **verifier**: GO
- **checks**: 286/220
- **Next**: `Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Planning-v1-001`
