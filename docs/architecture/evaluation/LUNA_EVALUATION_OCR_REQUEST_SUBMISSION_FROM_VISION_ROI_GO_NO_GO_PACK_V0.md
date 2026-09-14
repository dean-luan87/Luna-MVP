# Luna — GO / NO_GO: OCR Request Submission from Vision ROI v0

## GO

- Vision ROI OCRRequest candidate 在 gated eval-only 下经 **ocr_mainline_bridge** 提交成功。
- result matrix / collection / audit 完整。
- `rapidocr_invoked=false`，`paddleocr_invoked=false`，无事实写入、无融合、无导航。
- verifier = **GO**。

## CONDITIONAL_GO

- 部分提交失败但 matrix / error 完整；或无可提交 candidate 但 plan 完整。
- 无越界；verifier = **CONDITIONAL_GO**。

## NO_GO

- 直连 RapidOCR / PaddleOCR 绕过 bridge。
- 写 MidPlatform fact / Scene Delta / WorldModel。
- 跨模态融合或导航决策。
- audit 缺失。
