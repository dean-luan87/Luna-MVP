## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Stabilized-Execution-Planning-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_stabilized_execution_planning_v1.py`
- **Status**: execution-planning-only（一次性定死「怎么迁」；不执行真实文件操作）

## Intent

从 **Stabilized Resume Planning** 进入工程结构稳定化执行规划。将 B0–B7 执行顺序、每批输入输出、前置 gate、回滚路线、测试清单、verifier rerun 清单全部冻结，供后续 DryRun 仅模拟、不再重议目录结构。

## Upstream

- `_eval_out/main_project_structure_migration_stabilized_resume_planning_v1_smoke_v0/`（verifier=GO）

## B0–B7（单域、冻结）

| Batch | 域 | 规划内容 |
|-------|-----|----------|
| B0 | docs_index_only | README / phase table 对齐 |
| B1 | governance_docs_only | governance 文档稳定落位 |
| B2 | architecture_docs_only | architecture / evaluation 文档稳定落位 |
| B3 | capabilities_only | capability 模块稳定落位 |
| B4 | runners_verifiers_only | runner / verifier 稳定落位 |
| B5 | config_schema_only | config / schema / examples 稳定落位 |
| B6 | tools_scripts_tests_only | tools / scripts / tests 稳定落位 |
| B7 | verification_gate_only | 交叉引用 / import / path 一致性 |

每批必须具备：before/after manifest plan、rollback route、verifier rerun list、abort conditions、`touched_paths_candidate`（本阶段不 touch）、`protected_path_intersection=false`、`eval_out_write_allowed=false`。

## 产物（smoke）

1. `stabilized_execution_planning_policy_v1.json`
2. `resume_planning_input_review_v1.json`
3. `b0_b7_execution_batch_plan_v1.json`
4. `batch_pre_gate_matrix_v1.json`
5. `batch_before_after_manifest_plan_v1.json`
6. `batch_rollback_route_plan_v1.json`
7. `batch_verifier_rerun_plan_v1.json`
8. `batch_protected_asset_guard_matrix_v1.json`
9. `batch_eval_out_readonly_guard_v1.json`
10. `batch_domain_isolation_matrix_v1.json`
11. `batch_abort_condition_matrix_v1.json`
12. `stabilized_execution_planning_readiness_decision_v1.json`
13. `summary.json`
14. `verifier_report.json`

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_EXECUTION_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Main-Project-Structure-Migration-Stabilized-Execution-DryRun-v1-001`

## Implementation Status

- **GO**（432/420 checks）
