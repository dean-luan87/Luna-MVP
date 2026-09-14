# Luna — Vision ROI → OCRRequest Bridge v0

**Phase**：`Phase-Vision-ROI-to-OCR-Request-Bridge-001`

## 目的

从 Vision ROI proposal / `vision_provider_input_pack` 中筛选适合 OCR 的 ROI，生成 **OCRRequest candidate**（`vision_roi_to_ocr_request_candidate_v0`）。

## 原则

- 只做触发与引用，不解释、不融合。
- 不调用 OCR runtime / RapidOCR / PaddleOCR。
- 不写 MidPlatform / Scene Delta / WorldModel。
- 不做导航决策、不调用 AI interpretation。
- 候选全程 `fact_status=not_fact`，`candidate_status=not_submitted`。

## 筛选规则（v0）

| ROI | 动作 |
|-----|------|
| `upper_sign_roi` | 生成 OCRRequest candidate |
| `center_roi` 且 `task_hint=sign_region` | 生成 OCRRequest candidate |
| 其他 | 写入 rejection matrix |

## 实现

- `capabilities/vision_runtime/vision_roi_to_ocr_request_bridge_v0.py`
- `tools/evaluation/vision/run_vision_roi_to_ocr_request_bridge_v0.py`
- `tools/evaluation/vision/verify_vision_roi_to_ocr_request_bridge_v0.py`

## 评测

[LUNA_EVALUATION_VISION_ROI_TO_OCR_REQUEST_BRIDGE_V0.md](../evaluation/LUNA_EVALUATION_VISION_ROI_TO_OCR_REQUEST_BRIDGE_V0.md)

## 建议下一跳

**Phase-OCR-Request-Submission-Gated-Smoke-001**（已实现）：经 `ocr_mainline_bridge` gated 提交 candidate，仍 evaluation-only。见 [LUNA_OCR_REQUEST_SUBMISSION_FROM_VISION_ROI_V0.md](../ocr/LUNA_OCR_REQUEST_SUBMISSION_FROM_VISION_ROI_V0.md)。
