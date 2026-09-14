## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Planning-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_rollback_rehearsal_execution_planning_v1.py`
- **Status**: planning-only（定义真实 rollback rehearsal 执行前置，不执行 rehearsal）

## Intent

在 Roadmap Decision（Route A）之后，规划真实 rollback rehearsal execution 的：

- 准入门（RehearsalExecutionGate，≥14 项）
- Sandbox/branch 创建规则（仅规划，不创建）
- Owner/operator approval（≥8 项要求）
- 执行窗口（≥8 项要求）
- Restore map / restore 操作权限边界
- Verifier rerun / evidence / failure response / success claim gate

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-DryRun-v1-001`

## Non-Claims

- Planning GO ≠ sandbox/branch 已创建 ≠ rehearsal 已执行 ≠ evidence 已生成

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Roadmap-Decision-v1-001**: **GO**（286/220 checks）
- **Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Planning-v1-001**: **GO**（443/340 checks）
- **Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-DryRun-v1-001**: **GO**（426/380 checks；见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_DRYRUN_V1.md`）
- **Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Post-DryRun-Review-v1-001**: **GO**（364/360 checks；见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_POST_DRYRUN_REVIEW_V1.md`）
- **Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Roadmap-Decision-v1-001**: **GO**（356/260 checks；见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_ROADMAP_DECISION_V1.md`）
