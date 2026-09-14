# Luna Evaluation — GO / NO_GO Pack

## Phase

- `Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Arming-DryRun-v1-001`

## GO 条件（必须全部满足）

### 上游读取（Arming Planning）

- 上游必须：
  - `verifier=GO`
  - `boundary_ok=true`
  - `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_ARMING_PLANNING_READY_FOR_DRYRUN`
  - `recommended_next_phase=Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Arming-DryRun-v1-001`
  - `selected_batch_id=B0`
  - `b0_only=true`
  - `b1_b7_arming_deferred=true`
  - arming/execution/file-op/rerun/rollback/tests 全部 false

### 本阶段产物

- 17 类 arming dry-run 产物全部生成（含 `summary.json` / `verifier_report.json`）
- `selected_batch_id=B0`、`b0_only=true`、`b1_b7_arming_deferred=true`
- B0 arming scope dry-run `simulated_consumption=pass`
- B0 scope 不包含 forbidden 域：`capabilities/runner/verifier/configs/scripts/tests/protected/HR/DnAE/_eval_out`
- B1–B7 dry-run 中保持 deferred 且不释放 arming/execute
- execution window dry-run pass，但 `execution_window_opened_now=false`
- allowlist/blocklist/manifest/rollback/rerun/tests/abort/guard/non-claims dry-run pass
- `b0_armed_now=false`、`batch_armed_now=false`、`batch_execution_started_now=false`
- 所有 `actual_file_*_executed=false`
- `verifier_rerun_executed_now=false`
- `rollback_rehearsal_executed_now=false`
- `post_migration_tests_executed_now=false`

### Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_ARMING_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Arming-Post-DryRun-Review-v1-001`
- `boundary_ok=true`

## NO_GO 条件（任一命中即 NO_GO）

- 任何真实 arming/window/file-op/rerun/rollback/tests 被执行（任一字段 true）
- B0 scope 触及 forbidden 域
- B1–B7 deferred 语义被破坏
- 产物缺失或 final decision / next phase 不匹配

