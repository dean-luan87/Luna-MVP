# Luna Evaluation — GO / NO_GO Pack

## Phase

- `Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-B0-Arming-Request-Planning-v1-001`

## GO 条件（必须全部满足）

### 上游读取（Arming Post-DryRun Review）

- 上游必须：
  - `verifier=GO`
  - `boundary_ok=true`
  - `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_ARMING_POST_DRYRUN_REVIEW_READY_FOR_B0_ARMING_REQUEST_PLANNING`
  - `recommended_next_phase=Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-B0-Arming-Request-Planning-v1-001`
  - `selected_batch_id=B0`
  - `b0_only=true`
  - `b1_b7_arming_deferred=true`
  - arming/execution/file-op/rerun/rollback/tests 全部 false

### 本阶段产物

- 15 类 request planning 产物全部生成（含 `summary.json` / `verifier_report.json`）
- `selected_batch_id=B0`、`b0_only=true`、`b1_b7_arming_deferred=true`
- B0 request scope 不越界：不包含 `capabilities/runner/verifier/configs/scripts/tests/protected/HR/DnAE/_eval_out`
- `b0_arming_request_artifact_generated_now=false`
- `b0_arming_request_sent_now=false`
- `b0_arming_authorized_now=false`
- `b0_armed_now=false`
- `execution_window_opened_now=false`
- all `actual_file_*_executed=false`
- `verifier_rerun_executed_now=false`
- `rollback_rehearsal_executed_now=false`
- `post_migration_tests_executed_now=false`

### Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_B0_ARMING_REQUEST_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-B0-Arming-Request-DryRun-v1-001`
- `boundary_ok=true`

## NO_GO 条件（任一命中即 NO_GO）

- scope 越界或包含 B1–B7
- request artifact / request sent / authorized / arming / window / file-op / rerun / rollback / tests 任一被执行（字段 true）
- final decision / next phase 不匹配

