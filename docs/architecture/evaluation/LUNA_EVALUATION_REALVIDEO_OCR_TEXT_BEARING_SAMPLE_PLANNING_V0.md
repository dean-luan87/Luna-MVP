# Luna — Evaluation: RealVideo OCR Text-Bearing Sample Planning v0

**Phase**：`Phase-RealVideo-OCR-Text-Bearing-Sample-Planning-001`

## 运行

```bash
python3 tools/evaluation/midplatform/run_realvideo_ocr_text_bearing_sample_planning_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_text_bearing_sample_planning_smoke_v0 \
  --realvideo-reference-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_reference_closure_smoke_v0 \
  --realvideo-reference-update-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_reference_update_smoke_v0 \
  --realvideo-readonly-consumer-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_evidence_readonly_consumer_smoke_v0 \
  --realvideo-gated-submission-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_request_gated_submission_smoke_v0 \
  --realvideo-roi-to-ocr-reference-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_v0 \
  --realvideo-frame-sample-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_frame_sample_smoke_v0 \
  --realvideo-case-registry-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_case_registry_smoke_v0 \
  --benchmark-real-values-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-lab-harness-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full
```

## 验证

```bash
python3 tools/evaluation/midplatform/verify_realvideo_ocr_text_bearing_sample_planning_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_text_bearing_sample_planning_smoke_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_REALVIDEO_OCR_TEXT_BEARING_SAMPLE_PLANNING_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_REALVIDEO_OCR_TEXT_BEARING_SAMPLE_PLANNING_GO_NO_GO_PACK_V0.md)
