# Luna — GO / NO_GO: CrossModal Reference Only (RapidOCR) v0

## GO

- RapidOCR consumer 重建 reference-only；`provider=rapidocr_candidate`；`empty_text=true` 允许。
- stub vs RapidOCR comparison 完整；无融合、无事实写入；verifier = **GO**。

## NO_GO

- 融合/解释空文本/写事实/导航/AI/重新调用 OCR；audit 缺失。
