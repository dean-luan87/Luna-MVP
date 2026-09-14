# Luna Evaluation — GO / NO_GO Pack

## Phase

- `Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Authorization-DryRun-v1-001`

## GO 条件（必须全部满足）

### 上游读取

- 上游 `Controlled Batch Execution Authorization Planning` 必须：
  - `verifier=GO`
  - `boundary_ok=true`
  - `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN`
  - `recommended_next_phase=Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Authorization-DryRun-v1-001`
- 上游 17 类 planning 产物必须可读取

### 本阶段产物

- 17 类 dry-run 产物全部生成（含 `summary.json` / `verifier_report.json`）
- B0–B7 每个 batch `simulated_consumption=pass`
- request schema dry-run pass，且 `request_sent_now=false`
- grant schema dry-run pass，且 `authorized_now=false`
- precondition gate dry-run pass，且 **不** 释放 authorization
- execution window dry-run pass，且 `execution_window_opened_now=false`
- allowlist/blocklist dry-run pass，且所有 `actual_file_*_executed=false`
- verifier rerun plan dry-run pass，且 `verifier_rerun_executed_now=false`
- rollback requirement dry-run pass，且 `rollback_rehearsal_executed_now=false`
- post-migration test plan dry-run pass，且 `post_migration_tests_executed_now=false`
- abort condition dry-run pass
- protected/eval_out/HR/DnAE guard（以 summary 冻结字段为准）全部为 false

### 边界冻结（全部必须为 false）

- request / authorized / arming / execution 相关字段全部 false
- `eval_out_modified_now=false`
- `protected_asset_modified_now=false`
- `hr_modified_now=false`
- `dnae_modified_now=false`

### Non-Claims（防误读覆盖）

必须覆盖（至少包含以下语义）：

- Authorization DryRun GO ≠ execution authorization request sent
- request schema pass ≠ request sent
- grant schema pass ≠ execution authorized
- allowlist pass ≠ file operation executed
- verifier rerun plan pass ≠ verifier rerun executed
- rollback requirement pass ≠ rollback rehearsal executed
- post-migration test plan pass ≠ tests executed
- workspace_fallback GO ≠ standard `_eval_out` already written

### Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Authorization-Post-DryRun-Review-v1-001`
- `boundary_ok=true`

## NO_GO 条件（任一命中即 NO_GO）

- 任何真实 file operation 执行（move/delete/rename/merge/copy/overwrite/archive 任一为 true）
- request/grant/arming/execution 任一被置为 true
- verifier rerun / rollback rehearsal / post-migration tests 任一被执行
- 产物缺失或 B0–B7 trace 不完整
- 上游 planning 不是 GO 或被误读

