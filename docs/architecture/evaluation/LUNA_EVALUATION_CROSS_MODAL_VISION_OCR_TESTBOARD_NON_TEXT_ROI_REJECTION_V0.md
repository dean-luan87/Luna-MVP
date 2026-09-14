# Luna — Evaluation: TestBoard NonText ROI Rejection v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-NonTextROI-Rejection-001`

## 运行

```bash
python3 tools/evaluation/midplatform/run_cross_modal_vision_ocr_testboard_non_text_roi_rejection_v0.py \
  --duplicate-conflicting-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_duplicate_conflicting_smoke_v0 \
  --testboard-expansion-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_expansion_smoke_v0 \
  --vision-roi-bridge-root /abs/path/_eval_out/vision_roi_to_ocr_request_bridge_smoke_v0 \
  --output-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_non_text_roi_rejection_smoke_v0

python3 tools/evaluation/midplatform/verify_cross_modal_vision_ocr_testboard_non_text_roi_rejection_v0.py \
  --smoke-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_non_text_roi_rejection_smoke_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_NON_TEXT_ROI_REJECTION_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_NON_TEXT_ROI_REJECTION_GO_NO_GO_PACK_V0.md)
