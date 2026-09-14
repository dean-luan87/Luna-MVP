# Luna — Vision-triggered OCR Evidence ReadOnly Consumer v0

**Phase**：`Phase-Vision-OCR-Evidence-ReadOnly-Consumer-001`

## 目的

只读消费由 Vision ROI → OCRRequest → gated submission 得到的 `ocr_submission_from_vision_roi_collection`，生成按 **candidate / frame / roi** 索引的 consumer view。

## 原则

- 不做 Vision+OCR 融合；不解释 OCR 文本含义。
- 不写 MidPlatform / Scene Delta / WorldModel；不做导航。

## 实现

- `capabilities/ocr_runtime/vision_triggered_ocr_evidence_readonly_consumer_v0.py`
- `tools/evaluation/ocr/run_vision_triggered_ocr_evidence_readonly_consumer_v0.py`
- `tools/evaluation/ocr/verify_vision_triggered_ocr_evidence_readonly_consumer_v0.py`

## 评测

[LUNA_EVALUATION_VISION_TRIGGERED_OCR_EVIDENCE_READONLY_CONSUMER_V0.md](../evaluation/LUNA_EVALUATION_VISION_TRIGGERED_OCR_EVIDENCE_READONLY_CONSUMER_V0.md)

## 建议下一跳

**Phase-CrossModal-Vision-OCR-Evidence-Reference-Only-001**（已实现）：Vision + OCR reference-only 对齐。见 [LUNA_CROSS_MODAL_VISION_OCR_REFERENCE_ONLY_V0.md](../midplatform/LUNA_CROSS_MODAL_VISION_OCR_REFERENCE_ONLY_V0.md)。

**Phase-OCR-Real-RapidOCR-Submission-From-Vision-ROI-Gated-001**（另开 phase）。
