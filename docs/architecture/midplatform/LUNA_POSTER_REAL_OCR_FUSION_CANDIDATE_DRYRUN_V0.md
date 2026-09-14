# Luna — Poster Real OCR Fusion Candidate DryRun v0

**Phase**：`Phase-Poster-Real-OCR-Fusion-Candidate-DryRun-001`

## 目的

基于 Poster real OCR reference closure，生成 **Poster OCR × layout region** 的 **fusion candidate dry-run**。`fusion_candidate_generated=true`，但 `fusion_committed=false`，不写事实层。

## 原则

- fusion candidate 仅为候选，不是 fusion fact
- visual symbols 仅作 context，不当普通 OCR 文本
- `reading_order_confidence=low` 不强行跨区 semantic join
- price/promo/time 保留 TTL risk
- 全部 `fact_status=not_fact`；`requires_review=true`

## 实现

- Capability：`capabilities/midplatform/poster_real_ocr_fusion_candidate_dryrun_v0.py`
- Runner：`tools/evaluation/midplatform/run_poster_real_ocr_fusion_candidate_dryrun_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_poster_real_ocr_fusion_candidate_dryrun_v0.py`

## 评测

[LUNA_EVALUATION_POSTER_REAL_OCR_FUSION_CANDIDATE_DRYRUN_V0.md](../evaluation/LUNA_EVALUATION_POSTER_REAL_OCR_FUSION_CANDIDATE_DRYRUN_V0.md)

## 建议下一跳

**Poster-Real-OCR-Fusion-Review-Queue-001** — 见 [LUNA_POSTER_REAL_OCR_FUSION_REVIEW_QUEUE_V0.md](./LUNA_POSTER_REAL_OCR_FUSION_REVIEW_QUEUE_V0.md)
