# Luna — Main Project Structure Migration B0 Preflight Via Harness v1

## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-B0-Preflight-Via-Harness-v1-001`
- **性质**: preflight-only（B0 作为 first consumer 的实际 preflight 检查层；不迁移、不 arming、不 file-op）
- **定位**: 使用已固化的 reusable Batch Preflight Harness contract，对 B0 `batch_config` 执行一次完整 preflight

## 输入（只读）

- `B0 Harness Adoption and Reusable Contract Closure`（GO）
- 必须存在：`reusable_batch_preflight_harness_contract_closure_v1.json`、`batch_config_template_v1.json`、`future_batch_usage_guide_v1.json`、`anti_recursion_rules_freeze_v1.json`

## 核心输出（20 类）

1. `b0_preflight_via_harness_policy_v1.json`
2. `reusable_harness_contract_input_review_v1.json`
3. `b0_batch_config_instance_v1.json`
4.–16. 各 fixed check result（scope / domain / protected / eval_out / fileop / manifest / rollback / rerun / post-tests / abort / workspace_fallback / non_claims）
17. `b0_preflight_migration_refactor_opportunity_scan_v1.json`
18. `b0_preflight_result_v1.json`
19. `b0_preflight_via_harness_readiness_decision_v1.json`
20. `summary.json` + `verifier_report.json`

## B0 batch_config 范围

- **batch_domain**: Documentation Index / README / phase table alignment
- **candidate_paths**（仅此三处）:
  - `docs/architecture/README.md`
  - `docs/architecture/evaluation/README.md`
  - `docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md`
- **allowed_operations**: move, rename
- **blocked_operations**: delete, overwrite, merge, copy

## 强制边界

- `b0_preflight_executed_now=true`（本阶段确实执行 preflight）
- `harness_contract_reused=true`
- `harness_extraction_reopened_now=false` / `harness_adoption_reopened_now=false`
- 禁止 B1–B7 重新进入 Harness Extraction / Adoption 链
- 所有 file-op / arming / execution / rerun / rollback rehearsal / post-migration tests = false

## Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_B0_PREFLIGHT_VIA_HARNESS_READY_FOR_CONTROLLED_EXECUTION`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-B0-Controlled-Execution-v1-001`
