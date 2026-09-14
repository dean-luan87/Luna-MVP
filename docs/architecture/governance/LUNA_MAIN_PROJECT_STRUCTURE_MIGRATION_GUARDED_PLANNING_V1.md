## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Guarded-Planning-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_guarded_planning_v1.py`
- **Status**: guarded-planning-only（不执行真实迁移）

## Intent

在 Readiness and Test Plan GO 之后，冻结未来受控迁移的：

- **B0–B7** 批次计划（候选 scope / 排除 scope / 前后检查 / 回滚点）
- **10** 项批次 gate 序列
- 候选 scope / 排除 scope / 批次前检查 / 批次后测试绑定
- **31** 项迁移后测试矩阵（绑定到批次）
- 人工确认点与回滚 checkpoint 策略

## Inputs

- `main_project_structure_migration_readiness_and_test_plan_v1_smoke_v0`（required）
- roadmap / PAHR closure / consolidation closure / structure map / gate taxonomy 等（见 capability `ROOT_SPECS`）

## Outputs

`_eval_out/main_project_structure_migration_guarded_planning_v1_smoke_v0/`

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Main-Project-Structure-Migration-Guarded-DryRun-v1-001`

## Non-Claims

- guarded planning GO ≠ 真实搬迁可执行
- 测试矩阵已绑定 ≠ 测试已执行
- 不设计白盒/测试中心物理结构

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Guarded-DryRun-v1-001**: **GO**（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_DRYRUN_V1.md`）
- **Phase-Main-Project-Structure-Migration-Guarded-Post-DryRun-Review-v1-001**: **GO**（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_POST_DRYRUN_REVIEW_V1.md`）
- **Phase-Main-Project-Structure-Migration-Guarded-Closure-v1-001**: **GO**（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSURE_V1.md`）
