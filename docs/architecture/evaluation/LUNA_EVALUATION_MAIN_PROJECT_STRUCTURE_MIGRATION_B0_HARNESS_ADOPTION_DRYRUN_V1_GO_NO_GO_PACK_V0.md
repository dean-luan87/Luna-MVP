# Luna Evaluation — GO / NO_GO Pack

## Phase

- `Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-DryRun-v1-001`

## GO 条件（必须全部满足）

### 上游读取（B0 Harness Adoption Planning）

- 上游必须：
  - `verifier=GO`
  - `boundary_ok=true`
  - `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_PLANNING_READY_FOR_DRYRUN`
  - `recommended_next_phase=Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-DryRun-v1-001`
  - `selected_batch_id=B0`
  - `b0_only=true`
  - `b1_b7_harness_adoption_deferred=true`
  - 所有执行/arming/file-op/rerun/rollback/tests/runtime_refactor 等字段为 false

### 本阶段产物（18 类）

- 18 类 dry-run 产物全部生成（含 `summary.json` / `verifier_report.json`）
- `b0_batch_config_consumption_dryrun_v1.json` pass，且 candidate_paths/ops/readonly/non_claims 覆盖要求
- `b0_scope_and_domain_isolation_dryrun_v1.json` pass，且不包含 forbidden scopes
- `b0_harness_preflight_check_binding_dryrun_v1.json` pass，且覆盖固定 checks（含 `migration_refactor_opportunity_scan_check`）
- `b0_migration_refactor_opportunity_scan_dryrun_v1.json` pass：
  - `extract_now_allowed=false`
  - `runtime_refactor_executed_now=false`
  - `blocked_from_runtime_refactor_now=true`
  - C 类 runtime/core behavior 被 blocked
- `b1_b7_harness_adoption_deferred_dryrun_v1.json` pass：全部 deferred 且 preflight/execution/armed 为 false

### Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-Post-DryRun-Review-v1-001`

## NO_GO 条件（任一命中即 NO_GO）

- 上游不是 GO 或 final_decision/next_phase 不匹配
- 出现 harness 生成/生效/runtime 集成，或 batch_config 应用到真实 batch，或 preflight/arming/执行/file-op/复跑/演练/测试 任一字段为 true
- B0 candidate_paths / operations 不满足约束或 scope 越界

