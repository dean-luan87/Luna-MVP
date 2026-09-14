## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-Planning-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_rollback_rehearsal_dryrun_planning_v1.py`
- **Status**: planning-only（定义 rollback rehearsal dry-run，不执行、不创建 sandbox/branch）

## Intent

在 Pre-Authorization Closure 与 Roadmap Decision（Route A）之后，定义未来 rollback rehearsal **dry-run** 如何模拟：

- **RehearsalSandboxPolicy**：专用 rehearsal 分支/沙箱策略（`sandbox_created_now=false`）
- **RollbackRehearsalDryRunScope**：B0 baseline + B1–B6 恢复路径 + B7 verification gate（8 批）
- **RollbackRestorePathMapPlan**：基于 `current_to_target_structure_map` 的反向恢复映射计划
- **DocsLinkRestorePlan** / **VerdictTableRestorePlan** / **EvalOutReferenceRestorePlan**
- **CapabilityRunnerVerifierDocLinkageRestorePlan**
- **RollbackVerifierRerunPlan**：≥12 verifier 顺序 + ≥4 rollback 专用 verifier
- **RollbackRehearsalEvidenceTemplate** / **RollbackSuccessClaimPolicy**（success claim 禁止）

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_DRYRUN_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-v1-001`

## Non-Claims

- Planning GO ≠ sandbox/branch 已创建
- Planning GO ≠ rollback rehearsal dry-run 已执行
- Planning GO ≠ rollback rehearsal 已执行 / evidence 已生成 / success 可声明
- DryRun 下一阶段仍不执行真实回滚，只模拟链路

## Implementation Status

- **Phase-Post-Pre-Authorization-and-Rollback-Rehearsal-Roadmap-Decision-v1-001**: **GO**（293/220 checks）
- **Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-Planning-v1-001**: **GO**（389/340 checks）
- **Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-v1-001**: **GO**（456/380 checks）
- **Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Post-DryRun-Review-v1-001**: **GO**（364/360 checks）
- **Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Closure-v1-001**: **GO**（276/260 checks）
- **Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Roadmap-Decision-v1-001**: pending
