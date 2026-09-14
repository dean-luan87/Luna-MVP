# Multiframe Crop Execution DryRun GO/NO_GO Pack v0

## GO

- 30 projected regions intake；真实 PNG crop 生成
- OCR / OCRRequest / EP / Semantic / SV rerun 均未执行
- `detected_region=false`；`projection_not_detection=true`
- same-frame blocker 未解除；no-write boundary 通过

## CONDITIONAL_GO

- 部分 crop deferred/failed，总数与 intake 对齐

## NO_GO

- 执行 OCR 或生成 OCRRequest / EP / Semantic
- 解除 same-frame blocker 或写事实层
- mock crop 或宣称 independent consensus
