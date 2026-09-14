# Luna — Main Project Structure Migration Controlled Batch Execution Arming Planning v1

## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Arming-Planning-v1-001`
- **性质**: arming planning only（只做 arming 规划，不 arming，不执行）
- **收窄策略**: **仅规划 B0 单批次**；B1–B7 明确 deferred
- **上游输入**:
  - `Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Authorization-Post-DryRun-Review-v1-001`（verifier=GO）

## 目标

在上一阶段 post-dryrun review 已通过的前提下，冻结 **B0** 的 arming planning 对象（窗口、allow/block、manifest、rollback、verifier rerun、post tests、abort、guard、non-claims），同时把 B1–B7 全量 arming 明确延期，避免一次性放大风险面。

## 强制边界（必须为 false / 不发生）

- 不 arming（`batch_armed_now=false`），不执行 batch（`batch_execution_started_now=false`）
- 不打开执行窗口（`execution_window_opened_now=false`）
- 不进行真实文件操作（move/delete/rename/merge/copy/overwrite/archive）
- 不 rerun verifier
- 不执行 rollback rehearsal
- 不执行 post-migration tests
- 不修改 `_eval_out`、不触碰 protected / HR / DnAE

## 产物（17 类）

输出目录：

- `_eval_out/main_project_structure_migration_controlled_batch_execution_arming_planning_v1_smoke_v0/`

产物文件：

1. `controlled_batch_execution_arming_planning_policy_v1.json`
2. `controlled_execution_authorization_post_review_input_review_v1.json`
3. `b0_single_batch_arming_scope_v1.json`
4. `b1_b7_deferred_arming_matrix_v1.json`
5. `b0_execution_window_arming_plan_v1.json`
6. `b0_file_operation_allowlist_arming_plan_v1.json`
7. `b0_file_operation_blocklist_arming_plan_v1.json`
8. `b0_before_after_manifest_arming_plan_v1.json`
9. `b0_rollback_route_arming_plan_v1.json`
10. `b0_verifier_rerun_arming_plan_v1.json`
11. `b0_post_migration_test_arming_plan_v1.json`
12. `b0_abort_condition_arming_plan_v1.json`
13. `b0_protected_eval_out_guard_arming_plan_v1.json`
14. `controlled_batch_execution_arming_non_claims_register_v1.json`
15. `controlled_batch_execution_arming_planning_readiness_decision_v1.json`
16. `summary.json`
17. `verifier_report.json`

## B0 Scope（必须收敛）

- `batch_id=B0`
- `batch_domain=Documentation Index / README / phase table alignment`
- `controlled_execution_scope_candidate` 只允许包含 docs 索引/README/phase table alignment 候选
- 不得包含 `capabilities/`、runner/verifier、configs/scripts/tests、protected/HR/DnAE、`_eval_out`
- `b0_arming_allowed_later=true`，且 `b0_armed_now=false`

## B1–B7

- 全部 `deferred=true`
- 全部 `arming_allowed_now=false`
- 全部 `batch_armed_now=false`
- 全部 `batch_execution_started_now=false`

## Final Decision

- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_ARMING_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Arming-DryRun-v1-001`

## Non-Claims（明确不等于什么）

- Arming Planning GO ≠ B0 armed
- B0 selected ≠ B0 executed
- B0 arming plan ≠ file operation executed
- B1–B7 deferred ≠ B1–B7 ready
- verifier rerun plan ≠ verifier rerun executed
- rollback route plan ≠ rollback rehearsal executed
- post-migration test plan ≠ tests executed
- workspace_fallback GO ≠ standard `_eval_out` already written

