# Evaluation — RealVideo ROI-to-OCR Reference v0

```bash
python3 tools/evaluation/midplatform/run_cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_v0 \
  --frame-sample-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_frame_sample_smoke_v0 \
  --realvideo-registry-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_case_registry_smoke_v0 \
  --vision-roi-proposal-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_roi_proposal_stub_smoke_v0 \
  --vision-roi-to-ocr-bridge-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_roi_to_ocr_request_bridge_smoke_v0 \
  --cross-modal-rapidocr-reference-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_reference_only_rapidocr_smoke_v0 \
  --poster-track-b-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_testboard_track_b_closure_v0 \
  --metrics-collector-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_metrics_collector_smoke_v0 \
  --simulation-lab-harness-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full

python3 tools/evaluation/midplatform/verify_cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_v0.py \
  --reference-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_v0
```

GO/NO_GO：[pack](./LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_REALVIDEO_ROI_TO_OCR_REFERENCE_GO_NO_GO_PACK_V0.md)
