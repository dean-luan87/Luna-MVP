# LUNA OCR Bridge — Evidence Types v0 (Phase-OCRBridge-Design-001)

## 类型一览

| 类型 | Python 文档 | 用途 |
|------|-------------|------|
| EligibleTextEvidenceV0 | `capabilities/ocr_bridge/ocr_evidence_types_v0.py` | A 类合理域；**唯一**允许 `should_enter_fact_text_layer=true`（仍受 reading_order / 校验器约束） |
| ConditionalTextEvidenceV0 | 同上 | B 类条件域；必须 `should_enter_fact_text_layer=false`；携带 preprocess / layout / fallback 语义 |
| SymbolEvidenceV0 | 同上 | 符号/图标证据；`should_enter_raw_text=false` |
| GlyphEvidenceV0 | 同上 | 字形/艺术字；`ocr_confirmed` 默认 false |
| LayoutEvidenceV0 | 同上 | 版面组；允许 `group_raw_text_joined` **仅作为组内结构化字段**，不等于 MidPlatform 全局 raw 拼接输入 |
| RejectedOrUncertainEvidenceV0 | 同上 | 拒识/不确定 |

## `source_refs`

每条 evidence 携带 `source_refs`（`source_image_ref`、`provider_ref`、`quality_gate_ref`、`layout_ref`、`eligibility_gate_ref`、`routing_ref` 等）。Evaluation 映射会附加 `eval_*` 字段便于审计。
