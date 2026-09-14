# GO / NO-GO Pack — Real Rollback Rehearsal Pre-Authorization Planning v1（V0）

## Phase

- `Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Planning-v1-001`
- scope: `pre_authorization_planning_only=true`

## Inputs（read-only）

- `_eval_out/main_project_structure_migration_rollback_rehearsal_execution_roadmap_decision_v1_smoke_v0/`
  - `summary.json`
  - `verifier_report.json`
  - `selected_route_decision_v1.json`
  - 其余 roadmap decision 产物（route matrix / dependencies / permission non-release / non-claims / readiness）

## Outputs

- `_eval_out/main_project_structure_migration_real_rollback_rehearsal_pre_authorization_planning_v1_smoke_v0/`
  - 10 类核心对象（policy/owner-operator/window/sandbox-branch/restore-map/restore-op/verifier/evidence/success-claim/readiness）
  - `summary.json`
  - `verifier_report.json`

## GO 条件

- `verifier=GO`
- `boundary_ok=true`
- 上游 roadmap decision `verifier=GO` 且 Route A 被正确消费
- 10 类核心对象生成且各自 `*_granted_now=false` / `*_opened_now=false` / `*_executed_now=false`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001`

## NO-GO 条件（任一触发即 NO-GO）

- 任一真实授权被标记为 granted（包括 owner/operator/window/restore/verifier/evidence 等）
- execution window 被标记为 opened
- 创建 sandbox/branch、生成 restore map、执行 restore operation、rerun verifier、生成 evidence、声明 rollback success
- 释放 real rehearsal execution / real migration execution / batch arming
- 出现真实文件 move/delete/rename/merge 或 runtime/subprocess/WorldModel 写入
- final decision 越级指向真实执行

