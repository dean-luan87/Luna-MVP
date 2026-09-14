# Luna — CrossModal Vision OCR TestBoard NonText ROI Rejection v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-NonTextROI-Rejection-001`

## 目的

将 `NON_TEXT_ROI_REJECTED` 转为 executed，验证非文本 ROI 在 OCR 前被拒绝；TestBoard 达到 **10 executed / 0 planned_only**。

## 原则

- 从 Vision ROI → OCR bridge rejection matrix 关联拒绝原因。
- 不生成 OCRRequest、不调用 OCR、不进入 fusion / Scene Delta candidate。

## 评测

[LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_NON_TEXT_ROI_REJECTION_V0.md](../evaluation/LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_NON_TEXT_ROI_REJECTION_V0.md)

## 建议下一跳

**Phase-CrossModal-Vision-OCR-TestBoard-v0-Closure-001**（见 [LUNA_CROSS_MODAL_VISION_OCR_TESTBOARD_V0_CLOSURE_V0.md](./LUNA_CROSS_MODAL_VISION_OCR_TESTBOARD_V0_CLOSURE_V0.md)）— TestBoard v0 已冻结。
