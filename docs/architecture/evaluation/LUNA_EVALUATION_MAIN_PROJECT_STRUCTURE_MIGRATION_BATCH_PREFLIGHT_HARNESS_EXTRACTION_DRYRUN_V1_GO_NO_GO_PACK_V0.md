# Luna Evaluation — GO / NO_GO Pack

## Phase

- `Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-DryRun-v1-001`

## GO 条件（必须全部满足）

### 上游读取（Extraction Planning）

- 上游必须：
  - `verifier=GO`
  - `boundary_ok=true`
  - `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_PLANNING_READY_FOR_DRYRUN`
  - `recommended_next_phase=Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-DryRun-v1-001`
  - `batch_preflight_harness_extraction_planning_only=true`
  - `harness_generated_now=false`
  - `harness_enforced_now=false`
  - `batch_armed_now=false`
  - all `actual_file_*_executed=false`

### 本阶段产物（15 类）

- 15 类 dry-run 产物全部生成（含 `summary.json` / `verifier_report.json`）
- `reusable_preflight_check_inventory_dryrun_v1.json` dry-run pass，且最少覆盖：
  - `scope_check/domain_isolation_check/protected_guard_check/eval_out_readonly_check/file_operation_boundary_check/manifest_requirement_check/rollback_requirement_check/verifier_rerun_requirement_check/post_migration_test_requirement_check/abort_condition_check/workspace_fallback_check/non_claims_check/readiness_decision`
- `batch_config_schema_consumption_dryrun_v1.json` dry-run pass，字段覆盖不少于 15 项（至少覆盖 schema 最小集合）
- `batch_preflight_harness_interface_dryrun_v1.json` dry-run pass，且 `harness_generated_now=false`
- `batch_preflight_output_contract_dryrun_v1.json` dry-run pass，且声明未来 batch 至少输出：
  - `batch_config/preflight_result/migration_refactor_opportunity_scan/extract_now_allowed/extract_later_candidates/blocked_refactor_items/final_batch_readiness_decision`
- `batch_specific_override_policy_dryrun_v1.json` dry-run pass，且 override 不得绕过 protected/eval_out/domain/file-op/no-runtime-modification
- `b0_to_b7_harness_adoption_dryrun_v1.json` 覆盖 B0–B7，且：
  - B0 为 first adoption candidate
  - B1–B7 deferred until B0 harness validation
  - `execution_allowed_now=false`
- `deprecated_repetitive_phase_pattern_dryrun_v1.json` dry-run pass
- `migration_refactor_opportunity_scan_rule_dryrun_v1.json` dry-run pass，且 A/B/C 风险分级齐备、`blocked_from_runtime_refactor_now=true`
- `batch_preflight_harness_extraction_non_claims_dryrun_v1.json` 覆盖 required non-claims

### 边界

- `batch_preflight_harness_extraction_dryrun_only=true`
- `simulated=true`
- `harness_generated_now=false`
- `harness_enforced_now=false`
- `harness_runtime_integrated_now=false`
- `batch_config_applied_to_real_batch_now=false`
- `batch_execution_started_now=false`
- `batch_armed_now=false`
- all `actual_file_*_executed=false`
- `verifier_rerun_executed_now=false`
- `rollback_rehearsal_executed_now=false`
- `post_migration_tests_executed_now=false`

### Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-Post-DryRun-Review-v1-001`

## NO_GO 条件（任一命中即 NO_GO）

- 上游不是 GO 或 final_decision/next_phase 不匹配
- 产物缺失或 dry-run pass=false
- 出现 harness 生成/生效/runtime 集成/真实 batch 应用/arming/执行/文件操作/复跑/演练/测试任一字段为 true

