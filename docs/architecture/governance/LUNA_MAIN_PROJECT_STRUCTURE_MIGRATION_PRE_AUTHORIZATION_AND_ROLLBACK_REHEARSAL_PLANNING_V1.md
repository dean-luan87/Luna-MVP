## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Planning-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_pre_authorization_and_rollback_rehearsal_planning_v1.py`
- **Status**: planning-only（定义授权与 rollback rehearsal 规划，不执行）

## Intent

在 Controlled Execution Roadmap 选中 Route A 后，把真实迁移前必须具备的治理对象写清楚：

- **7 类 owner 授权解析**（`owner_confirmed_now=false`；禁止 auto-confirm）
- **Operator acknowledgement** 策略（`operator_ack_executed_now=false`）
- **Pre-execution authorization package** 模板（11 条 included records；`package_generated_now=false`）
- **Rollback rehearsal scope / plan / evidence template**（B0–B7；11 步；`rehearsal_executed_now=false`）
- **Batch arming 前置记录**（B0–B7；`armed_batch_count=0`）
- **15 条 authorization blockers**（缺 owner / ack / rehearsal / evidence 等阻断真实迁移与 arming）

## Owner × Batch 映射（规划，非确认）

| Batch | 所需 owner |
|-------|------------|
| B1 docs relink | docs_owner + architecture_owner |
| B2 capability grouping | capability_owner + architecture_owner |
| B3 governance grouping | governance_owner + architecture_owner |
| B4 midplatform core | midplatform_owner + architecture_owner |
| B5 dev artifact reference | evaluation_owner + architecture_owner |
| B6 future marker | architecture_owner |
| B7 verification gate | evaluation_owner + architecture_owner |

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-DryRun-v1-001`

## Non-Claims

- planning GO ≠ owner 已确认 / operator ack 已执行 / authorization package 已生成
- planning GO ≠ rollback rehearsal 已执行 / batch 已 armed / 真实迁移可执行

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Controlled-Execution-Roadmap-Decision-v1-001**: **GO**（255 checks）
- **Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Planning-v1-001**: **GO**（482/320 checks）
- **Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-DryRun-v1-001**: **GO**（401/360 checks；见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_DRYRUN_V1.md`）
- **Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Post-DryRun-Review-v1-001**: **GO**（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_POST_DRYRUN_REVIEW_V1.md`）
- **Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Closure-v1-001**: **GO**（333/260 checks）
