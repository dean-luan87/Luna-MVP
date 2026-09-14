# Luna Evaluation — Rollback Rehearsal Execution Roadmap Decision v1

**Phase**：`Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Roadmap-Decision-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_rollback_rehearsal_execution_roadmap_decision_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_rollback_rehearsal_execution_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_rollback_rehearsal_execution_roadmap_decision_v1.py
```

## 通过条件（摘要）

- 必须读取 Execution Post-DryRun Review 输出，并观测其 `verifier=GO / boundary_ok=true / ready_for_roadmap_decision=true`
- 至少 6 条路线候选（Route A-F）
- **Route A 被选中**：`Real Rollback Rehearsal Pre-Authorization Planning`
- **不得释放任何真实执行权限**：`real_rehearsal_execution_allowed=false`、`real_migration_execution_allowed=false`、`batch_arming_allowed=false`
- Route E（Controlled Batch Arming Planning）必须 blocked/deferred
- Verifier ≥ 260 checks（baseline 220）

## Smoke 结果

- **verifier**: GO
- **checks**: 356/260
- **selected_route**: `Route A — Real Rollback Rehearsal Pre-Authorization Planning`
- **final_decision**: `MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_ROADMAP_DECISION_READY_FOR_REAL_REHEARSAL_PRE_AUTHORIZATION_PLANNING`
- **Next**: `Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Planning-v1-001`

## 下游（已完成）

- Real Rollback Rehearsal Pre-Authorization Planning v1：`Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Planning-v1-001`（GO；531/360；final_decision 指向 Pre-Authorization DryRun）

