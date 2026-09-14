# Evaluation — RealVideo FrameSample Smoke v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-FrameSample-Smoke-001`

## 输入根（默认）

| 输入 | 路径 |
|------|------|
| RealVideo CaseRegistry | `_eval_out/cross_modal_vision_ocr_realvideo_case_registry_smoke_v0/` |
| Poster Track B closure | `_eval_out/poster_testboard_track_b_closure_v0/` |
| Metrics collector | `_eval_out/cross_modal_vision_ocr_testboard_metrics_collector_smoke_v0/` |
| Simulation Lab harness | `_eval_out/simulation_lab_minimal_harness_v0/developer_full/` |
| Vision ingest | `_eval_out/video_frame_minimal_ingest_smoke_v0/` |
| Vision frame trace | `_eval_out/vision_frame_trace_stream_registry_smoke_v0/` |
| Vision frame input governance | `_eval_out/vision_frame_input_governance_smoke_v0/` |
| Public facility governance | `_eval_out/public_facility_semantic_correction_governance_smoke_v0/` |

## 运行

```bash
python3 tools/evaluation/midplatform/run_cross_modal_vision_ocr_realvideo_frame_sample_smoke_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_frame_sample_smoke_v0 \
  --realvideo-registry-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_case_registry_smoke_v0 \
  --poster-track-b-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_testboard_track_b_closure_v0 \
  --metrics-collector-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_metrics_collector_smoke_v0 \
  --simulation-lab-harness-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full \
  --vision-ingest-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/video_frame_minimal_ingest_smoke_v0 \
  --vision-frame-trace-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_frame_trace_stream_registry_smoke_v0 \
  --vision-frame-input-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_frame_input_governance_smoke_v0

python3 tools/evaluation/midplatform/verify_cross_modal_vision_ocr_realvideo_frame_sample_smoke_v0.py \
  --frame-sample-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_frame_sample_smoke_v0
```

`--bootstrap-inputs` 仅在缺少前置 vision/registry 产物时使用（前置 ingest 不计入本 phase 的 `new_video_decoded`）。

GO/NO_GO：[pack](./LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_REALVIDEO_FRAME_SAMPLE_SMOKE_GO_NO_GO_PACK_V0.md)
