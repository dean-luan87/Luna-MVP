# Luna — Main Project Structure Migration B0 Harness Adoption DryRun v1

## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-DryRun-v1-001`
- **性质**: dry-run only（只模拟消费；不生成/不 enforce 正式 harness；不执行 preflight；不迁移/不 arming/不 file-op）
- **上游输入**:
  - `Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-Planning-v1-001`（verifier=GO）

## 目标

对 B0 Harness Adoption Planning 做 dry-run，验证 B0 `batch_config` 与检查绑定等是否可被统一 Batch Preflight Harness 结构消费：

- batch_config consumption
- check binding
- scope/domain isolation
- protected/eval_out guard
- file operation boundary
- manifest/rollback/verifier rerun/post-test/abort requirement
- migration refactor opportunity scan（只输出候选；禁止 runtime refactor）
- B1–B7 deferred semantics

## 产物（18 类）

输出目录：

- `_eval_out/main_project_structure_migration_b0_harness_adoption_dryrun_v1_smoke_v0/`

产物文件：

1. `b0_harness_adoption_dryrun_policy_v1.json`
2. `b0_harness_adoption_planning_input_review_v1.json`
3. `b0_batch_config_consumption_dryrun_v1.json`
4. `b0_harness_preflight_check_binding_dryrun_v1.json`
5. `b0_scope_and_domain_isolation_dryrun_v1.json`
6. `b0_protected_eval_out_guard_dryrun_v1.json`
7. `b0_file_operation_boundary_dryrun_v1.json`
8. `b0_manifest_requirement_dryrun_v1.json`
9. `b0_rollback_requirement_dryrun_v1.json`
10. `b0_verifier_rerun_requirement_dryrun_v1.json`
11. `b0_post_migration_test_requirement_dryrun_v1.json`
12. `b0_abort_condition_dryrun_v1.json`
13. `b0_migration_refactor_opportunity_scan_dryrun_v1.json`
14. `b1_b7_harness_adoption_deferred_dryrun_v1.json`
15. `b0_harness_adoption_non_claims_dryrun_v1.json`
16. `b0_harness_adoption_dryrun_readiness_decision_v1.json`
17. `summary.json`
18. `verifier_report.json`

## Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-Post-DryRun-Review-v1-001`

