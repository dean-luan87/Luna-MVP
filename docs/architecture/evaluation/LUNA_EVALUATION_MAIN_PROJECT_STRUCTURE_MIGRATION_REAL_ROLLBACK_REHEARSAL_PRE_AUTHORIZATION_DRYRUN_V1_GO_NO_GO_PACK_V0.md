# GO / NO-GO Pack — Real Rollback Rehearsal Pre-Authorization DryRun v1（V0）

## Phase

- `Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001`
- scope: `pre_authorization_dryrun_only=true` + `simulated=true`

## Inputs（read-only）

- `_eval_out/main_project_structure_migration_real_rollback_rehearsal_pre_authorization_planning_v1_smoke_v0/`
  - `summary.json`
  - `verifier_report.json`
  - 10 类 planning 核心对象（owner/operator、window、sandbox/branch、restore map、restore op、verifier、evidence、success claim、readiness）

## Outputs

- `_eval_out/main_project_structure_migration_real_rollback_rehearsal_pre_authorization_dryrun_v1_smoke_v0/`
  - 10 类 dryrun 核心对象（policy + 8 evaluations/decisions + readiness）
  - `summary.json`
  - `verifier_report.json`

## GO 条件

- `verifier=GO`
- `boundary_ok=true`
- 上游 planning `verifier=GO` 且 `ready_for_pre_authorization_dryrun=true`
- 10 类 dryrun 对象生成且全部 `*_authorized_now=false / *_granted_now=false / *_opened_now=false / *_executed_now=false`
- success claim gate 仍为 blocked
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Post-DryRun-Review-v1-001`

## NO-GO 条件（任一触发即 NO-GO）

- 任一真实授权被标记为 granted/authorized（包括 sandbox/branch/restore map/verifier/evidence）
- execution window 被标记为 opened
- 发生 sandbox/branch 创建、restore map 生成、restore operation 执行、verifier rerun、evidence 生成、success claim 允许
- 释放 real rehearsal execution / real migration execution / batch arming
- 出现真实文件 move/delete/rename/merge 或 runtime/subprocess/WorldModel 写入
- final decision 越级指向真实执行

