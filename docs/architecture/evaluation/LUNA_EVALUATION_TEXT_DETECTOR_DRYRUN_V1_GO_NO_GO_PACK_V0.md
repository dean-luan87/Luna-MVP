# Text Detector DryRun v1 GO/NO_GO Pack v0

## GO

- 30 crop + 6 frame intake；text-like candidate + bbox adjustment candidate 输出
- supervision 缺失时 heuristic fallback 完整；无 OCR / OCRRequest / EP / Semantic / SV

## NO_GO

- 运行 OCR；把 candidate 当 OCR text 或事实；写 WM/SceneDelta；改 routing
