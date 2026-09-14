## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Controlled-Execution-Roadmap-Decision-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_controlled_execution_roadmap_decision_v1.py`
- **Status**: roadmap-decision-only（不执行真实迁移）

## Selected Route

**Real Migration Pre-Authorization and Rollback Rehearsal Planning**（Route A，P0）

### 理由

- Controlled Execution 链已闭环，但 `real_migration_execution_allowed=false`
- `owner_approval_executed=false`；`rollback_rehearsal_executed=false`
- 真实迁移前必须先规划 **owner/授权解析** 与 **rollback rehearsal**
- Route B/C 并入 A；Route E/F **blocked**；Route D/G/H/I **deferred**；Route J discussion only

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_ROADMAP_DECISION_READY_FOR_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_PLANNING`
- **Next**: `Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Planning-v1-001`

## Non-Claims

- Roadmap GO ≠ 真实迁移 / batch armed / rollback rehearsal 已执行 / owner 已确认

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Controlled-Execution-Closure-v1-001**: **GO**（285 checks）
- **Phase-Main-Project-Structure-Migration-Controlled-Execution-Roadmap-Decision-v1-001**: **GO**
- **Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Planning-v1-001**: **GO**（482/320 checks；见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_PLANNING_V1.md`）
- **Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-DryRun-v1-001**: **GO**（401/360 checks）
- **Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Post-DryRun-Review-v1-001**: **GO**（400/340 checks）
