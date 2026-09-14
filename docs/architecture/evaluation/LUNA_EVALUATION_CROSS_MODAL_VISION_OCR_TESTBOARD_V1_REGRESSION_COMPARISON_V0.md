# Evaluation — TestBoard v1 Regression Comparison v0

```bash
python3 tools/evaluation/midplatform/run_cross_modal_vision_ocr_testboard_v1_regression_comparison_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_v1_regression_comparison_v0 \
  --v0-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_v0_closure_smoke_v0 \
  --v1-planning-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_v1_planning_smoke_v0 \
  --metrics-collector-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_metrics_collector_smoke_v0 \
  --poster-track-b-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_testboard_track_b_closure_v0 \
  --realvideo-registry-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_case_registry_smoke_v0 \
  --realvideo-frame-sample-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_frame_sample_smoke_v0 \
  --realvideo-roi-to-ocr-reference-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_v0 \
  --simulation-lab-harness-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full \
  --bootstrap-v0-closure

python3 tools/evaluation/midplatform/verify_cross_modal_vision_ocr_testboard_v1_regression_comparison_v0.py \
  --regression-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_v1_regression_comparison_v0
```

GO/NO_GO：[pack](./LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_V1_REGRESSION_COMPARISON_GO_NO_GO_PACK_V0.md)
