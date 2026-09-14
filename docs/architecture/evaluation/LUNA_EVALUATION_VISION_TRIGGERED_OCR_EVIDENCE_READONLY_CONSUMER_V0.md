# Luna — Evaluation: Vision-triggered OCR Evidence ReadOnly Consumer v0

**Phase**：`Phase-Vision-OCR-Evidence-ReadOnly-Consumer-001`

## 输入

默认：`/_eval_out/ocr_request_submission_from_vision_roi_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/ocr/run_vision_triggered_ocr_evidence_readonly_consumer_v0.py \
  --output-root /abs/path/_eval_out/vision_triggered_ocr_evidence_readonly_consumer_smoke_v0 \
  --ocr-submission-from-vision-roi-root /abs/path/_eval_out/ocr_request_submission_from_vision_roi_smoke_v0

python3 tools/evaluation/ocr/verify_vision_triggered_ocr_evidence_readonly_consumer_v0.py \
  --smoke-root /abs/path/_eval_out/vision_triggered_ocr_evidence_readonly_consumer_smoke_v0
```

## GO / NO_GO

[LUNA_EVALUATION_VISION_TRIGGERED_OCR_EVIDENCE_READONLY_CONSUMER_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_VISION_TRIGGERED_OCR_EVIDENCE_READONLY_CONSUMER_GO_NO_GO_PACK_V0.md)
