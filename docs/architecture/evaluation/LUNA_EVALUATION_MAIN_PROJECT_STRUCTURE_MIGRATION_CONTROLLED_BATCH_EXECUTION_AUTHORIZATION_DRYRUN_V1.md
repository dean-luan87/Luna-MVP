# Luna Evaluation — Main Project Structure Migration Controlled Batch Execution Authorization DryRun v1

## 目的

本评测文档用于运行并验证：

`Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Authorization-DryRun-v1-001`

该阶段只做 dry-run 消费模拟，不发 request、不 grant、不 arming、不执行 batch、不做 file operation、不 rerun verifier、不跑 rollback rehearsal、不执行 post-migration tests。

## 运行方式

### 1) 运行（生成 17 类产物）

默认（尝试写入仓库 `_eval_out`，若无权限请使用 `--output-root` 指向 workspace）：

```bash
python -m tools.evaluation.governance.run_main_project_structure_migration_controlled_batch_execution_authorization_dryrun_v1
```

workspace fallback 推荐命令（示例）：

```bash
python -m tools.evaluation.governance.run_main_project_structure_migration_controlled_batch_execution_authorization_dryrun_v1 \
  --output-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_batch_exec_auth_dryrun" \
  --controlled-batch-execution-authorization-planning-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_batch_exec_auth_planning"
```

### 2) 验证（verifier）

```bash
python -m tools.evaluation.governance.verify_main_project_structure_migration_controlled_batch_execution_authorization_dryrun_v1 \
  --output-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_batch_exec_auth_dryrun" \
  --controlled-batch-execution-authorization-planning-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_batch_exec_auth_planning"
```

## 预期输出

输出目录内必须包含：

- `summary.json`
- `verifier_report.json`
- 其余 15 个 dry-run 产物（见 governance 文档或 runner 输出清单）

并满足：

- `verifier=GO`
- `boundary_ok=true`
- 所有执行类字段（request/grant/arming/execution/file op/rerun/rollback/tests）保持 `false`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Authorization-Post-DryRun-Review-v1-001`

## workspace_fallback 约定

当 `--output-root` 使用 workspace 路径或上游输入来自 workspace fallback 时：

- `summary.json` 必须记录：
  - `source_path_mode=workspace_fallback`
  - `standard_eval_out_write_pending_on_local_repro=true`

该标记 **不** 等于标准仓库 `_eval_out` 已落盘。

