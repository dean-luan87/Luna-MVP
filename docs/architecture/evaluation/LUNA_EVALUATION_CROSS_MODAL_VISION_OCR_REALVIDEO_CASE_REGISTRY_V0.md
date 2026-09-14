# Luna — Evaluation: RealVideo Case Registry v0

```bash
python3 tools/evaluation/midplatform/run_cross_modal_vision_ocr_realvideo_case_registry_v0.py \
  --v1-planning-root /abs/path/cross_modal_vision_ocr_testboard_v1_planning_smoke_v0 \
  --metrics-collector-root /abs/path/cross_modal_vision_ocr_testboard_metrics_collector_smoke_v0 \
  --poster-governance-root /abs/path/poster_layout_segmentation_governance_smoke_v0 \
  --public-facility-governance-root /abs/path/public_facility_semantic_correction_governance_smoke_v0 \
  --output-root /abs/path/cross_modal_vision_ocr_realvideo_case_registry_smoke_v0

python3 tools/evaluation/midplatform/verify_cross_modal_vision_ocr_realvideo_case_registry_v0.py \
  --smoke-root /abs/path/cross_modal_vision_ocr_realvideo_case_registry_smoke_v0
```

GO/NO_GO：[pack](./LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_REALVIDEO_CASE_REGISTRY_GO_NO_GO_PACK_V0.md)
