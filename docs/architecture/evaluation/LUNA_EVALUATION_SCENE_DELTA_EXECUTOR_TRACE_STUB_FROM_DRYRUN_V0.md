# Luna Evaluation — Scene Delta Executor Trace Stub from Dry-Run Smoke v0

**Phase**: `Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-DryRun-001`

## 目的

验证可由 **Scene Delta write candidate dry-run** 目录下的 summary / mapping / risk / no-write audit 生成 **executor trace stub** 与 **planned step matrix**、**executor 入参兼容报告**、**trace stub audit**；全程 **无真实 executor、无 Scene Delta 写入、无 DB、无事实层、无 AI**。

## 前置

- `Phase-MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-001` = GO  
- `Phase-MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001` = GO  

**默认输入 dry-run 根目录**：`_eval_out/scene_delta_write_candidate_dryrun_verifier_smoke_v0/`

## 命令

```bash
python3 tools/evaluation/midplatform/run_scene_delta_executor_trace_stub_from_dryrun_v0.py \
  --output-root /ABS/PATH/_eval_out/scene_delta_executor_trace_stub_from_dryrun_smoke_v0

python3 tools/evaluation/midplatform/verify_scene_delta_executor_trace_stub_from_dryrun_v0.py \
  --smoke-root /ABS/PATH/_eval_out/scene_delta_executor_trace_stub_from_dryrun_smoke_v0
```

## 产物

| 文件 | 说明 |
|------|------|
| `scene_delta_executor_trace_stub_summary.json` | 输入根、`trace_id`、源 dry_run / candidate 引用。 |
| `scene_delta_executor_trace_stub.json` | Trace stub 主体。 |
| `scene_delta_executor_planned_step_matrix.json` | 8 步 planned 矩阵。 |
| `scene_delta_executor_input_compatibility_report.json` | 与未来 executor 入参对齐的检查摘要。 |
| `scene_delta_executor_trace_stub_audit_report.json` | No-write audit。 |
| `scene_delta_executor_trace_stub_notes.md` | 短说明。 |
| `scene_delta_executor_trace_stub_verifier_report.json` | Verifier 报告。 |

## Verifier 退出码

- **GO** / **CONDITIONAL_GO**：**0**；**NO_GO**：**2**。
