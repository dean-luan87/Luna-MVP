# Luna — RapidOCR Submission from Vision ROI v0

**Phase**：`Phase-OCR-Real-RapidOCR-Submission-From-Vision-ROI-Gated-001`

## 目的

在 gated evaluation-only 条件下，将 Vision ROI 生成的 OCRRequest candidate 经 **ocr_mainline_bridge** 提交，并启用 RapidOCR lightweight real provider（允许 stub fallback）。

## 原则

- 必须经过 OCR mainline bridge；不得直连 RapidOCR。
- 不启用 PaddleOCR；不做 CrossModal Fusion；不写事实层。

## 环境门控

| 变量 | 值 |
|------|-----|
| `LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0` | `true` |
| `LUNA_ENABLE_OCR_REAL_PROVIDER_V0` | `true` |
| `LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0` | `true` |
| `LUNA_ENABLE_OCR_STUB_PROVIDER_V0` | `true` |
| `LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0` | `false` |
| `LUNA_OCR_SUBMISSION_EVAL_ONLY` | `true` |
| `LUNA_OCR_LIGHTWEIGHT_MAX_EDGE_PX` | `512`（默认） |

## 评测

[LUNA_EVALUATION_RAPIDOCR_SUBMISSION_FROM_VISION_ROI_V0.md](../evaluation/LUNA_EVALUATION_RAPIDOCR_SUBMISSION_FROM_VISION_ROI_V0.md)

## 建议下一跳

**Phase-Vision-Triggered-OCR-RapidOCR-ReadOnly-Consumer-001**（已实现）：见 [LUNA_VISION_TRIGGERED_RAPIDOCR_EVIDENCE_READONLY_CONSUMER_V0.md](./LUNA_VISION_TRIGGERED_RAPIDOCR_EVIDENCE_READONLY_CONSUMER_V0.md)。
