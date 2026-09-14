## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Guarded-Roadmap-Decision-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_guarded_roadmap_decision_v1.py`
- **Status**: roadmap-decision-only（路线裁决，不执行迁移）

## Intent

在 **Guarded Closure** 后裁决下一步主线。评估 10 条路线（A–J），默认选中：

**Migration Execution Control and Test Harness Planning**

不选中：真实迁移执行、白盒/测试中心结构优化、Developer Backend 定稿、Docs 重组（均 deferred/blocked）。

## Selected Route (A)

- 定义真实迁移前的 **执行控制计划** 与 **测试 harness 准备**
- 范围：batch arming、abort condition、post-migration verifier suite、rollback rehearsal requirement
- **仍为 planning-only**，不搬文件、不执行测试、不确认 owner

## Inputs

- `main_project_structure_migration_guarded_closure_v1_smoke_v0`（required）
- guarded post-review / dryrun / planning / readiness
- 上游 PAHR closure、consolidation closure、structure map、gate taxonomy

## Outputs

`_eval_out/main_project_structure_migration_guarded_roadmap_decision_v1_smoke_v0/`

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_ROADMAP_DECISION_READY_FOR_EXECUTION_CONTROL_AND_TEST_HARNESS_PLANNING`
- **Next**: `Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Planning-v1-001`

## Non-Claims

- roadmap GO ≠ 真实搬迁可执行
- roadmap GO ≠ post-migration tests 可执行
- roadmap GO ≠ owner 已确认
- 选中 Route A 仍为 planning，不等于 file move 已授权

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Guarded-Roadmap-Decision-v1-001**: **GO**（smoke：262 checks）
- **Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Planning-v1-001**: **GO**（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_PLANNING_V1.md`）
- **Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-DryRun-v1-001**: **GO**（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_DRYRUN_V1.md`）
- **Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Post-DryRun-Review-v1-001**: **GO**（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_POST_DRYRUN_REVIEW_V1.md`）
- **Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Closure-v1-001**: **GO**（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSURE_V1.md`）
- **Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-DryRun-v1-001**: pending
