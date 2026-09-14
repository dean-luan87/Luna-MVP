# Luna — Main Project Structure Migration Batch Preflight Harness Extraction DryRun v1

## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-DryRun-v1-001`
- **性质**: dry-run only（只模拟消费；不生成/不 enforce 正式 harness；不迁移/不 arming/不 file-op）
- **上游输入**:
  - `Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-Planning-v1-001`（verifier=GO）

## 目标

对 Harness 抽离规划做 dry-run，验证以下规划产物可被 B0–B7 消费：

- batch config schema
- harness interface
- output contract
- verifier baseline
- override policy
- B0–B7 adoption matrix
- repetitive phase deprecation register
- migration refactor opportunity scan rule（只输出候选与低风险计划；禁止迁移时重构 runtime）

## 强制边界（必须为 false / 不发生）

- 不生成正式 harness，不 enforce，不做 runtime 集成
- 不对真实 batch 应用 config，不执行迁移，不 arming
- 不做任何真实文件操作；不 rerun verifier；不执行 rollback rehearsal；不跑 post-migration tests

## 产物（15 类）

输出目录：

- `_eval_out/main_project_structure_migration_batch_preflight_harness_extraction_dryrun_v1_smoke_v0/`

产物文件：

1. `batch_preflight_harness_extraction_dryrun_policy_v1.json`
2. `batch_preflight_harness_extraction_planning_input_review_v1.json`
3. `reusable_preflight_check_inventory_dryrun_v1.json`
4. `batch_config_schema_consumption_dryrun_v1.json`
5. `batch_preflight_harness_interface_dryrun_v1.json`
6. `batch_preflight_output_contract_dryrun_v1.json`
7. `batch_preflight_verifier_baseline_dryrun_v1.json`
8. `batch_specific_override_policy_dryrun_v1.json`
9. `b0_to_b7_harness_adoption_dryrun_v1.json`
10. `deprecated_repetitive_phase_pattern_dryrun_v1.json`
11. `migration_refactor_opportunity_scan_rule_dryrun_v1.json`
12. `batch_preflight_harness_extraction_non_claims_dryrun_v1.json`
13. `batch_preflight_harness_extraction_dryrun_readiness_decision_v1.json`
14. `summary.json`
15. `verifier_report.json`

## Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-Post-DryRun-Review-v1-001`

