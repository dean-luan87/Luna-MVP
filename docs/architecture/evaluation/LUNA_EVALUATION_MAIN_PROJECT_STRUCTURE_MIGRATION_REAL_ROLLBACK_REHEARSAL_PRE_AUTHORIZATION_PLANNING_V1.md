# Luna Evaluation — Real Rollback Rehearsal Pre-Authorization Planning v1

**Phase**：`Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Planning-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_real_rollback_rehearsal_pre_authorization_planning_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_real_rollback_rehearsal_pre_authorization_planning_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_real_rollback_rehearsal_pre_authorization_planning_v1.py
```

## 通过条件（摘要）

- 必须读取上游 Execution Roadmap Decision 输出，并确认：
  - `verifier=GO`、`boundary_ok=true`
  - `selected_route=Route A — Real Rollback Rehearsal Pre-Authorization Planning`
  - `recommended_next_phase=Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Planning-v1-001`
  - `real_rehearsal_execution_allowed=false`、`real_migration_execution_allowed=false`、`batch_arming_allowed=false`
- 必须生成 10 类核心对象（owner/operator、window、sandbox/branch、restore map、restore op、verifier rerun、evidence、success claim gate 等）
- **授权不得被误读为已授权**：`authorization_granted_now=false`，且 `ready_for_real_rollback_rehearsal_execution=false`
- Verifier ≥ 360 checks（baseline 300）

## Smoke 结果

- **verifier**: GO
- **checks**: 531/360
- **final_decision**: `MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001`

## 下游（已完成）

- Pre-Authorization DryRun v1：`Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001`（GO；604/420；final_decision 指向 Pre-Authorization Post-DryRun Review）

