# Luna — Main Project Structure Migration Controlled Batch Execution B0 Arming Request Planning v1

## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-B0-Arming-Request-Planning-v1-001`
- **性质**: request planning only（只规划，不生成/发送 request，不授权，不 arming，不执行）
- **收窄策略**: **仅 B0**；不展开大治理链；B1–B7 保持 deferred
- **上游输入**:
  - `Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Arming-Post-DryRun-Review-v1-001`（verifier=GO）

## 目标

冻结 B0 arming request 的最小请求结构：

- 谁请求 / 谁批准（identity）
- 请求 arming 的 batch（B0）
- 请求范围（docs 索引/README/phase table alignment 候选）
- 前置条件（gate）
- 禁止范围与禁止操作（forbidden scope / operations）
- manifest / rollback / verifier rerun / post-migration test 的要求（requirements）
- abort / revoke 条件
- non-claims（防误读）

## 强制边界（必须为 false / 不发生）

- 不生成 request artifact，不发送 request，不授予授权
- 不 arming，不打开 execution window，不执行 batch
- 不做真实文件操作，不 rerun verifier，不执行 rollback rehearsal，不跑 post-migration tests
- `_eval_out` / protected / HR / DnAE 永久冻结

## 产物（15 类）

输出目录：

- `_eval_out/main_project_structure_migration_controlled_batch_execution_b0_arming_request_planning_v1_smoke_v0/`

产物文件：

1. `b0_arming_request_planning_policy_v1.json`
2. `b0_arming_post_dryrun_review_input_review_v1.json`
3. `b0_arming_request_identity_planning_v1.json`
4. `b0_arming_request_scope_planning_v1.json`
5. `b0_arming_request_precondition_gate_planning_v1.json`
6. `b0_arming_request_forbidden_scope_planning_v1.json`
7. `b0_arming_request_manifest_requirement_planning_v1.json`
8. `b0_arming_request_rollback_requirement_planning_v1.json`
9. `b0_arming_request_verifier_rerun_requirement_planning_v1.json`
10. `b0_arming_request_post_migration_test_requirement_planning_v1.json`
11. `b0_arming_request_abort_revoke_planning_v1.json`
12. `b0_arming_request_non_claims_register_v1.json`
13. `b0_arming_request_planning_readiness_decision_v1.json`
14. `summary.json`
15. `verifier_report.json`

## Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_B0_ARMING_REQUEST_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-B0-Arming-Request-DryRun-v1-001`

## Non-Claims（明确不等于什么）

- Request Planning GO ≠ request artifact generated
- request artifact generated in future ≠ request sent
- request sent in future ≠ arming authorized
- arming authorized in future ≠ B0 armed
- B0 armed in future ≠ B0 executed
- B0 execution in future ≠ B1–B7 allowed
- workspace_fallback GO ≠ standard `_eval_out` already written

