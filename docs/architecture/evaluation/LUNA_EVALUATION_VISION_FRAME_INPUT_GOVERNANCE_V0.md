# Luna 评测 — Vision Frame Input Governance v0

**Phase**：`Phase-Vision-Frame-Input-Governance-001`  
**Verifier**：`tools/evaluation/vision/verify_vision_frame_input_governance_v0.py`

## 输入（frame trace smoke 根目录）

须包含：

- `vision_stream_registry.json`  
- `vision_frame_trace.jsonl`  
- `vision_frame_lineage_matrix.json`  
- `vision_sampling_consistency_report.json`  
- `vision_frame_trace_audit_report.json`  

## CLI

```bash
python3 tools/evaluation/vision/run_vision_frame_input_governance_v0.py \
  --frame-trace-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_frame_trace_stream_registry_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_frame_input_governance_smoke_v0
```

Verifier 需同时传入 frame trace 根与 governance 输出根：

```bash
python3 tools/evaluation/vision/verify_vision_frame_input_governance_v0.py \
  --frame-trace-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_frame_trace_stream_registry_smoke_v0 \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_frame_input_governance_smoke_v0
```

## 产物（`--output-root`）

| 文件 | 说明 |
|------|------|
| `vision_frame_input_governance_summary.json` | 汇总计数、全局 STCM/performance 占位 |
| `vision_frame_input_governance_matrix.json` | 逐帧治理结果 |
| `vision_provider_input_candidate.json` | `vision_frame_input_candidate_v0`（仅 input_governance） |
| `vision_frame_input_governance_audit_report.json` | audit |
| `vision_frame_input_governance_notes.md` | 短说明 |
| `vision_frame_input_governance_verifier_report.json` | verifier 输出 |

GO / CONDITIONAL_GO / NO_GO：`LUNA_EVALUATION_VISION_FRAME_INPUT_GOVERNANCE_GO_NO_GO_PACK_V0.md`。
