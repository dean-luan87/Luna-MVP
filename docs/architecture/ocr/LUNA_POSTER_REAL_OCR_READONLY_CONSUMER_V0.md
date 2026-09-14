# Luna — Poster Real OCR ReadOnly Consumer v0

**Phase**：`Phase-Poster-Real-OCR-ReadOnly-Consumer-001`

## 目的

只读消费 `Poster-Real-OCR-Gated-Execution-001` 产出的 `poster_layout_text_evidence_candidate.json`，构建 region consumer view、matrix、indexes、TTL/risk、metrics update candidate 与 audit。**不重新运行 OCR**。

## 原则

- 只读索引/归档/统计；不解释文本含义
- 不跨 region semantic join；`reading_order_confidence=low`
- price/promo/time 保留 TTL risk
- `fact_status=not_fact`；`write_allowed=false`
- 不消费 visual symbol 为 OCR 文本

## 实现

- Capability：`capabilities/ocr_runtime/poster_real_ocr_readonly_consumer_v0.py`
- Runner：`tools/evaluation/ocr/run_poster_real_ocr_readonly_consumer_v0.py`
- Verifier：`tools/evaluation/ocr/verify_poster_real_ocr_readonly_consumer_v0.py`

## 评测

[LUNA_EVALUATION_POSTER_REAL_OCR_READONLY_CONSUMER_V0.md](../evaluation/LUNA_EVALUATION_POSTER_REAL_OCR_READONLY_CONSUMER_V0.md)

## 建议下一跳

**Phase-Poster-Real-OCR-Reference-Update-001** — 见 [LUNA_POSTER_REAL_OCR_REFERENCE_UPDATE_V0.md](../midplatform/LUNA_POSTER_REAL_OCR_REFERENCE_UPDATE_V0.md)
