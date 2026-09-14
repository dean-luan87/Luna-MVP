# Luna — Evaluation: CrossModal Vision OCR TestBoard Metrics Schema v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Schema-001`

## 运行

```bash
python3 tools/evaluation/midplatform/run_cross_modal_vision_ocr_testboard_metrics_schema_v0.py \
  --v0-closure-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_v0_closure_smoke_v0 \
  --v1-planning-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_v1_planning_smoke_v0 \
  --poster-governance-root /abs/path/_eval_out/poster_layout_segmentation_governance_smoke_v0 \
  --output-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_metrics_schema_smoke_v0

python3 tools/evaluation/midplatform/verify_cross_modal_vision_ocr_testboard_metrics_schema_v0.py \
  --smoke-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_metrics_schema_smoke_v0
```

## GO / NO_GO

[LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_METRICS_SCHEMA_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_METRICS_SCHEMA_GO_NO_GO_PACK_V0.md)
