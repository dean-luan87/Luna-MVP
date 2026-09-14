# Luna — OCR Poster Region OCR Plan Stub v0

**Phase**：`Phase-OCR-Poster-Region-OCR-Plan-Stub-001`

## 目的

在 Poster Layout Governance 之上，为 **4 个 text regions** 生成区域 OCR 计划 stub（provider class、priority、timeout、risk、TTL）。**不运行 OCR。**

## 原则

- `full_image_ocr_allowed=false`；logo/qr/product/background 排除
- `expected_output=layout_text_evidence_candidate`；`fact_status=not_fact`
- `force_semantic_join_allowed=false`

## 评测

[LUNA_EVALUATION_OCR_POSTER_REGION_OCR_PLAN_STUB_V0.md](../evaluation/LUNA_EVALUATION_OCR_POSTER_REGION_OCR_PLAN_STUB_V0.md)

## 下一跳

**Phase-OCR-Poster-VisualSymbolEvidence-Stub-001** — 见 [LUNA_OCR_POSTER_VISUAL_SYMBOL_EVIDENCE_STUB_V0.md](./LUNA_OCR_POSTER_VISUAL_SYMBOL_EVIDENCE_STUB_V0.md)

## 建议下一跳

**Phase-Poster-Real-OCR-Gated-Execution-001** — 见 [LUNA_POSTER_REAL_OCR_GATED_EXECUTION_V0.md](./LUNA_POSTER_REAL_OCR_GATED_EXECUTION_V0.md)
