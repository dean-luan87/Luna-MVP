# Luna — Evaluation: RealVideo OCRRequest Gated Submission v0

**Phase**：`CrossModal-Vision-OCR-TestBoard-v1-RealVideo-OCRRequest-Gated-Submission-001`

## 运行

```bash
python3 tools/evaluation/ocr/run_realvideo_ocr_request_gated_submission_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_request_gated_submission_smoke_v0 \
  --realvideo-roi-to-ocr-reference-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_v0 \
  --realvideo-frame-sample-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_frame_sample_smoke_v0 \
  --realvideo-case-registry-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_case_registry_smoke_v0 \
  --vision-roi-proposal-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_roi_proposal_stub_smoke_v0 \
  --vision-roi-to-ocr-bridge-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_roi_to_ocr_request_bridge_smoke_v0 \
  --benchmark-real-values-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-lab-harness-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full
```

## 验证

```bash
python3 tools/evaluation/ocr/verify_realvideo_ocr_request_gated_submission_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_request_gated_submission_smoke_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_REALVIDEO_OCR_REQUEST_GATED_SUBMISSION_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_REALVIDEO_OCR_REQUEST_GATED_SUBMISSION_GO_NO_GO_PACK_V0.md)
