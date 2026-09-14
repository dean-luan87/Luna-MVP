# Luna — OCR Semantic Candidate Generator DryRun v0

**Phase**：`Phase-OCR-Semantic-Candidate-Generator-DryRun-001`

## 目的

基于 **OCRTextEvidencePack v0** 生成 **OCRSemanticCandidate** dry-run（规则/启发式），不运行 LLM/VLM/语义大模型。

## 原则

- `raw_ocr_text` 为证据，**不可覆盖**
- semantic candidate 为 `not_fact` / `write_allowed=false`
- RealVideo `empty_text` → `unknown_text_or_unreadable`，**不得**当 `no_text_fact`
- Poster non-empty → `poster_promo_text` / `price_discount_text` / `temporal_notice_text`（仍 not_fact）
- completion/correction 仅 candidate，不提交

## 实现

- Capability：`capabilities/midplatform/ocr_semantic_candidate_generator_dryrun_v0.py`
- Runner：`tools/evaluation/midplatform/run_ocr_semantic_candidate_generator_dryrun_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_ocr_semantic_candidate_generator_dryrun_v0.py`

## 前置

- [LUNA_OCR_EVIDENCE_PACK_ADAPTER_UPDATE_V0.md](./LUNA_OCR_EVIDENCE_PACK_ADAPTER_UPDATE_V0.md)

## 评测

[LUNA_EVALUATION_OCR_SEMANTIC_CANDIDATE_GENERATOR_DRYRUN_V0.md](../evaluation/LUNA_EVALUATION_OCR_SEMANTIC_CANDIDATE_GENERATOR_DRYRUN_V0.md)

## 建议下一跳

**Mixed Video + Poster Batch Smoke**（见 [LUNA_CROSS_MODAL_VISION_OCR_MIXED_VIDEO_POSTER_BATCH_SMOKE_V0.md](./LUNA_CROSS_MODAL_VISION_OCR_MIXED_VIDEO_POSTER_BATCH_SMOKE_V0.md)）或 **WorldModel Attach Candidate dry-run**。
