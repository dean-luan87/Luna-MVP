# Evaluation — Benchmark Collector Real Values Planning v0

```bash
python3 tools/evaluation/midplatform/run_cross_modal_vision_ocr_benchmark_real_values_planning_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_planning_v0 \
  --v1-track-closures-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_v1_track_closures_v0 \
  --regression-comparison-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_v1_regression_comparison_v0 \
  --metrics-schema-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_metrics_schema_smoke_v0 \
  --metrics-collector-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_metrics_collector_smoke_v0 \
  --simulation-lab-harness-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full

python3 tools/evaluation/midplatform/verify_cross_modal_vision_ocr_benchmark_real_values_planning_v0.py \
  --planning-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_planning_v0
```

GO/NO_GO：[pack](./LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_BENCHMARK_REAL_VALUES_PLANNING_GO_NO_GO_PACK_V0.md)
