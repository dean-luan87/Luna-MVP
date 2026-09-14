## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Stabilized-Resume-Planning-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_stabilized_resume_planning_v1.py`
- **Status**: stabilized-resume-planning-only（工程整理主线恢复规划；非真实迁移）

## Intent

在 GC 分支收口与 Return-To-Registry wrapper 完成后，**重新接管 Luna-Core 主工程结构迁移整理主线**。

产品决策：

- **暂停** Governance Constraint Module 递归链（含 Artifact Generation Planning）
- **暂停** Registry Authorization 支线
- **优先** Main Project Structure Migration 稳定化与受控批次执行

本阶段确认：迁移目标结构不再大改、B0–B7 批次恢复矩阵、protected/forbidden 矩阵、test/verifier/rollback 要求、最短 7 步 future phase 模板（避免再开大型治理链）。

## Upstream

- `Phase-Return-To-Registry-Generation-Authorization-Planning-v1-001`（GO）
- `Phase-Governance-Constraint-Module-Branch-Closure-v1-001`（GO）
- Main Project Structure Migration 历史链（32 phase eval_out 全 GO）

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_RESUME_PLANNING_READY_FOR_EXECUTION_PLANNING`
- **Next**: `Phase-Main-Project-Structure-Migration-Stabilized-Execution-Planning-v1-001`

## Shortest Route (frozen)

1. Stabilized Resume Planning ✅
2. Stabilized Execution Planning（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_EXECUTION_PLANNING_V1.md`）
3. Stabilized Execution DryRun
4. Post-DryRun Review
5. Controlled Batch Execution Authorization
6. Controlled Batch Execution
7. Post-Migration Test + Verifier Closure

## Implementation Status

- **GO**（422/420 checks）
