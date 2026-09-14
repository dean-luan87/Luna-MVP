# Luna — Text Region Tracklet DryRun v1 GO/NO_GO Pack v0

## GO

- 6 frame artifacts intake；≥1 tracklet candidate；projected region 明确非 detection
- continuity / drift / crop readiness 完整；无 detector/OCR/crop；blocker 未解除；`verifier=GO`

## CONDITIONAL_GO

- artifact 数非 6 但 projection-only 表达完整；无越界行为

## NO_GO

- detector/OCR/crop/OCRRequest/EP/Semantic/SV rerun；解除 blocker；写 fact/WM/SceneDelta；benchmark claim
