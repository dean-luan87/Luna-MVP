# Luna — Poster Real OCR Gated Execution v0

**Phase**：`Phase-Poster-Real-OCR-Gated-Execution-001`

## 目的

在 **Poster Region OCR Plan** 门控下，对 **4 个 text regions**（`title_area`、`body_text_area`、`price_or_promo_area`、`time_location_area`）执行 **gated real OCR smoke**（优先 RapidOCR lightweight，经 `ocr_mainline_bridge_v0`）。输出 `layout_text_evidence_candidate`，**不写事实层**。

## 原则

- `full_image_ocr_allowed=false`；`segment_first_required=true`
- 仅 OCR text regions；排除 logo / QR / product / background
- 不解码 QR；不确认品牌；不调用 VisualSymbolRegistry
- 不做 semantic join / fusion；`reading_order_confidence=low`
- price / promo / time 文本带 TTL required risk
- `fact_status=not_fact`；`write_allowed=false`；`runtime_routing_changed=false`
- RapidOCR 不可用 → **CONDITIONAL_GO**（记录 `provider_unavailable`）；**禁止 MOCK_TEXT 冒充 real OCR**

## 实现

- Capability：`capabilities/ocr_runtime/poster_real_ocr_gated_execution_v0.py`
- Runner：`tools/evaluation/ocr/run_poster_real_ocr_gated_execution_v0.py`
- Verifier：`tools/evaluation/ocr/verify_poster_real_ocr_gated_execution_v0.py`

## 评测

[LUNA_EVALUATION_POSTER_REAL_OCR_GATED_EXECUTION_V0.md](../evaluation/LUNA_EVALUATION_POSTER_REAL_OCR_GATED_EXECUTION_V0.md)

## 建议下一跳

**Phase-Poster-Real-OCR-ReadOnly-Consumer-001** — 见 [LUNA_POSTER_REAL_OCR_READONLY_CONSUMER_V0.md](./LUNA_POSTER_REAL_OCR_READONLY_CONSUMER_V0.md)
