## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Guarded-DryRun-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_guarded_dryrun_v1.py`
- **Status**: dry-run-only（模拟 B0–B7 gate 串联，不搬文件）

## Intent

验证 **能否串起来**，而非 **能否真搬**：

- B0–B7 每批 gate / 前置检查 / 排除范围 / 测试绑定 / 回滚点 / 人工确认点 **模拟通过**
- 10 项 gate 序列 dry-run 汇总
- 31 项 post-migration 测试 **全部绑定、0 执行**
- 17+ 类排除范围持续有效

## Inputs

- `main_project_structure_migration_guarded_planning_v1_smoke_v0`（required）
- `main_project_structure_migration_readiness_and_test_plan_v1_smoke_v0`（required）
- 上游 closure / structure map / gate taxonomy（见 capability `ROOT_SPECS`）

## Outputs

`_eval_out/main_project_structure_migration_guarded_dryrun_v1_smoke_v0/`

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **Next**: `Phase-Main-Project-Structure-Migration-Guarded-Post-DryRun-Review-v1-001`

## Non-Claims

- dry-run GO ≠ 真实迁移可执行
- 测试绑定完成 ≠ 测试已执行
- `requires_review` 的 HumanApproval gate 仅为占位，非 owner 已确认

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Guarded-Post-DryRun-Review-v1-001**: **GO**（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_POST_DRYRUN_REVIEW_V1.md`）
- **Phase-Main-Project-Structure-Migration-Guarded-Closure-v1-001**: **GO**（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSURE_V1.md`）
