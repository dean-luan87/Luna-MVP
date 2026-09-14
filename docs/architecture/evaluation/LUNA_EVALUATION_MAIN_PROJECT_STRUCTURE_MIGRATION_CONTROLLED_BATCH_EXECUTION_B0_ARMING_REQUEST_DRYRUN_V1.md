# Luna Evaluation — Main Project Structure Migration Controlled Batch Execution B0 Arming Request DryRun v1

## 目的

运行并验证：

`Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-B0-Arming-Request-DryRun-v1-001`

本阶段仅做 **B0 arming request dry-run**：只模拟消费 planning 产物；不生成 request artifact、不发送 request、不授权、不 arming、不打开 execution window、不执行文件操作、不 rerun verifier、不执行 rollback rehearsal、不跑 post-migration tests。

## 运行方式

### 1) 运行（生成 15 类产物）

默认（尝试写入仓库 `_eval_out`，若无权限请使用 `--output-root` 指向 workspace）：

```bash
python3 -m tools.evaluation.governance.run_main_project_structure_migration_controlled_batch_execution_b0_arming_request_dryrun_v1
```

workspace fallback 推荐命令（示例）：

```bash
python3 -m tools.evaluation.governance.run_main_project_structure_migration_controlled_batch_execution_b0_arming_request_dryrun_v1 \
  --output-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/b0_arming_request_dryrun" \
  --b0-arming-request-planning-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/b0_arming_request_planning"
```

### 2) 验证（verifier）

```bash
python3 -m tools.evaluation.governance.verify_main_project_structure_migration_controlled_batch_execution_b0_arming_request_dryrun_v1 \
  --output-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/b0_arming_request_dryrun" \
  --b0-arming-request-planning-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/b0_arming_request_planning"
```

## 预期输出

- `verifier=GO`
- `boundary_ok=true`
- `selected_batch_id=B0`、`b0_only=true`、`b1_b7_arming_deferred=true`
- request artifact 未生成、request 未发送、arming 未授权、B0 未 armed
- execution window 未打开
- 所有 `actual_file_*_executed=false`、`verifier_rerun_executed_now=false`、`rollback_rehearsal_executed_now=false`、`post_migration_tests_executed_now=false`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_B0_ARMING_REQUEST_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-B0-Arming-Request-Post-DryRun-Review-v1-001`

## workspace_fallback 约定

当输入 root 来自 workspace fallback（`source_path_mode=workspace_fallback`）时：

- `summary.json` 必须继续记录：
  - `source_path_mode=workspace_fallback`
  - `standard_eval_out_write_pending_on_local_repro=true`

该标记 **不** 等于标准仓库 `_eval_out` 已落盘。

