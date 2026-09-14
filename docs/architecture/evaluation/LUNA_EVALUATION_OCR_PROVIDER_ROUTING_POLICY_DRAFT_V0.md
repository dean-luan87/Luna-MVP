# LUNA Evaluation Tools — OCR Provider Routing Policy Draft v0 (Phase-EvaluationTools-OCR-006)

## Purpose

这是 **Evaluation Tools 内部** 的 routing policy draft，用于把“哪类内容适合哪个 OCR 方案”写成可审查的草案：

- RapidOCR 作为 baseline/primary 的适用范围
- PaddleOCR/CnOCR/OCR-VL 的候选范围（本阶段不执行 PaddleOCR trial）
- layout/symbol/glyph 分支优先的内容类型
- low_quality/manual_review 的分流建议

## Hard boundary

- 本草案不得自动影响主线 provider routing
- 主线若引用，必须经过人工评审并重新冻结为 runtime 合同

## Implementation ref

`capabilities/evaluation/ocr/ocr_capability_boundary_router_policy_v0.py`

