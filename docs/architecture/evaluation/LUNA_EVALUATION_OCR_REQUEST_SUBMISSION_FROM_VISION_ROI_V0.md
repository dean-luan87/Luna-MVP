# Luna — Evaluation: OCR Request Submission from Vision ROI v0

**Phase**：`Phase-OCR-Request-Submission-Gated-Smoke-001`

## 前置

- `Phase-Vision-ROI-to-OCR-Request-Bridge-001` = GO
- `Phase-OCR-Mainline-Minimal-Bridge-001` = GO

## 输入

默认 bridge root：`_eval_out/vision_roi_to_ocr_request_bridge_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/ocr/run_ocr_request_submission_from_vision_roi_v0.py \
  --output-root /abs/path/_eval_out/ocr_request_submission_from_vision_roi_smoke_v0 \
  --vision-roi-to-ocr-bridge-root /abs/path/_eval_out/vision_roi_to_ocr_request_bridge_smoke_v0

python3 tools/evaluation/ocr/verify_ocr_request_submission_from_vision_roi_v0.py \
  --smoke-root /abs/path/_eval_out/ocr_request_submission_from_vision_roi_smoke_v0
```

## 产物

| 文件 | 说明 |
|------|------|
| `ocr_request_submission_plan_from_vision_roi.json` | 门控与选型计划 |
| `ocr_request_submission_result_matrix.json` | 逐 candidate 提交结果 |
| `ocr_submission_from_vision_roi_collection.json` | OCR 结果聚合 |
| `ocr_request_submission_from_vision_roi_audit_report.json` | 边界审计 |

## GO / NO_GO

[LUNA_EVALUATION_OCR_REQUEST_SUBMISSION_FROM_VISION_ROI_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_OCR_REQUEST_SUBMISSION_FROM_VISION_ROI_GO_NO_GO_PACK_V0.md)
