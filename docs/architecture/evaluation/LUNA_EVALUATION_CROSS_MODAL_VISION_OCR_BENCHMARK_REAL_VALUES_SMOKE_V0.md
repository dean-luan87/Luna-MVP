# Evaluation — Benchmark Collector Real Values Smoke v0

```bash
python3 tools/evaluation/midplatform/run_cross_modal_vision_ocr_benchmark_real_values_smoke_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --benchmark-planning-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_planning_v0 \
  --v1-track-closures-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_v1_track_closures_v0 \
  --regression-comparison-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_v1_regression_comparison_v0 \
  --metrics-schema-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_metrics_schema_smoke_v0 \
  --metrics-collector-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_metrics_collector_smoke_v0 \
  --public-facility-runtime-dryrun-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/public_facility_runtime_dryrun_v0 \
  --poster-track-b-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_testboard_track_b_closure_v0 \
  --realvideo-roi-to-ocr-reference-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_v0 \
  --simulation-lab-harness-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full

python3 tools/evaluation/midplatform/verify_cross_modal_vision_ocr_benchmark_real_values_smoke_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0
```

GO/NO_GO：[pack](./LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_BENCHMARK_REAL_VALUES_SMOKE_GO_NO_GO_PACK_V0.md)
