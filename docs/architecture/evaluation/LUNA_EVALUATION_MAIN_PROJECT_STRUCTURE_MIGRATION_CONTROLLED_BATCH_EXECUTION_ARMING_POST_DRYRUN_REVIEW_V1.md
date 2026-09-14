# Luna Evaluation — Main Project Structure Migration Controlled Batch Execution Arming Post-DryRun Review v1

## 目的

运行并验证：

`Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Arming-Post-DryRun-Review-v1-001`

本阶段 **review-only**：只审查 B0-only arming dry-run 是否可信，不 arming、不打开窗口、不执行文件操作、不 rerun verifier、不执行 rollback rehearsal、不跑 post-migration tests。

## 运行方式

### 1) 运行（生成 16 类 review 产物）

默认（尝试写入仓库 `_eval_out`，若无权限请使用 `--output-root` 指向 workspace）：

```bash
python3 -m tools.evaluation.governance.run_main_project_structure_migration_controlled_batch_execution_arming_post_dryrun_review_v1
```

workspace fallback 推荐命令（示例）：

```bash
python3 -m tools.evaluation.governance.run_main_project_structure_migration_controlled_batch_execution_arming_post_dryrun_review_v1 \
  --output-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_batch_exec_arming_post_review" \
  --controlled-batch-execution-arming-dryrun-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_batch_exec_arming_dryrun"
```

### 2) 验证（verifier）

```bash
python3 -m tools.evaluation.governance.verify_main_project_structure_migration_controlled_batch_execution_arming_post_dryrun_review_v1 \
  --output-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_batch_exec_arming_post_review" \
  --controlled-batch-execution-arming-dryrun-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_batch_exec_arming_dryrun"
```

## 预期输出

- `verifier=GO`
- `selected_batch_id=B0`、`b0_only=true`、`b1_b7_arming_deferred=true`
- 未发生 arming/window/file-op/rerun/rollback/tests（全部字段 false）
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_ARMING_POST_DRYRUN_REVIEW_READY_FOR_B0_ARMING_REQUEST_PLANNING`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-B0-Arming-Request-Planning-v1-001`

## workspace_fallback 约定

当输入 root 来自 workspace fallback（`source_path_mode=workspace_fallback`）时：

- `summary.json` 必须继续记录：
  - `source_path_mode=workspace_fallback`
  - `standard_eval_out_write_pending_on_local_repro=true`

该标记 **不** 等于标准仓库 `_eval_out` 已落盘。

