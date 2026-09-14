## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Planning-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_real_rollback_rehearsal_pre_authorization_planning_v1.py`
- **Status**: pre-authorization-planning-only（真实演练前的预授权规划；不授予授权、不执行）

## Intent

将上游 Roadmap Decision 选中的 Route A 展开为 “真实 rollback rehearsal 前的授权规划”：

- owner/operator 授权要求（只定义 requirement，不标记已完成）
- execution window 授权规划（只定义窗口条件，不打开窗口）
- sandbox/branch 准备授权规划（只给 candidate name，不创建）
- restore map / restore operation 授权边界规划（不生成、不执行）
- verifier rerun / evidence generation 授权规划（不 rerun、不生成证据）
- success claim gate 继续保持 blocked

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001`

## Non-Claims

- Pre-Authorization Planning GO ≠ owner/operator 已授权
- Pre-Authorization Planning GO ≠ execution window 已打开
- Pre-Authorization Planning GO ≠ sandbox/branch 可创建
- Pre-Authorization Planning GO ≠ restore map 可生成 / restore operation 可执行
- Pre-Authorization Planning GO ≠ verifier 可 rerun / evidence 可生成
- Pre-Authorization Planning GO ≠ rollback success 可声明
- Pre-Authorization Planning GO ≠ 真实 rehearsal / 真实迁移 / batch arming 可执行

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Roadmap-Decision-v1-001**: **GO**（356/260 checks）
- **Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Planning-v1-001**: **GO**（531/360 checks）
- **Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001**: **GO**（604/420 checks；见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_DRYRUN_V1.md`）

