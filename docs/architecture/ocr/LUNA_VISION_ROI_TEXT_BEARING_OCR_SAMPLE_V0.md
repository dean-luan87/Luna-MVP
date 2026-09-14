# Luna — Vision ROI Text-Bearing OCR Sample v0

**Phase**：`Phase-Vision-ROI-Text-Bearing-Sample-For-OCR-001`

## 目的

用本地含清晰文字的 **upper_sign_roi** fixture，沿 Vision ROI 形态 → OCRRequest → **ocr_mainline_bridge** → RapidOCR → 只读 consumer → CrossModal reference-only 验证 **非空 OCR 文本**。

## 原则

- 仅 evaluation-only；fixture 本地生成，`network_request_invoked=false`。
- 必须经过 OCR bridge；不得直连 RapidOCR；不启用 PaddleOCR。
- 不做融合、不解释文字、不写 MidPlatform / Scene Delta / WorldModel、不做导航。

## 环境门控

与 [LUNA_RAPIDOCR_SUBMISSION_FROM_VISION_ROI_V0.md](./LUNA_RAPIDOCR_SUBMISSION_FROM_VISION_ROI_V0.md) 相同。

## 评测

[LUNA_EVALUATION_VISION_ROI_TEXT_BEARING_OCR_SAMPLE_V0.md](../evaluation/LUNA_EVALUATION_VISION_ROI_TEXT_BEARING_OCR_SAMPLE_V0.md)

## 建议下一跳

**Phase-CrossModal-Vision-OCR-Fusion-Candidate-DryRun-001**（见 [LUNA_CROSS_MODAL_VISION_OCR_FUSION_CANDIDATE_DRYRUN_V0.md](../midplatform/LUNA_CROSS_MODAL_VISION_OCR_FUSION_CANDIDATE_DRYRUN_V0.md)）。
