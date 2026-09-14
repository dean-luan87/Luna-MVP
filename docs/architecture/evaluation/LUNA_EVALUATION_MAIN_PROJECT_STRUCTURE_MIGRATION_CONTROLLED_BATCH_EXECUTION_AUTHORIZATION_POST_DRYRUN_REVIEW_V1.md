# Luna Evaluation — Main Project Structure Migration Controlled Batch Execution Authorization Post-DryRun Review v1

## 目的

运行并验证：

`Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Authorization-Post-DryRun-Review-v1-001`

本阶段 **review only**：只审查上游 DryRun 是否可信，不发 request、不 grant、不 arming、不执行 batch、不做 file operation、不 rerun verifier、不执行 rollback rehearsal、不跑 post-migration tests。

## 运行方式

### 1) 运行（生成 16 类 review 产物）

默认（尝试写入仓库 `_eval_out`，若无权限请使用 `--output-root` 指向 workspace）：

```bash
python3 -m tools.evaluation.governance.run_main_project_structure_migration_controlled_batch_execution_authorization_post_dryrun_review_v1
```

workspace fallback 推荐命令（示例）：

```bash
python3 -m tools.evaluation.governance.run_main_project_structure_migration_controlled_batch_execution_authorization_post_dryrun_review_v1 \
  --output-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_batch_exec_auth_post_review" \
  --controlled-batch-execution-authorization-dryrun-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_batch_exec_auth_dryrun"
```

### 2) 验证（verifier）

```bash
python3 -m tools.evaluation.governance.verify_main_project_structure_migration_controlled_batch_execution_authorization_post_dryrun_review_v1 \
  --output-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_batch_exec_auth_post_review" \
  --controlled-batch-execution-authorization-dryrun-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_batch_exec_auth_dryrun"
```

## 预期输出

输出目录内必须包含：

- `summary.json`
- `verifier_report.json`
- 其余 14 个 review 产物

并满足：

- `verifier=GO`
- `boundary_ok=true`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_AUTHORIZATION_POST_DRYRUN_REVIEW_READY_FOR_CONTROLLED_BATCH_EXECUTION_ARMING_PLANNING`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Arming-Planning-v1-001`
- request/grant/arming/execution/file-op/rerun/rollback/tests 全部 false

## workspace_fallback 约定

当输入 root 来自 workspace fallback（`source_path_mode=workspace_fallback`）时：

- 本阶段 `summary.json` 必须继续记录：
  - `source_path_mode=workspace_fallback`
  - `standard_eval_out_write_pending_on_local_repro=true`

该标记 **不** 等于标准仓库 `_eval_out` 已落盘。

