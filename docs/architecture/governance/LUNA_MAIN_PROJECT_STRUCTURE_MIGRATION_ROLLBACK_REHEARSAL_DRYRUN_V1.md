## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_rollback_rehearsal_dryrun_v1.py`
- **Status**: dry-run-only（模拟 rollback rehearsal 链路，不执行、不创建 sandbox/branch）

## Intent

对 Rollback Rehearsal DryRun Planning 进行 dry-run，模拟：

- RehearsalSandbox（`sandbox_simulated=true`，`sandbox_created_now=false`）
- B0–B7 rollback scope 与 B1–B6 restore path
- restore path map / docs / verdict / eval_out / linkage
- verifier rerun（`verifier_rerun_simulated=true`，`verifier_rerun_executed_now=false`）
- evidence（`evidence_simulated=true`，`evidence_generated_now=false`）
- success claim 阻断（`dryrun_success_claim_attempt_blocked=true`）

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **Next**: `Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Post-DryRun-Review-v1-001`

## Non-Claims

- DryRun GO ≠ sandbox/branch 已创建
- DryRun GO ≠ rollback rehearsal 已执行 / evidence 已生成 / success 可声明
- DryRun GO ≠ verifier rerun 已执行

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-Planning-v1-001**: **GO**（389/340 checks）
- **Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-v1-001**: **GO**（456/380 checks）
- **Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Post-DryRun-Review-v1-001**: **GO**（364/360 checks）
- **Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Closure-v1-001**: **GO**（276/260 checks）
- **Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Roadmap-Decision-v1-001**: pending
