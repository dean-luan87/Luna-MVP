# Luna — GO / NO_GO: RapidOCR Submission from Vision ROI v0

## GO

- Vision ROI OCRRequest 经 bridge 提交；至少一条 RapidOCR real path 成功，或 real provider 执行且空文本路径明确。
- `direct_rapidocr_invoked=false`；无事实写入、无融合；verifier = **GO**。

## CONDITIONAL_GO

- RapidOCR 不可用但 stub fallback / error matrix 完整；或全空文本但 real path 已执行。

## NO_GO

- 直连 RapidOCR 绕过 bridge；启用 PaddleOCR；写事实层；融合/导航/AI；audit 缺失。
