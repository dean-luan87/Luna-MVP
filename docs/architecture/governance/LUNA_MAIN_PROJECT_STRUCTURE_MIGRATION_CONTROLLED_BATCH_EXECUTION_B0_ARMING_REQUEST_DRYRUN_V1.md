# Luna — Main Project Structure Migration Controlled Batch Execution B0 Arming Request DryRun v1

## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-B0-Arming-Request-DryRun-v1-001`
- **性质**: request dry-run only（只模拟消费，不生成/发送 request，不授权，不 arming，不执行）
- **收窄策略**: **仅 B0**；B1–B7 保持 deferred
- **上游输入**:
  - `Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-B0-Arming-Request-Planning-v1-001`（verifier=GO）

## 目标

对 `B0 Arming Request Planning` 产物做 dry-run 消费验证，仅模拟以下对象是否可消费：

- identity
- scope
- precondition gates
- forbidden scope
- manifest requirement
- rollback requirement
- verifier rerun requirement
- post-migration test requirement
- abort / revoke
- non-claims（防误读）

## 强制边界（必须为 false / 不发生）

- 不生成 request artifact，不发送 request，不授予授权
- 不 arming，不打开 execution window，不执行 batch
- 不做真实文件操作，不 rerun verifier，不执行 rollback rehearsal，不跑 post-migration tests
- `_eval_out` / protected / HR / DnAE 永久冻结
- workspace_fallback **不** 等于标准 `_eval_out` 已落盘

## 产物（15 类）

输出目录：

- `_eval_out/main_project_structure_migration_controlled_batch_execution_b0_arming_request_dryrun_v1_smoke_v0/`

产物文件：

1. `b0_arming_request_dryrun_policy_v1.json`
2. `b0_arming_request_planning_input_review_v1.json`
3. `b0_arming_request_identity_dryrun_v1.json`
4. `b0_arming_request_scope_dryrun_v1.json`
5. `b0_arming_request_precondition_gate_dryrun_v1.json`
6. `b0_arming_request_forbidden_scope_dryrun_v1.json`
7. `b0_arming_request_manifest_requirement_dryrun_v1.json`
8. `b0_arming_request_rollback_requirement_dryrun_v1.json`
9. `b0_arming_request_verifier_rerun_requirement_dryrun_v1.json`
10. `b0_arming_request_post_migration_test_requirement_dryrun_v1.json`
11. `b0_arming_request_abort_revoke_dryrun_v1.json`
12. `b0_arming_request_non_claims_dryrun_v1.json`
13. `b0_arming_request_dryrun_readiness_decision_v1.json`
14. `summary.json`
15. `verifier_report.json`

## Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_B0_ARMING_REQUEST_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-B0-Arming-Request-Post-DryRun-Review-v1-001`

## Non-Claims（明确不等于什么）

- B0 Arming Request DryRun GO ≠ request artifact generated
- request artifact generated in future ≠ request sent
- request sent in future ≠ arming authorized
- arming authorized in future ≠ B0 armed
- B0 armed in future ≠ B0 executed
- B0 execution in future ≠ B1–B7 allowed
- manifest requirement pass ≠ manifest generated
- verifier rerun requirement pass ≠ verifier rerun executed
- rollback requirement pass ≠ rollback rehearsal executed
- post-migration test requirement pass ≠ tests executed
- workspace_fallback GO ≠ standard `_eval_out` already written

