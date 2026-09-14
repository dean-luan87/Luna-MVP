# Luna — CrossModal Vision OCR Reference Only v0

**Phase**：`Phase-CrossModal-Vision-OCR-Evidence-Reference-Only-001`

## 目的

建立 Vision recognition evidence 与 Vision-triggered OCR evidence 的 **reference-only** 对齐候选；按 `frame_id + roi_id` 并列引用，不做融合、不解释文本。

## 原则

- Reference Only，不是 Fusion。
- 不写 MidPlatform fact / Scene Delta / WorldModel。
- 不调用 AI interpretation / navigation；不调用真实 OCR / Vision provider。

## 实现

- `capabilities/midplatform/cross_modal_vision_ocr_reference_only_v0.py`
- `tools/evaluation/midplatform/run_cross_modal_vision_ocr_reference_only_v0.py`
- `tools/evaluation/midplatform/verify_cross_modal_vision_ocr_reference_only_v0.py`

## 评测

[LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_REFERENCE_ONLY_V0.md](../evaluation/LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_REFERENCE_ONLY_V0.md)

## 建议下一跳

**Phase-CrossModal-Vision-OCR-Reference-Only-002**（RapidOCR 路径，已实现）：见 [LUNA_CROSS_MODAL_VISION_OCR_REFERENCE_ONLY_RAPIDOCR_V0.md](./LUNA_CROSS_MODAL_VISION_OCR_REFERENCE_ONLY_RAPIDOCR_V0.md)。
