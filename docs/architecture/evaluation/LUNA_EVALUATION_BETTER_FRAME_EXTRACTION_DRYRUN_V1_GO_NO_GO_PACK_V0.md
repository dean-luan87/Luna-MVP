# Luna — Better Frame Extraction DryRun v1 GO/NO_GO Pack v0

## GO

- tight / wide window 均 intake；candidate frame refs > 0
- frame artifact generated/deferred/failed 记录完整；生成文件路径真实
- 不 OCR / 不 crop；same-frame blocker 未解除；`boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- 视频缺失导致 artifact deferred；refs 仍生成；无越界行为

## NO_GO

- OCR / crop / OCRRequest / SV rerun / 解除 blocker / 写 fact / WM / SceneDelta
- benchmark claim / 改 routing / audit 缺失
