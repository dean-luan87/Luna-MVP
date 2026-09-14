# LUNA OCR Bridge — Distortion Prevention → Contract Mapping v0 (Phase-OCRBridge-Design-001)

将 Evaluation Tools OCR-007 的 **失真防控规则** 映射到 **OcrEvidencePack** 合同字段与校验器行为：

| OCR-007 / 设计原则 | 合同落点 |
|--------------------|----------|
| non-OCR 不进事实文本层 | `eligible_text_evidence[].source_refs.eval_content_type` + `should_enter_fact_text_layer`；校验器 **F** |
| symbol/glyph 不拼入 raw 事实 | `should_enter_raw_text=false`、`should_enter_fact_text_layer=false`；校验器 **G** |
| reading_order 不确定 → 无唯一全局事实 | `reading_order.reading_order_uncertain=true` 时 **`fact_text_layer_candidates` 为空**（build 默认）；校验器 **H** |
| multi_panel 不跨 panel 当全局事实 | `multi_panel_layout` 不得出现在 eligible；校验器 **I** |
| 低质量需不确定性 | NO_GO 不得出现在 eligible；CONDITIONAL_GO 与 pack 级 `uncertainty`；校验器 **J** |
