# Luna 评测 — Vision Frame Trace + Stream Registry v0

**Phase**：`Phase-Vision-FrameTrace-StreamRegistry-001`  
**Verifier**：`tools/evaluation/vision/verify_vision_frame_trace_stream_registry_v0.py`

**注意**：本 phase **不是**视角识别前置，**不**调用 YOLO / VLM / OCR；仅登记标准帧轨迹。接任何视觉识别前须先完成 **Vision-Frame-Input-Governance-001** 与 **Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001**，见架构文档 [LUNA_VISION_MAINLINE_PHASE_ORDER_AND_INPUT_GATE_V0.md](../vision/LUNA_VISION_MAINLINE_PHASE_ORDER_AND_INPUT_GATE_V0.md)。

## 输入（上游 ingest 根目录）

须包含（由 `run_video_frame_minimal_ingest_smoke_v0.py` 生成）：

- `video_frame_ingest_summary.json`  
- `video_frame_sampling_report.json`  
- `video_frame_envelopes.jsonl`  
- `video_frame_matrix.json`  
- `video_frame_audit_report.json`  

## CLI

```bash
python3 tools/evaluation/vision/run_vision_frame_trace_stream_registry_v0.py \
  --video-ingest-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/video_frame_minimal_ingest_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_frame_trace_stream_registry_smoke_v0
```

可选：`--repo-root /ABS/Luna-Workspace-Min`（默认与 runner 推导根一致）。

## 产物（`--output-root`）

| 文件 | 说明 |
|------|------|
| `vision_frame_trace_stream_registry_summary.json` | 本 phase 汇总 |
| `vision_stream_registry.json` | `vision_stream_registry_v0` |
| `vision_frame_trace.jsonl` | 每行 `vision_frame_trace_event_v0` |
| `vision_frame_lineage_matrix.json` | 帧血缘表 |
| `vision_sampling_consistency_report.json` | 采样一致性检查结果 |
| `vision_frame_trace_audit_report.json` | 只读 audit |
| `vision_frame_trace_stream_registry_notes.md` | 短说明 |
| `vision_frame_trace_stream_registry_verifier_report.json` | verifier 输出 |

## Verifier

```bash
python3 tools/evaluation/vision/verify_vision_frame_trace_stream_registry_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_frame_trace_stream_registry_smoke_v0
```

GO / CONDITIONAL_GO / NO_GO：`LUNA_EVALUATION_VISION_FRAME_TRACE_STREAM_REGISTRY_GO_NO_GO_PACK_V0.md`。
