## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_real_rollback_rehearsal_pre_authorization_dryrun_v1.py`
- **Status**: pre-authorization-dryrun-only（模拟授权链评估；不授予真实授权、不执行真实演练）

## Intent

对 Pre-Authorization Planning 定义的授权链做 dry-run 模拟评估，覆盖：

- owner/operator 授权 requirement（8 项）逐项 dryrun evaluation
- execution window requirement（9 项）逐项 dryrun evaluation
- sandbox/branch、restore map、restore operation 边界的 simulated decision/evaluation
- verifier rerun / evidence generation 的 simulated evaluation（不得 subprocess / 不生成证据）
- success claim gate 必须保持 blocked

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **Next**: `Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Post-DryRun-Review-v1-001`

## Non-Claims

- Pre-Authorization DryRun GO ≠ authorization_granted_now=true
- Pre-Authorization DryRun GO ≠ owner/operator 已授权或窗口已打开
- Pre-Authorization DryRun GO ≠ sandbox/branch/restore map/verifier rerun/evidence 可执行
- Pre-Authorization DryRun GO ≠ 真实 rollback rehearsal 可执行/已成功

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Planning-v1-001**: **GO**（531/360 checks）
- **Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001**: **GO**（604/420 checks）
- **Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Post-DryRun-Review-v1-001**: **GO**（560/420 checks；见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_POST_DRYRUN_REVIEW_V1.md`）

