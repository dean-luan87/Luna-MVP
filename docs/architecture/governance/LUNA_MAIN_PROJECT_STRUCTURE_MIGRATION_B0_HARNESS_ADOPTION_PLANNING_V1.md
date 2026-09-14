# Luna — Main Project Structure Migration B0 Harness Adoption Planning v1

## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-Planning-v1-001`
- **性质**: planning-only（只规划 B0 如何使用统一 Batch Preflight Harness；不生成/不 enforce 正式 harness；不执行迁移/arming/preflight）
- **上游输入**:
  - `Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-Post-DryRun-Review-v1-001`（verifier=GO）

## 目标

将 **B0** 作为第一个 adoption candidate，规划它如何通过统一 `Batch Preflight Harness` 跑迁移前检查：

- 产出 B0 `batch_config` 规划（docs index / README / phase table alignment only）
- 绑定固定 preflight checks（含 refactor opportunity scan check）
- 冻结 B1–B7 adoption（仅 deferred，不可 preflight/execution/arming）

## 产物（18 类）

输出目录：

- `_eval_out/main_project_structure_migration_b0_harness_adoption_planning_v1_smoke_v0/`

产物文件：

1. `b0_harness_adoption_planning_policy_v1.json`
2. `batch_preflight_harness_post_review_input_review_v1.json`
3. `b0_batch_config_planning_v1.json`
4. `b0_harness_preflight_check_binding_v1.json`
5. `b0_scope_and_domain_isolation_planning_v1.json`
6. `b0_protected_eval_out_guard_planning_v1.json`
7. `b0_file_operation_boundary_planning_v1.json`
8. `b0_manifest_requirement_planning_v1.json`
9. `b0_rollback_requirement_planning_v1.json`
10. `b0_verifier_rerun_requirement_planning_v1.json`
11. `b0_post_migration_test_requirement_planning_v1.json`
12. `b0_abort_condition_planning_v1.json`
13. `b0_migration_refactor_opportunity_scan_planning_v1.json`
14. `b1_b7_harness_adoption_deferred_matrix_v1.json`
15. `b0_harness_adoption_non_claims_register_v1.json`
16. `b0_harness_adoption_planning_readiness_decision_v1.json`
17. `summary.json`
18. `verifier_report.json`

## 强制边界（必须为 false / 不发生）

- 不生成/不注册/不 enforce harness，不做 runtime integration
- 不生成/不应用真实 batch_config，不执行 preflight
- 不 arming，不开 execution window，不执行迁移，不做 file-op
- 不 rerun verifier，不执行 rollback rehearsal，不跑 post-migration tests
- 不做 runtime refactor，不删除/不自动 deprecated 旧 phase

## Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-DryRun-v1-001`

