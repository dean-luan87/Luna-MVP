## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Stabilized-Batch-Authorization-Planning-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_stabilized_batch_authorization_planning_v1.py`
- **Status**: batch-authorization-planning-only（真实迁移前的授权规划；不发起请求、不授予、不 arming、不执行）

## Intent

在 Stabilized Execution Post-DryRun Review 通过后，进入 **批次授权规划**：

- B0–B7 哪些 batch 可进入未来授权请求（scope candidate / excluded scope 固化）
- 每批授权前必须满足的 gate、manifest、rollback、verifier list、abort conditions 固化
- 授权请求/授予 schema 固化（但本阶段 `request_sent_now=false`、`grant_issued_now=false`）
- execution window、verifier rerun、rollback 的授权边界固化（均不执行）
- file operation permission boundary 固化（所有 `actual_file_*_executed=false`）

## Upstream

- `_eval_out/main_project_structure_migration_stabilized_execution_post_dryrun_review_v1_smoke_v0/`（verifier=GO）

## Outputs

输出目录：`_eval_out/main_project_structure_migration_stabilized_batch_authorization_planning_v1_smoke_v0/`

1. `stabilized_batch_authorization_planning_policy_v1.json`
2. `execution_post_dryrun_review_input_review_v1.json`
3. `b0_b7_batch_authorization_scope_matrix_v1.json`
4. `batch_authorization_request_schema_planning_v1.json`
5. `batch_authorization_grant_schema_planning_v1.json`
6. `batch_pre_authorization_gate_matrix_v1.json`
7. `batch_execution_window_planning_v1.json`
8. `batch_verifier_rerun_authorization_planning_v1.json`
9. `batch_rollback_authorization_planning_v1.json`
10. `batch_file_operation_permission_boundary_v1.json`
11. `batch_protected_eval_out_guard_authorization_matrix_v1.json`
12. `batch_authorization_non_claims_register_v1.json`
13. `stabilized_batch_authorization_planning_readiness_decision_v1.json`
14. `summary.json`
15. `verifier_report.json`

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_BATCH_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Main-Project-Structure-Migration-Stabilized-Batch-Authorization-DryRun-v1-001`

