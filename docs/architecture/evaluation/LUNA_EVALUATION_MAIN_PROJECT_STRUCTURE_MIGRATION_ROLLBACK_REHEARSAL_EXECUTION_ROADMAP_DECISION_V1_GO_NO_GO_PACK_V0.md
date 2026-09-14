# GO / NO-GO Pack — Rollback Rehearsal Execution Roadmap Decision v1（V0）

## Phase

- `Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Roadmap-Decision-v1-001`
- scope: `roadmap_decision_only=true`

## Inputs（read-only）

- `_eval_out/main_project_structure_migration_rollback_rehearsal_execution_post_dryrun_review_v1_smoke_v0/`
  - `summary.json`
  - `verifier_report.json`
  - 9 类 post-dryrun review 产物（policy/completeness/freeze/continuity/non-executable/success-claim/boundary/issues/readiness）

## Outputs

- `_eval_out/main_project_structure_migration_rollback_rehearsal_execution_roadmap_decision_v1_smoke_v0/`
  - 8 类 roadmap decision 对象（policy/chain review/route matrix/dependency matrix/selected route/permission non-release/non-claims/readiness）
  - `summary.json`
  - `verifier_report.json`

## GO 条件

- `verifier=GO`
- `boundary_ok=true`
- Route A 被选中：`Route A — Real Rollback Rehearsal Pre-Authorization Planning`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_ROADMAP_DECISION_READY_FOR_REAL_REHEARSAL_PRE_AUTHORIZATION_PLANNING`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Planning-v1-001`
- 真实执行权限全部保持 false（至少包括 rehearsal / migration / batch arming / sandbox / branch / restore / verifier rerun / evidence / success claim）

## NO-GO 条件（任一触发即 NO-GO）

- 任一真实执行权限被释放（任一 “*_allowed=true” / “*_committed=true” / “*_created_now=true”）
- final decision 指向真实 rollback rehearsal execution / real migration execution / batch arming
- 发生 sandbox/branch 创建、restore map 生成、restore operation 执行、verifier rerun、真实 evidence 生成、success claim 声明
- 发生真实文件 move/delete/rename/merge
- 发生 runtime/subprocess 或 WorldModel/Memory/Fact/Library write

