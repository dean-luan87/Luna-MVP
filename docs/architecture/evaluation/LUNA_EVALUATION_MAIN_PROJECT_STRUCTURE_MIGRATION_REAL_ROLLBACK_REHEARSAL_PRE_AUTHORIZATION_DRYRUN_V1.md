# Luna Evaluation — Real Rollback Rehearsal Pre-Authorization DryRun v1

**Phase**：`Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_real_rollback_rehearsal_pre_authorization_dryrun_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_real_rollback_rehearsal_pre_authorization_dryrun_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_real_rollback_rehearsal_pre_authorization_dryrun_v1.py
```

## 通过条件（摘要）

- 必须读取上游 Pre-Authorization Planning 输出，并确认其 `verifier=GO / boundary_ok=true / ready_for_pre_authorization_dryrun=true`
- 必须生成 10 类 dry-run 核心对象（owner/operator、window、sandbox/branch、restore map、restore op、verifier、evidence、success claim gate 等）
- 所有授权与执行权限字段保持 false：`authorization_granted_now=false` 且 `real_rehearsal_execution_allowed=false`
- final decision 必须指向 Pre-Authorization Post-DryRun Review
- Verifier ≥ 420 checks（baseline 340）

## Smoke 结果

- **verifier**: GO
- **checks**: 604/420
- **final_decision**: `MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **Next**: `Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Post-DryRun-Review-v1-001`

