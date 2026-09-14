# Luna Evaluation — GO / NO_GO Pack

## Phase

- `Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-Planning-v1-001`

## GO 条件（必须全部满足）

### 上游读取（参考链必须为 GO）

- Controlled Batch Execution Authorization Post-DryRun Review：
  - `verifier=GO`
  - `boundary_ok=true`
  - `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_AUTHORIZATION_POST_DRYRUN_REVIEW_READY_FOR_CONTROLLED_BATCH_EXECUTION_ARMING_PLANNING`
- Controlled Batch Execution Arming Post-DryRun Review：
  - `verifier=GO`
  - `boundary_ok=true`
  - `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_ARMING_POST_DRYRUN_REVIEW_READY_FOR_B0_ARMING_REQUEST_PLANNING`
- B0 Arming Request Planning：
  - `verifier=GO`
  - `boundary_ok=true`
  - `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_B0_ARMING_REQUEST_PLANNING_READY_FOR_DRYRUN`

### 本阶段产物（12 类）

- 11 个规划产物 + `summary.json` + `verifier_report.json` 全部生成
- `reusable_preflight_check_inventory_v1.json` 覆盖固定检查清单（含 `workspace_fallback_check` / `non_claims_check` / `readiness_decision`）
- 固定检查清单必须包含 `migration_refactor_opportunity_scan_check`（仅输出候选清单与低风险计划；禁止迁移时 runtime 重构）
- `batch_config_schema_planning_v1.json` 含全部 batch config 必填字段：
  - `batch_id/batch_domain/candidate_paths/allowed_operations/blocked_operations/protected_path_policy/eval_out_policy/before_manifest_requirement/after_manifest_requirement/rollback_route/verifier_rerun_list/post_migration_test_list/abort_conditions/workspace_fallback_policy/non_claims`
- `b0_to_b7_harness_adoption_matrix_v1.json` 覆盖 B0–B7 且 `adopt_harness=true`
- `deprecated_repetitive_phase_pattern_register_v1.json` 登记重复 phase pattern 的弃用策略

### 边界

- `harness_generated_now=false`
- `harness_enforced_now=false`
- `batch_armed_now=false`
- `batch_execution_started_now=false`
- `actual_file_*_executed=false`
- `verifier_rerun_executed_now=false`
- `rollback_rehearsal_executed_now=false`
- `post_migration_tests_executed_now=false`

### Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-DryRun-v1-001`

## NO_GO 条件（任一命中即 NO_GO）

- 上游任一不是 GO
- schema 缺字段或固定检查清单缺项
- 出现 `harness_generated_now=true` / `harness_enforced_now=true` 或任何真实执行/文件操作/复跑/演练/测试字段为 true
- final_decision / next phase 不匹配

