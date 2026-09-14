# Luna Evaluation — Main Project Structure Migration Batch Preflight Harness Extraction Planning v1

## 目的

运行并验证：

`Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-Planning-v1-001`

本阶段仅做 **harness 抽离规划**：定义 batch config schema、固定 preflight 检查清单、输出合同、verifier baseline、以及 B0–B7 adoption matrix。

## 运行方式

### 1) 运行（生成 12 类产物）

默认（尝试写入仓库 `_eval_out`，若无权限请使用 `--output-root` 指向 workspace）：

```bash
python3 -m tools.evaluation.governance.run_main_project_structure_migration_batch_preflight_harness_extraction_planning_v1
```

workspace fallback 推荐命令（示例）：

```bash
python3 -m tools.evaluation.governance.run_main_project_structure_migration_batch_preflight_harness_extraction_planning_v1 \
  --output-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/batch_preflight_harness_extraction_planning" \
  --controlled-batch-exec-auth-post-review-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_batch_exec_auth_post_review" \
  --controlled-batch-exec-arming-post-review-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_batch_exec_arming_post_review" \
  --b0-arming-request-planning-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/b0_arming_request_planning"
```

### 2) 验证（verifier）

```bash
python3 -m tools.evaluation.governance.verify_main_project_structure_migration_batch_preflight_harness_extraction_planning_v1 \
  --output-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/batch_preflight_harness_extraction_planning" \
  --controlled-batch-exec-auth-post-review-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_batch_exec_auth_post_review" \
  --controlled-batch-exec-arming-post-review-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_batch_exec_arming_post_review" \
  --b0-arming-request-planning-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/b0_arming_request_planning"
```

## 预期输出

- `verifier=GO`
- `boundary_ok=true`
- `harness_generated_now=false`、`harness_enforced_now=false`
- 12 类产物齐全，且 `batch_config_schema_planning_v1.json` 含全部必填字段
- `reusable_preflight_check_inventory_v1.json` 覆盖固定检查清单
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-DryRun-v1-001`

