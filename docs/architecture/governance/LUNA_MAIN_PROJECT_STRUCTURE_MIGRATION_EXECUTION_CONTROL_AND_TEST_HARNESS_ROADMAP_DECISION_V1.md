## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Roadmap-Decision-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_execution_control_and_test_harness_roadmap_decision_v1.py`
- **Status**: roadmap-decision-only（选定下一主线，不释放执行权限）

## Selected Route

**Route A — Controlled Migration Execution Planning**（`selected_now=true`）

规划真实迁移执行前的 controlled execution plan：批次顺序、授权条件、执行窗口、回滚演练前置、测试/verifier 执行顺序、失败中止规则。**仍为 planning-only，不搬文件。**

**Next**: `Phase-Main-Project-Structure-Migration-Controlled-Execution-Planning-v1-001`

## Deferred / Blocked Routes

| Route | 状态 |
|-------|------|
| B Owner Approval | deferred（嵌入 Route A 前置） |
| C Rollback Rehearsal Planning | merged into A |
| D Post-Migration Test Harness Prep | merged into A |
| E Real Migration Execution Trial | **blocked** |
| F Whitebox / Test Center | deferred |
| G Developer Backend | deferred |
| H Docs Reorganization | deferred |
| I Return to Mainline | deferred |
| J Future Reserved Modules | discussion only |

## Closure Carryover

- `armed_batch_count=0`；`real_migration_execution_allowed=false`
- 31 测试绑定 / 12 verifier 编排 / rollback rehearsal required 均未执行
- 两项 correction：`no_permission_granted`

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_ROADMAP_DECISION_READY_FOR_CONTROLLED_MIGRATION_EXECUTION_PLANNING`

## Non-Claims

- roadmap GO ≠ 真实迁移 / batch armed / 测试或 verifier 已执行
- Route A 选定 ≠ 文件移动已授权

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Closure-v1-001**: **GO**（286 checks）
- **Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Roadmap-Decision-v1-001**: **GO**（248 checks）
- **Phase-Main-Project-Structure-Migration-Controlled-Execution-Planning-v1-001**: **GO**（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_V1.md`）
- **Phase-Main-Project-Structure-Migration-Controlled-Execution-DryRun-v1-001**: **GO**（426 checks）
- **Phase-Main-Project-Structure-Migration-Controlled-Execution-Post-DryRun-Review-v1-001**: pending
