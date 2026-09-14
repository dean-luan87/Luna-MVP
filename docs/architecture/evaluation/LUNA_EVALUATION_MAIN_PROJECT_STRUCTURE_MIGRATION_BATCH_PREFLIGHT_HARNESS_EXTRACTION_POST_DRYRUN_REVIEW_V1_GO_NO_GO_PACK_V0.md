# Luna Evaluation — GO / NO_GO Pack

## Phase

- `Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-Post-DryRun-Review-v1-001`

## GO 条件（必须全部满足）

### 上游读取（Extraction DryRun）

- 上游必须：
  - `verifier=GO`
  - `boundary_ok=true`
  - `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
  - `recommended_next_phase=Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-Post-DryRun-Review-v1-001`
  - `batch_preflight_harness_extraction_dryrun_only=true`
  - `simulated=true`
  - `harness_generated_now=false`
  - `harness_enforced_now=false`
  - `harness_runtime_integrated_now=false`
  - `batch_config_applied_to_real_batch_now=false`
  - `batch_armed_now=false`
  - `batch_execution_started_now=false`
  - all `actual_file_*_executed=false`

### 本阶段产物（16 类）

- 16 类 review 产物全部生成（含 `summary.json` / `verifier_report.json`）
- `reusable_preflight_check_inventory_review_v1.json` review pass，并确认固定检查覆盖要求（含 `migration_refactor_opportunity_scan_check`）
- `batch_config_schema_consumption_review_v1.json` review pass，字段覆盖不少于 15 项
- `batch_preflight_harness_interface_review_v1.json` review pass，并确认：
  - `harness_generated_now=false`
  - `harness_registered_now=false`
  - `harness_enforced_now=false`
  - `harness_runtime_integrated_now=false`
- `batch_preflight_output_contract_review_v1.json` review pass，并确认未来 batch 输出至少包含：
  - `batch_config/preflight_result/migration_refactor_opportunity_scan/extract_now_allowed/extract_later_candidates/blocked_refactor_items/final_batch_readiness_decision`
- `batch_preflight_verifier_baseline_review_v1.json` review pass，并确认：
  - `verifier_modified_now=false`
  - `must_assert_blocked_from_runtime_refactor_now=true`
- `batch_specific_override_policy_review_v1.json` review pass，且不能绕过 protected/eval_out/domain/file-op/runtime-refactor/workspace_fallback guard
- `b0_to_b7_harness_adoption_review_v1.json` review pass，且 B0 first candidate、B1–B7 deferred、`execution_allowed_now=false`
- `deprecated_repetitive_phase_pattern_review_v1.json` review pass，且 old phase 未删除/未 deprecated、旧 eval_out/旧 verifier_report 未改写
- `migration_refactor_opportunity_scan_rule_review_v1.json` review pass，且 A/B/C 分级成立、`blocked_from_runtime_refactor_now=true`、`runtime_refactor_executed_now=false`
- `batch_preflight_harness_non_generation_review_v1.json` review pass（formal harness 未生成、未 enforce、未集成、未应用 batch_config、未 file-op）
- `batch_preflight_harness_extraction_non_claims_review_v1.json` 覆盖 required non-claims

### Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_POST_DRYRUN_REVIEW_READY_FOR_B0_HARNESS_ADOPTION_PLANNING`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-Planning-v1-001`

## NO_GO 条件（任一命中即 NO_GO）

- 上游不是 GO 或 final_decision/next_phase 不匹配
- review 产物缺失或任一 review pass=false
- 出现 harness 生成/注册/生效/runtime 集成/真实 batch 应用/arming/执行/文件操作/复跑/演练/测试任一字段为 true
- 出现 runtime_refactor_executed_now=true、old_phase_deleted_now=true、verifier_modified_now=true、phase_template_modified_now=true

