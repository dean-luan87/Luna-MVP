## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Stabilized-Batch-Authorization-DryRun-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_stabilized_batch_authorization_dryrun_v1.py`
- **Status**: batch-authorization-dryrun-only（只模拟消费授权规划；不发 request、不 grant、不 arming、不执行）

## Intent

对 Stabilized Batch Authorization Planning 的 B0–B7 授权规划做 dry-run：只模拟消费 scope / request schema / grant schema / gates / execution window / verifier rerun authorization / rollback authorization / file operation boundary / protected+eval_out guards，验证可串联且全程保持非执行边界。

若标准 `_eval_out` 不可写或输入来自 workspace，则 `summary.source_path_mode=workspace_fallback`，并明确提示本机复现会写入标准 `_eval_out`。

## Upstream

- `_eval_out/main_project_structure_migration_stabilized_batch_authorization_planning_v1_smoke_v0/`（verifier=GO）

## Outputs

输出目录：`_eval_out/main_project_structure_migration_stabilized_batch_authorization_dryrun_v1_smoke_v0/`

1. `stabilized_batch_authorization_dryrun_policy_v1.json`
2. `batch_authorization_planning_input_review_v1.json`
3. `b0_b7_authorization_scope_dryrun_v1.json`
4. `batch_authorization_request_schema_dryrun_v1.json`
5. `batch_authorization_grant_schema_dryrun_v1.json`
6. `batch_pre_authorization_gate_dryrun_v1.json`
7. `batch_execution_window_dryrun_v1.json`
8. `batch_verifier_rerun_authorization_dryrun_v1.json`
9. `batch_rollback_authorization_dryrun_v1.json`
10. `batch_file_operation_permission_boundary_dryrun_v1.json`
11. `batch_protected_eval_out_guard_dryrun_v1.json`
12. `batch_authorization_non_claims_dryrun_v1.json`
13. `stabilized_batch_authorization_dryrun_readiness_decision_v1.json`
14. `summary.json`
15. `verifier_report.json`

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_BATCH_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **Next**: `Phase-Main-Project-Structure-Migration-Stabilized-Batch-Authorization-Post-DryRun-Review-v1-001`

