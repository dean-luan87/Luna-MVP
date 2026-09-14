# Luna Evaluation — Main Project Structure Migration B0 Harness Adoption Planning v1

## 目的

运行并验证：

`Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-Planning-v1-001`

本阶段仅做 **B0 harness adoption planning**：只规划 B0 如何使用统一 Batch Preflight Harness 进行 preflight；不生成/不 enforce 正式 harness，不执行 preflight、不执行迁移、不 arming、不 file-op。

## 运行方式

### 1) 运行（生成 18 类产物）

默认（尝试写入仓库 `_eval_out`，若无权限请使用 `--output-root` 指向 workspace）：

```bash
python3 -m tools.evaluation.governance.run_main_project_structure_migration_b0_harness_adoption_planning_v1
```

workspace fallback 推荐命令（示例）：

```bash
python3 -m tools.evaluation.governance.run_main_project_structure_migration_b0_harness_adoption_planning_v1 \
  --output-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/b0_harness_adoption_planning" \
  --batch-preflight-harness-extraction-post-review-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/batch_preflight_harness_extraction_post_review"
```

### 2) 验证（verifier）

```bash
python3 -m tools.evaluation.governance.verify_main_project_structure_migration_b0_harness_adoption_planning_v1 \
  --output-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/b0_harness_adoption_planning" \
  --batch-preflight-harness-extraction-post-review-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/batch_preflight_harness_extraction_post_review"
```

## 预期输出

- `verifier=GO`
- `selected_batch_id=B0`、`b0_only=true`、`b1_b7_harness_adoption_deferred=true`
- `harness_generated_now=false`、`harness_enforced_now=false`、`harness_runtime_integrated_now=false`
- `b0_batch_config_applied_to_real_batch_now=false`、`b0_preflight_executed_now=false`
- all `actual_file_*_executed=false`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-DryRun-v1-001`

