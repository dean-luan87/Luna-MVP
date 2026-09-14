## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Guarded-Closure-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_guarded_closure_v1.py`
- **Status**: closure-only（冻结受控迁移链条，不释放真实搬迁）

## Intent

对 **Readiness → Guarded Planning → Guarded DryRun → Guarded Post-DryRun Review** 四阶段做正式 closure：

- 冻结批次 / gate / 排除范围 / 测试矩阵 / rollback checkpoint / HumanApproval 占位状态
- 登记 **correction_record**（post-review `rollback_executed` 字段布尔语义修复，不授予任何权限）
- 输出 **non-claims**、**deferred action pool**、**closure boundary freeze**

## 写死的 Non-Claims

- **Guarded Closure ≠ 可真实搬迁**
- **Guarded Closure ≠ 可执行 post-migration tests**
- **Guarded Closure ≠ owner 已确认**
- **Guarded Closure ≠ protected / HR / DnAE 可处理**

## Inputs

- `main_project_structure_migration_guarded_post_dryrun_review_v1_smoke_v0`（required）
- `main_project_structure_migration_guarded_dryrun_v1_smoke_v0`（required）
- `main_project_structure_migration_guarded_planning_v1_smoke_v0`（required）
- `main_project_structure_migration_readiness_and_test_plan_v1_smoke_v0`（required）
- 上游 roadmap / PAHR closure / consolidation closure / structure map / gate taxonomy

## Outputs

`_eval_out/main_project_structure_migration_guarded_closure_v1_smoke_v0/`

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE`
- **Next**: `Phase-Main-Project-Structure-Migration-Guarded-Roadmap-Decision-v1-001`

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Guarded-Closure-v1-001**: **GO**（smoke：`verify_main_project_structure_migration_guarded_closure_v1`，275 checks）
- **Phase-Main-Project-Structure-Migration-Guarded-Roadmap-Decision-v1-001**: **GO**（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_ROADMAP_DECISION_V1.md`）
- **Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Planning-v1-001**: **GO**
