# Luna — Poster Real OCR Reference Update v0

**Phase**：`Phase-Poster-Real-OCR-Reference-Update-001`

## 目的

将 Poster original reference-only、Poster real OCR readonly consumer、VisualSymbolEvidence stub **并列更新**为新的 Poster Real OCR Reference 索引。**不重新运行 OCR**，**不 fusion**。

## 原则

- 保留 `original_text_plan_refs`（4 条 plan lineage）
- 新增 `real_ocr_text_evidence_refs`（4 条候选证据）
- 保留 `visual_symbol_refs`（4 条 visual track）
- text / visual track 分离；`fusion_status=not_fused`
- 全部 `fact_status=not_fact`；`write_allowed=false`

## 实现

- Capability：`capabilities/midplatform/poster_real_ocr_reference_update_v0.py`
- Runner：`tools/evaluation/midplatform/run_poster_real_ocr_reference_update_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_poster_real_ocr_reference_update_v0.py`

## 评测

[LUNA_EVALUATION_POSTER_REAL_OCR_REFERENCE_UPDATE_V0.md](../evaluation/LUNA_EVALUATION_POSTER_REAL_OCR_REFERENCE_UPDATE_V0.md)

## 建议下一跳

**Phase-Poster-Real-OCR-Reference-Closure-001** — 见 [LUNA_POSTER_REAL_OCR_REFERENCE_CLOSURE_V0.md](./LUNA_POSTER_REAL_OCR_REFERENCE_CLOSURE_V0.md)
