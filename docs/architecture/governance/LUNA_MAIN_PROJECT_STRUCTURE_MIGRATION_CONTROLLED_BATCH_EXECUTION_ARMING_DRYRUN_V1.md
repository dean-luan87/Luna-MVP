# Luna — Main Project Structure Migration Controlled Batch Execution Arming DryRun v1

## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Arming-DryRun-v1-001`
- **性质**: dry-run only（只模拟消费，不真实 arming / 不执行）
- **收窄策略**: **仅 B0**；B1–B7 保持 deferred
- **上游输入**:
  - `Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Arming-Planning-v1-001`（verifier=GO）

## 目标

对 B0 单批次 arming planning 的结构做 dry-run 消费模拟，确认：

- B0 scope/window/allowlist/blocklist/manifest/rollback/rerun/tests/abort/guard/non-claims 可消费
- 仍然不发生真实 arming、不打开窗口、不执行文件操作、不复跑 verifier、不执行 rollback rehearsal、不跑 post-migration tests
- workspace_fallback 不被误读为标准 `_eval_out` 已落盘

## 强制边界（必须为 false / 不发生）

- `b0_armed_now=false`、`batch_armed_now=false`
- `execution_window_opened_now=false`
- 所有 `actual_file_*_executed=false`
- `verifier_rerun_executed_now=false`
- `rollback_rehearsal_executed_now=false`
- `post_migration_tests_executed_now=false`
- `_eval_out` / protected / HR / DnAE 不修改

## 产物（17 类）

输出目录：

- `_eval_out/main_project_structure_migration_controlled_batch_execution_arming_dryrun_v1_smoke_v0/`

产物文件：

1. `controlled_batch_execution_arming_dryrun_policy_v1.json`
2. `controlled_batch_execution_arming_planning_input_review_v1.json`
3. `b0_single_batch_arming_scope_dryrun_v1.json`
4. `b1_b7_deferred_arming_dryrun_v1.json`
5. `b0_execution_window_arming_dryrun_v1.json`
6. `b0_file_operation_allowlist_arming_dryrun_v1.json`
7. `b0_file_operation_blocklist_arming_dryrun_v1.json`
8. `b0_before_after_manifest_arming_dryrun_v1.json`
9. `b0_rollback_route_arming_dryrun_v1.json`
10. `b0_verifier_rerun_arming_dryrun_v1.json`
11. `b0_post_migration_test_arming_dryrun_v1.json`
12. `b0_abort_condition_arming_dryrun_v1.json`
13. `b0_protected_eval_out_guard_arming_dryrun_v1.json`
14. `controlled_batch_execution_arming_non_claims_dryrun_v1.json`
15. `controlled_batch_execution_arming_dryrun_readiness_decision_v1.json`
16. `summary.json`
17. `verifier_report.json`

## Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_ARMING_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Arming-Post-DryRun-Review-v1-001`

## Non-Claims（明确不等于什么）

- Arming DryRun GO ≠ B0 armed
- B0 selected ≠ B0 executed
- B0 arming scope pass ≠ file operation executed
- B1–B7 deferred ≠ B1–B7 ready
- execution window pass ≠ execution window opened
- verifier rerun plan pass ≠ verifier rerun executed
- rollback route pass ≠ rollback rehearsal executed
- post-migration test plan pass ≠ tests executed
- workspace_fallback GO ≠ standard `_eval_out` already written

