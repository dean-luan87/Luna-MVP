# Luna — GO / NO_GO: Vision ROI → OCRRequest Bridge v0

## GO

- 从 Vision ROI 生成 ≥1 条 OCRRequest candidate（典型：`upper_sign_roi`）。
- `ocr_request.input_type=roi`，`allow_full_image=false`。
- `candidate_status=not_submitted`；未调用 OCR / AI / 导航。
- rejection matrix 完整。
- audit 无越界；verifier = **GO**。

## CONDITIONAL_GO

- 无可触发 OCR 的 ROI，但 rejection matrix 与 audit 完整。
- 无越界行为；verifier = **CONDITIONAL_GO**。

## NO_GO

- 调用 OCR provider / RapidOCR / PaddleOCR。
- 写入 MidPlatform fact / Scene Delta / WorldModel。
- 生成融合结论或导航决策。
- audit 缺失或 verifier 失败。
