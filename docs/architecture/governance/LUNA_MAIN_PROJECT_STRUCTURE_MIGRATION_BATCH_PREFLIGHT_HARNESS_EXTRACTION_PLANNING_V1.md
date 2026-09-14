# Luna — Main Project Structure Migration Batch Preflight Harness Extraction Planning v1

## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-Planning-v1-001`
- **性质**: planning only（只做抽离规划；不生成 harness、不执行 harness、不迁移、不 arming、不生成/发送 request）
- **目的**: 从既有 B0 / Controlled Batch Execution 授权与 arming 链中抽取同构的迁移前置验证逻辑，形成可复用的 **Batch Migration Preflight Harness** 合同与接口规划。

## 输入参考（仅消费已有产物；不修改）

- Controlled Batch Execution Authorization Post-DryRun Review（GO）
- Controlled Batch Execution Arming Post-DryRun Review（GO）
- B0 Arming Request Planning（GO）

## 核心输出（11 + summary/verifier）

1. `batch_preflight_harness_extraction_policy_v1.json`
2. `reusable_preflight_check_inventory_v1.json`
3. `batch_config_schema_planning_v1.json`
4. `batch_preflight_harness_interface_planning_v1.json`
5. `batch_preflight_output_contract_planning_v1.json`
6. `batch_preflight_verifier_baseline_planning_v1.json`
7. `batch_specific_override_policy_v1.json`
8. `b0_to_b7_harness_adoption_matrix_v1.json`
9. `deprecated_repetitive_phase_pattern_register_v1.json`
10. `batch_preflight_harness_extraction_readiness_decision_v1.json`
11. `summary.json`
12. `verifier_report.json`

## Batch Config 必须支持的字段（schema 规划）

- `batch_id`
- `batch_domain`
- `candidate_paths`
- `allowed_operations`
- `blocked_operations`
- `protected_path_policy`
- `eval_out_policy`
- `before_manifest_requirement`
- `after_manifest_requirement`
- `rollback_route`
- `verifier_rerun_list`
- `post_migration_test_list`
- `abort_conditions`
- `workspace_fallback_policy`
- `non_claims`

## Harness 固定检查（不可被 batch override）

- `scope_check`
- `domain_isolation_check`
- `protected_guard_check`
- `eval_out_readonly_check`
- `file_operation_boundary_check`
- `manifest_requirement_check`
- `rollback_requirement_check`
- `verifier_rerun_requirement_check`
- `post_migration_test_requirement_check`
- `abort_condition_check`
- `workspace_fallback_check`
- `non_claims_check`
- `migration_refactor_opportunity_scan_check`
- `readiness_decision`

## 边界（必须为 false / 不发生）

- `harness_generated_now=false`
- `harness_enforced_now=false`
- `batch_execution_started_now=false`
- `actual_file_*_executed=false`
- `verifier_rerun_executed_now=false`
- `rollback_rehearsal_executed_now=false`
- `post_migration_tests_executed_now=false`

## Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-DryRun-v1-001`

