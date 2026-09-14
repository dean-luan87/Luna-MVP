# Luna Evaluation — GO / NO_GO Pack

## Phase

- `Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-Planning-v1-001`

## GO 条件（必须全部满足）

### 上游读取（Harness Extraction Post-DryRun Review）

- 上游必须：
  - `verifier=GO`
  - `boundary_ok=true`
  - `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_POST_DRYRUN_REVIEW_READY_FOR_B0_HARNESS_ADOPTION_PLANNING`
  - `recommended_next_phase=Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-Planning-v1-001`
  - `harness_generated_now=false`、`harness_registered_now=false`、`harness_enforced_now=false`、`harness_runtime_integrated_now=false`
  - `batch_config_applied_to_real_batch_now=false`
  - `old_phase_deleted_now=false`、`old_phase_deprecated_now=false`
  - `runtime_refactor_executed_now=false`

### 本阶段产物（18 类）

- 18 类 planning 产物全部生成（含 `summary.json` / `verifier_report.json`）
- `selected_batch_id=B0`、`b0_only=true`、`b1_b7_harness_adoption_deferred=true`
- B0 batch_config planning 覆盖字段集合（至少 15 项 + non_claims）
- B0 scope 不包含 `capabilities/runner/verifier/configs/scripts/tests/protected/HR/DnAE/_eval_out`
- B0 harness check binding 覆盖固定检查项（含 `migration_refactor_opportunity_scan_check`）
- Migration Refactor Opportunity Scan planning：`extract_now_allowed=false` 且 runtime 类条目在 `blocked_refactor_items`
- B1–B7：`adoption_deferred=true`、`preflight_allowed_now=false`、`execution_allowed_now=false`、`batch_armed_now=false`
- 边界字段：harness 未生成/未 enforce/未集成，B0 preflight 未执行，未 arming，未开窗，未 file-op

### Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-DryRun-v1-001`

## NO_GO 条件（任一命中即 NO_GO）

- 上游不是 GO 或 final_decision/next_phase 不匹配
- scope 越界（出现 forbidden tokens）或包含 B1–B7
- 出现 harness 生成/生效/runtime 集成，或 B0 batch_config 应用于真实 batch，或任何 file-op/arming/window/execution 被执行

