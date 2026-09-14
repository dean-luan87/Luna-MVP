# Luna — ROI Crop v2 BBoxExpansion GO/NO_GO Pack v0

## GO

- 4 expansion candidates intake；4 expanded crops generated（或 defer 原因明确）
- source_bbox 保留；crop 文件存在；`new_ocr_invoked=false`；`boundary_ok=true`

## CONDITIONAL_GO

- 部分 crop deferred（frame 缺失等）；trace/defer 完整

## NO_GO

- 执行 OCR；生成 OCRRequest；覆盖 source bbox；写 fact/WM
