# Luna — RealVideo OCRRequest Gated Submission v0

**Phase**：`CrossModal-Vision-OCR-TestBoard-v1-RealVideo-OCRRequest-Gated-Submission-001`

## 目的

基于 RealVideo ROI-to-OCR Reference 中 **eligible** 的 `upper_sign_roi` OCRRequest reference，经 **OCR mainline bridge** 执行 gated submission，产出 OCR evidence candidate。

## 原则

- 仅 `upper_sign_roi` 可提交；非 text ROI 禁止
- RapidOCR lightweight；禁止 PaddleOCR heavy；禁止 direct provider bypass
- 禁止 MOCK_TEXT；`empty_text` 不等于失败
- 全部 `fact_status=not_fact`；`write_allowed=false`

## 实现

- Capability：`capabilities/ocr_runtime/realvideo_ocr_request_gated_submission_v0.py`
- Runner：`tools/evaluation/ocr/run_realvideo_ocr_request_gated_submission_v0.py`
- Verifier：`tools/evaluation/ocr/verify_realvideo_ocr_request_gated_submission_v0.py`

## 评测

[LUNA_EVALUATION_REALVIDEO_OCR_REQUEST_GATED_SUBMISSION_V0.md](../evaluation/LUNA_EVALUATION_REALVIDEO_OCR_REQUEST_GATED_SUBMISSION_V0.md)

## 建议下一跳

**Phase-RealVideo-OCR-Evidence-ReadOnly-Consumer-001** — 见 [LUNA_REALVIDEO_OCR_EVIDENCE_READONLY_CONSUMER_V0.md](./LUNA_REALVIDEO_OCR_EVIDENCE_READONLY_CONSUMER_V0.md)

**Phase-RealVideo-OCR-Reference-Update-001**（readonly consumer 之后）
