# Luna Evaluation — Main Project Structure Migration Batch Preflight Harness Extraction Post-DryRun Review v1

## 目的

运行并验证：

`Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-Post-DryRun-Review-v1-001`

本阶段仅做 **review-only**：审查 Harness Extraction DryRun 的可信度与边界，确认未生成/未 enforce/未集成 harness，未执行迁移/arming/file-op，未删除旧 phase，未修改 verifier/template，未进行 runtime 重构。

## 运行方式

### 1) 运行（生成 16 类产物）

默认（尝试写入仓库 `_eval_out`，若无权限请使用 `--output-root` 指向 workspace）：

```bash
python3 -m tools.evaluation.governance.run_main_project_structure_migration_batch_preflight_harness_extraction_post_dryrun_review_v1
```

workspace fallback 推荐命令（示例）：

```bash
python3 -m tools.evaluation.governance.run_main_project_structure_migration_batch_preflight_harness_extraction_post_dryrun_review_v1 \
  --output-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/batch_preflight_harness_extraction_post_review" \
  --batch-preflight-harness-extraction-dryrun-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/batch_preflight_harness_extraction_dryrun"
```

### 2) 验证（verifier）

```bash
python3 -m tools.evaluation.governance.verify_main_project_structure_migration_batch_preflight_harness_extraction_post_dryrun_review_v1 \
  --output-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/batch_preflight_harness_extraction_post_review" \
  --batch-preflight-harness-extraction-dryrun-root "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/batch_preflight_harness_extraction_dryrun"
```

## 预期输出

- `verifier=GO`
- `boundary_ok=true`
- `harness_generated_now=false`、`harness_enforced_now=false`、`harness_runtime_integrated_now=false`、`harness_registered_now=false`
- `runtime_refactor_executed_now=false`
- `old_phase_deleted_now=false`、`old_phase_deprecated_now=false`
- `verifier_modified_now=false`、`phase_template_modified_now=false`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_POST_DRYRUN_REVIEW_READY_FOR_B0_HARNESS_ADOPTION_PLANNING`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-Planning-v1-001`

