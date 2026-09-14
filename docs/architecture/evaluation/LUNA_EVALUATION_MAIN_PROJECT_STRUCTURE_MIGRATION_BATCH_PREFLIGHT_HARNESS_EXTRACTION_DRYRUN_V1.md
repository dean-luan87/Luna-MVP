# Luna Evaluation — Main Project Structure Migration Batch Preflight Harness Extraction DryRun v1

## 目的

运行并验证：

`Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-DryRun-v1-001`

本阶段仅做 **harness 抽离规划 dry-run**：模拟消费 planning 产物，验证可被 B0–B7 消费；不生成正式 harness、不 enforce、不集成 runtime、不迁移、不 arming、不做 file-op。

## 运行方式

### 1) 运行（生成 15 类产物）

默认（尝试写入仓库 `_eval_out`，若无权限请使用 `--output-root` 指向 workspace）：

```bash
python3 -m tools.evaluation.governance.run_main_project_structure_migration_batch_preflight_harness_extraction_dryrun_v1
```

workspace fallback 推荐命令（示例）：

```bash
python3 -m tools.evaluation.governance.run_main_project_structure_migration_batch_preflight_harness_extraction_dryrun_v1 \
  --output-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/batch_preflight_harness_extraction_dryrun" \
  --batch-preflight-harness-extraction-planning-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/batch_preflight_harness_extraction_planning"
```

### 2) 验证（verifier）

```bash
python3 -m tools.evaluation.governance.verify_main_project_structure_migration_batch_preflight_harness_extraction_dryrun_v1 \
  --output-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/batch_preflight_harness_extraction_dryrun" \
  --batch-preflight-harness-extraction-planning-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/batch_preflight_harness_extraction_planning"
```

## 预期输出

- `verifier=GO`
- `boundary_ok=true`
- `harness_generated_now=false`、`harness_enforced_now=false`、`harness_runtime_integrated_now=false`
- `batch_config_applied_to_real_batch_now=false`、`batch_armed_now=false`、`batch_execution_started_now=false`
- all `actual_file_*_executed=false`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-Post-DryRun-Review-v1-001`

