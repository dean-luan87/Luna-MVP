## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Planning-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_execution_control_and_test_harness_planning_v1.py`
- **Status**: planning-only（定义执行控制与测试 harness，不执行迁移/测试/回滚演练）

## Intent

在 Guarded Roadmap Decision 选中 Route A 后，定义：

- **何时允许启动**真实迁移（ExecutionControlGate GO/NO-GO）
- **如何一键停止**（AbortConditionPolicy，16 项 abort 条件）
- **B0–B7 batch arming**（本阶段不 armed）
- **迁移后怎么测**（31 项 → 5 组 PostMigrationTestHarness）
- **失败怎么回滚**（RollbackRehearsalRequirement + FailureResponseMatrix）

## 核心产物

| 产物 | 说明 |
|------|------|
| `execution_control_gate.json` | 真实迁移前硬门 GO/NO-GO |
| `batch_arming_policy.json` | 8 批次 arming 前置条件（arming_allowed_now=false） |
| `abort_condition_policy.json` | 16 项 abort 条件 |
| `pre_execution_checklist.json` | 14 项迁移前 checklist（不执行） |
| `post_migration_test_harness.json` | A–E 五组 harness，31 测试 |
| `post_migration_verifier_suite.json` | 12 项 verifier（4 required + 8 optional_if_missing） |
| `rollback_rehearsal_requirement.json` | 回滚演练要求（rehearsal_execution_allowed_now=false） |

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-DryRun-v1-001`

## Non-Claims

- planning GO ≠ 真实迁移 / batch armed / 测试已执行 / rollback rehearsal 已执行 / verifier suite 已执行
- planning GO ≠ owner 已确认

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Planning-v1-001**: **GO**（305 checks）
- **Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-DryRun-v1-001**: **GO**（354 checks；见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_DRYRUN_V1.md`）
- **Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Post-DryRun-Review-v1-001**: **GO**（320 checks；见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_POST_DRYRUN_REVIEW_V1.md`）
- **Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Closure-v1-001**: **GO**（286 checks；见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSURE_V1.md`）
- **Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Roadmap-Decision-v1-001**: pending
