# Luna Evaluation — Scene Delta Executor Trace Stub from Generic Dry-Run v0

**Phase**：`Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-Generic-DryRun-001`  
**Runner**：`tools/evaluation/midplatform/run_scene_delta_executor_trace_stub_from_generic_dryrun_v0.py`  
**Verifier**：`tools/evaluation/midplatform/verify_scene_delta_executor_trace_stub_from_generic_dryrun_v0.py`

## 前置

- `Phase-MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-001` = GO（OCR dry-run）  
- `Phase-MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-From-Vision-001` = GO（Vision dry-run）

## 自动识别规则

在 **`--dry-run-root`** 下：

1. 若存在 **`scene_delta_write_candidate_dryrun_from_vision_summary.json`** 且 **`schema_version`** 为 `scene_delta_write_candidate_dryrun_from_vision_summary_v0` → **Vision** 文件集。  
2. 否则若存在 **`scene_delta_write_candidate_dryrun_summary.json`** 且 **`schema`** 为 `scene_delta_write_candidate_dryrun_summary_v0` → **OCR** 文件集。  
3. 否则报错退出。

## 命令示例

**Vision dry-run 输入**（默认 `--dry-run-root` 指向 Vision smoke）：

```bash
python3 tools/evaluation/midplatform/run_scene_delta_executor_trace_stub_from_generic_dryrun_v0.py \
  --dry-run-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_write_candidate_dryrun_from_vision_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_trace_stub_from_generic_dryrun_vision_smoke_v0

python3 tools/evaluation/midplatform/verify_scene_delta_executor_trace_stub_from_generic_dryrun_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_trace_stub_from_generic_dryrun_vision_smoke_v0
```

**OCR dry-run 回归**：

```bash
python3 tools/evaluation/midplatform/run_scene_delta_executor_trace_stub_from_generic_dryrun_v0.py \
  --dry-run-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_write_candidate_dryrun_verifier_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_trace_stub_from_generic_dryrun_ocr_smoke_v0

python3 tools/evaluation/midplatform/verify_scene_delta_executor_trace_stub_from_generic_dryrun_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_trace_stub_from_generic_dryrun_ocr_smoke_v0
```

## 产物

| 文件 | 说明 |
|------|------|
| `scene_delta_executor_trace_stub_generic_summary.json` | 含 **dry_run_loader**、flavor、`trace_id` 等 |
| `scene_delta_executor_trace_stub_generic.json` | `scene_delta_executor_trace_stub_generic_v0` |
| `scene_delta_executor_planned_step_matrix_generic.json` | 8 步矩阵（仅允许 planned_only / blocked_by_policy / skipped_no_write） |
| `scene_delta_executor_input_compatibility_report_generic.json` | OCR / Vision 兼容性与 no-write 侧检查 |
| `scene_delta_executor_trace_stub_generic_audit_report.json` | generic no-write audit |
| `scene_delta_executor_trace_stub_generic_notes.md` | 短说明 |
| `scene_delta_executor_trace_stub_generic_verifier_report.json` | Meta-verifier |

## 退出码

Verifier：**GO / CONDITIONAL_GO** → **0**；**NO_GO** → **2**。

GO 语义见 [LUNA_EVALUATION_SCENE_DELTA_EXECUTOR_TRACE_STUB_GENERIC_DRYRUN_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_SCENE_DELTA_EXECUTOR_TRACE_STUB_GENERIC_DRYRUN_GO_NO_GO_PACK_V0.md)。
