## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Stabilized-Execution-DryRun-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_stabilized_execution_dryrun_v1.py`
- **Status**: execution-dryrun-only（只模拟消费 planning 产物；不做真实文件迁移）

## Intent

对 **Stabilized Execution Planning** 的 B0–B7 计划进行 dry-run：验证每批的 pre-gate、before/after manifest plan、rollback route、verifier rerun list（不执行）、abort conditions、protected guard、`_eval_out` readonly guard、domain isolation 能串起来，且全程保持无真实 file operation。

## Upstream

- `_eval_out/main_project_structure_migration_stabilized_execution_planning_v1_smoke_v0/`（verifier=GO）

## Outputs

输出目录：`_eval_out/main_project_structure_migration_stabilized_execution_dryrun_v1_smoke_v0/`

1. `stabilized_execution_dryrun_policy_v1.json`
2. `execution_planning_input_review_v1.json`
3. `b0_b7_batch_dryrun_trace_v1.json`
4. `batch_pre_gate_dryrun_result_v1.json`
5. `batch_before_after_manifest_dryrun_v1.json`
6. `batch_rollback_route_dryrun_v1.json`
7. `batch_verifier_rerun_dryrun_v1.json`
8. `batch_protected_asset_guard_dryrun_v1.json`
9. `batch_eval_out_readonly_guard_dryrun_v1.json`
10. `batch_domain_isolation_dryrun_v1.json`
11. `batch_abort_condition_dryrun_v1.json`
12. `stabilized_execution_dryrun_readiness_decision_v1.json`
13. `summary.json`
14. `verifier_report.json`

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_EXECUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **Next**: `Phase-Main-Project-Structure-Migration-Stabilized-Execution-Post-DryRun-Review-v1-001`

