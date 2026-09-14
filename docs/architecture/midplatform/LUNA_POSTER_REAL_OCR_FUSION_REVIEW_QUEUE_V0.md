# Luna — Poster Real OCR Fusion Review Queue v0

**Phase**：`Phase-Poster-Real-OCR-Fusion-Review-Queue-001`

## 目的

将 Poster real OCR **fusion candidate dry-run** 产物放入 **review queue**。`review_status=pending_review`，`approval_status=not_approved`。**不批准、不自动批准**。

## 原则

- review queue ≠ approval；pending_review ≠ 事实
- 继承 commercial/temporal/TTL、reading_order、brand/QR 未确认状态
- `fusion_committed=false`；`scene_delta_candidate_generated=false`
- 全部 `fact_status=not_fact`；`write_allowed=false`

## 实现

- Capability：`capabilities/midplatform/poster_real_ocr_fusion_review_queue_v0.py`
- Runner：`tools/evaluation/midplatform/run_poster_real_ocr_fusion_review_queue_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_poster_real_ocr_fusion_review_queue_v0.py`

## 评测

[LUNA_EVALUATION_POSTER_REAL_OCR_FUSION_REVIEW_QUEUE_V0.md](../evaluation/LUNA_EVALUATION_POSTER_REAL_OCR_FUSION_REVIEW_QUEUE_V0.md)

## 建议下一跳

**Poster-Real-OCR-Fusion-TTL-Gate-DryRun-001** — 见 [LUNA_POSTER_REAL_OCR_FUSION_TTL_GATE_DRYRUN_V0.md](./LUNA_POSTER_REAL_OCR_FUSION_TTL_GATE_DRYRUN_V0.md)

**Poster-Real-OCR-Fusion-Policy-Gate-DryRun-001**（TTL 之后）
