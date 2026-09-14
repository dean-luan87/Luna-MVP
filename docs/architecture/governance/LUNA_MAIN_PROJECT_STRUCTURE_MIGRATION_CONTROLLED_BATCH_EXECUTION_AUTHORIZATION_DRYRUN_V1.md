# Luna — Main Project Structure Migration Controlled Batch Execution Authorization DryRun v1

## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Authorization-DryRun-v1-001`
- **性质**: dry-run only（只模拟“最后一道真实执行授权闸门规划”的可消费性）
- **上游输入**:
  - `main_project_structure_migration_controlled_batch_execution_authorization_planning_v1_smoke_v0`（verifier=GO）

## 目标

对 Controlled Batch Execution Authorization Planning 产出的对象做 dry-run 消费模拟，覆盖：

- B0–B7 controlled execution authorization scope
- request / grant schema
- precondition gates
- execution window
- file operation allowlist / blocklist
- verifier rerun plan
- rollback rehearsal requirement
- abort condition matrix
- post-migration test plan
- non-claims（防误读）

## 强制边界（必须为 false / 不发生）

本阶段 **不** 允许发生以下行为：

- 不发起 authorization request、不授予 authorization
- 不 batch arming、不开始 batch 执行
- 不进行任何真实文件操作（move/delete/rename/merge/copy/overwrite/archive）
- 不 rerun verifier
- 不执行 rollback rehearsal
- 不执行 post-migration tests
- 不修改 `_eval_out`、不触碰 protected / HR / DnAE

## 产物（17 类）

输出目录：

- `_eval_out/main_project_structure_migration_controlled_batch_execution_authorization_dryrun_v1_smoke_v0/`

产物文件：

1. `controlled_batch_execution_authorization_dryrun_policy_v1.json`
2. `controlled_batch_execution_authorization_planning_input_review_v1.json`
3. `b0_b7_controlled_execution_authorization_scope_dryrun_v1.json`
4. `controlled_execution_authorization_request_schema_dryrun_v1.json`
5. `controlled_execution_authorization_grant_schema_dryrun_v1.json`
6. `controlled_execution_precondition_gate_dryrun_v1.json`
7. `controlled_execution_window_dryrun_v1.json`
8. `controlled_execution_file_operation_allowlist_dryrun_v1.json`
9. `controlled_execution_file_operation_blocklist_dryrun_v1.json`
10. `controlled_execution_verifier_rerun_plan_dryrun_v1.json`
11. `controlled_execution_rollback_rehearsal_requirement_dryrun_v1.json`
12. `controlled_execution_abort_condition_dryrun_v1.json`
13. `controlled_execution_post_migration_test_plan_dryrun_v1.json`
14. `controlled_execution_non_claims_dryrun_v1.json`
15. `controlled_batch_execution_authorization_dryrun_readiness_decision_v1.json`
16. `summary.json`
17. `verifier_report.json`

## Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Authorization-Post-DryRun-Review-v1-001`

## Non-Claims（明确不等于什么）

- DryRun GO ≠ execution authorization request sent
- request/grant schema pass ≠ request sent / ≠ execution authorized
- execution authorized（未来）≠ batch armed（未来）≠ batch executed（未来）
- allowlist/blocklist pass ≠ file operation executed
- verifier rerun plan pass ≠ verifier rerun executed
- rollback requirement pass ≠ rollback rehearsal executed
- post-migration test plan pass ≠ tests executed
- workspace_fallback GO ≠ 标准 `_eval_out` 已落盘

