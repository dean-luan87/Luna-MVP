## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Readiness-and-Test-Plan-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_readiness_and_test_plan_v1.py`
- **Status**: planning-only（不执行真实迁移、不读文件内容、不调用 stat/exists/runtime）

## Intent

为 Luna-Core 主工程结构迁移建立：

- **MigrationReadinessGate** — 迁移前置门（GO/NO-GO 条件）
- **MigrationAllowedScope** / **MigrationForbiddenScope** — 允许候选 vs 禁止范围
- **PreMigrationChecklist** — 迁移前检查要求（仅定义，本阶段不执行）
- **PostMigrationTestPlan** — 迁移后测试矩阵（A–E 五组，仅定义）
- **MigrationRollbackRequirement** — 回滚批次与恢复要求
- **WhiteboxTestCenterDefermentPolicy** — 白盒/测试中心延后至主工程迁移+测试后
- **FutureReservedModuleConstraint** — 14 个 future_reserved 模块约束

冻结 **240 HR** / **914 permanent block** carryover；不解除 protected asset / permanent block。

## Inputs（13 roots + 必选 artifacts）

| intake | `_eval_out` smoke root |
|--------|-------------------------|
| roadmap_decision | `post_protected_asset_and_human_review_resolution_roadmap_decision_v1_smoke_v0` |
| pahr_closure | `protected_asset_and_human_review_resolution_closure_v1_smoke_v0` |
| pahr_post_review | `protected_asset_and_human_review_resolution_post_dryrun_review_v1_smoke_v0` |
| pahr_dryrun | `protected_asset_and_human_review_resolution_dryrun_v1_smoke_v0` |
| pahr_planning | `protected_asset_and_human_review_resolution_planning_v1_smoke_v0` |
| consolidation_roadmap | `luna_project_structure_consolidation_roadmap_decision_v1_smoke_v0` |
| consolidation_closure | `luna_project_structure_consolidation_closure_v1_smoke_v0` |
| consolidation_post_review | `luna_project_structure_consolidation_post_dryrun_review_v1_smoke_v0` |
| consolidation_dryrun | `luna_project_structure_consolidation_dryrun_v1_smoke_v0` |
| consolidation_planning | `luna_project_structure_consolidation_planning_v1_smoke_v0` |
| structure_map | `luna_project_module_inventory_and_structure_map_dryrun_v1_smoke_v0` |
| structure_governance | `luna_project_structure_governance_and_modularization_planning_v1_smoke_v0` |
| gate_taxonomy | `gate_taxonomy_and_requirement_framework_planning_v1_smoke_v0` |

必读 artifacts 含 `main_project_migration_readiness_route_decision.json`、`current_to_target_structure_map.json`、`human_review_carryover_for_future_execution.json`、`permanent_block_carryover_for_future_governance.json` 等（见 capability `REQUIRED_ARTIFACTS`）。

## Outputs

`_eval_out/main_project_structure_migration_readiness_and_test_plan_v1_smoke_v0/`：

- `main_project_migration_readiness_policy.json`
- `migration_readiness_gate.json` / `migration_allowed_scope.json` / `migration_forbidden_scope.json`
- `pre_migration_checklist.json` / `post_migration_test_plan.json` / `migration_rollback_requirement.json`
- `whitebox_test_center_deferment_policy.json` / `future_reserved_module_constraint.json`
- `migration_readiness_decision.json` / `governance_debt_register.json`
- 四类 boundary report（no file move / delete / runtime / write）

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_READINESS_AND_TEST_PLAN_READY_FOR_GUARDED_MIGRATION_PLANNING`
- **Next**: `Phase-Main-Project-Structure-Migration-Guarded-Planning-v1-001`

## Non-Claims

- readiness GO ≠ 真实搬迁可执行
- post-migration test plan 已定义 ≠ 测试已执行通过
- 240 HR / 914 permanent block 仍未解除
- 白盒/测试中心 / Developer Backend 整体结构本阶段不定稿

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Guarded-Planning-v1-001**: **GO**（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_PLANNING_V1.md`）
- **Phase-Main-Project-Structure-Migration-Guarded-DryRun-v1-001**: **GO**
- **Phase-Main-Project-Structure-Migration-Guarded-Post-DryRun-Review-v1-001**: **GO**
- **Phase-Main-Project-Structure-Migration-Guarded-Closure-v1-001**: **GO**（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSURE_V1.md`）
- **Phase-Main-Project-Structure-Migration-Guarded-Roadmap-Decision-v1-001**: **GO**
- **Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Planning-v1-001**: **GO**
- **Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-DryRun-v1-001**: pending
