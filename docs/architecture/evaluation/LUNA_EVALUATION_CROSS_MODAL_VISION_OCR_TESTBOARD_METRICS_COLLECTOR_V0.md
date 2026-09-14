# Luna — Evaluation: CrossModal Vision OCR TestBoard Metrics Collector v0

```bash
python3 tools/evaluation/midplatform/run_cross_modal_vision_ocr_testboard_metrics_collector_v0.py \
  --schema-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_metrics_schema_smoke_v0 \
  --v0-closure-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_v0_closure_smoke_v0 \
  --poster-governance-root /abs/path/_eval_out/poster_layout_segmentation_governance_smoke_v0 \
  --rapidocr-submission-root /abs/path/_eval_out/rapidocr_submission_from_vision_roi_smoke_v0 \
  --rapidocr-readonly-consumer-root /abs/path/_eval_out/vision_triggered_rapidocr_evidence_readonly_consumer_smoke_v0 \
  --reference-only-rapidocr-root /abs/path/_eval_out/cross_modal_vision_ocr_reference_only_rapidocr_smoke_v0 \
  --fusion-dryrun-root /abs/path/_eval_out/cross_modal_vision_ocr_fusion_candidate_dryrun_smoke_v0 \
  --gate-evaluator-root /abs/path/_eval_out/cross_modal_scene_delta_gate_evaluator_dryrun_smoke_v0 \
  --executor-trace-stub-root /abs/path/_eval_out/cross_modal_scene_delta_executor_trace_stub_smoke_v0 \
  --output-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_metrics_collector_smoke_v0

python3 tools/evaluation/midplatform/verify_cross_modal_vision_ocr_testboard_metrics_collector_v0.py \
  --smoke-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_metrics_collector_smoke_v0 \
  --schema-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_metrics_schema_smoke_v0 \
  --v0-closure-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_v0_closure_smoke_v0 \
  --poster-governance-root /abs/path/_eval_out/poster_layout_segmentation_governance_smoke_v0
```

GO/NO_GO：见 [pack](./LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_METRICS_COLLECTOR_GO_NO_GO_PACK_V0.md)
