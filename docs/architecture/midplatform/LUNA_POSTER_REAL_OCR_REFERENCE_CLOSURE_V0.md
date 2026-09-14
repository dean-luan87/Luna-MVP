# Luna — Poster Real OCR Reference Closure v0

**Phase**：`Phase-Poster-Real-OCR-Reference-Closure-001`

## 目的

对 Poster real OCR reference 链做**只读 closure**：聚合并验证从 layout governance → region OCR plan → visual symbol → original reference → real OCR execution → readonly consumer → reference update 的完整 lineage。**不新增能力**，不重新 OCR。

## 原则

- `poster_real_ocr_reference_status=closed_for_reference_evaluation`
- 保留 plan / real OCR / visual 三轨分离
- 全部 `fact_status=not_fact`；`write_allowed=false`
- 不 fusion、不 benchmark、不改 routing

## 实现

- Capability：`capabilities/midplatform/poster_real_ocr_reference_closure_v0.py`
- Runner：`tools/evaluation/midplatform/run_poster_real_ocr_reference_closure_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_poster_real_ocr_reference_closure_v0.py`

## 评测

[LUNA_EVALUATION_POSTER_REAL_OCR_REFERENCE_CLOSURE_V0.md](../evaluation/LUNA_EVALUATION_POSTER_REAL_OCR_REFERENCE_CLOSURE_V0.md)

## 建议下一跳

**Phase-Poster-Real-OCR-Fusion-Candidate-DryRun-001** — 见 [LUNA_POSTER_REAL_OCR_FUSION_CANDIDATE_DRYRUN_V0.md](./LUNA_POSTER_REAL_OCR_FUSION_CANDIDATE_DRYRUN_V0.md)
