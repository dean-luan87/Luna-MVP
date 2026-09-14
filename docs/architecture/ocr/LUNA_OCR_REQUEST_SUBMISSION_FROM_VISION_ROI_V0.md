# Luna — OCR Request Submission from Vision ROI v0

**Phase**：`Phase-OCR-Request-Submission-Gated-Smoke-001`

## 目的

在显式 **gated evaluation-only** 条件下，将 Vision ROI bridge 产出的 `not_submitted` OCRRequest candidate 提交至 `ocr_mainline_bridge_v0`，获得 OCR evidence / bridge_pack。

## 原则

- 只提交已生成的 candidate；不绕过 ImageInputGate / normalization / ROI governance。
- 不直连 RapidOCR / PaddleOCR；必须经过 OCR mainline bridge。
- 输出仍为 OCR evidence candidate；不做跨模态融合、不写事实层。

## 环境门控（runner 强制）

| 变量 | 建议值 |
|------|--------|
| `LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0` | `true` |
| `LUNA_ENABLE_OCR_STUB_PROVIDER_V0` | `true` |
| `LUNA_ENABLE_OCR_REAL_PROVIDER_V0` | `false` |
| `LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0` | `false` |
| `LUNA_OCR_SUBMISSION_EVAL_ONLY` | `true` |

## 实现

- `capabilities/ocr_runtime/ocr_request_submission_from_vision_roi_v0.py`
- `tools/evaluation/ocr/run_ocr_request_submission_from_vision_roi_v0.py`
- `tools/evaluation/ocr/verify_ocr_request_submission_from_vision_roi_v0.py`

## 评测

[LUNA_EVALUATION_OCR_REQUEST_SUBMISSION_FROM_VISION_ROI_V0.md](../evaluation/LUNA_EVALUATION_OCR_REQUEST_SUBMISSION_FROM_VISION_ROI_V0.md)

## 建议下一跳

**Phase-Vision-OCR-Evidence-ReadOnly-Consumer-001**（已实现）：只读消费 submission collection。见 [LUNA_VISION_TRIGGERED_OCR_EVIDENCE_READONLY_CONSUMER_V0.md](./LUNA_VISION_TRIGGERED_OCR_EVIDENCE_READONLY_CONSUMER_V0.md)。

**Phase-OCR-Real-RapidOCR-Submission-From-Vision-ROI-Gated-001**（另开 phase）：在相同 submission 骨架下启用 gated real provider。
