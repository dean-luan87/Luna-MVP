# Luna — OCR Evidence Pack Adapter Update v0

**Phase**：`Phase-OCR-Evidence-Pack-Adapter-Update-001`

## 目的

将既有 **Poster（4）** 与 **RealVideo（10）** OCR evidence 适配为统一 **OCRTextEvidencePack v0**，仅做 adapter / schema alignment / reference mapping。

## 原则

- adapter 只封装已有 evidence，**不修改** raw OCR（`raw_ocr_text`、`text_items`、`empty_text` 原样保留）
- 原 `source_chain` 保留并追加 `ocr_evidence_pack_adapter_update`
- 坐标/时空/可读性字段齐全；缺失显式 `null`，**不得伪造**
- `evidence_status` 默认 `not_fact` / `write_allowed=false`
- `semantic_candidate` / `world_model_attach_candidate` 仅 placeholder ref，不运行模型、不写 WM
- `empty_text` 不得解释为 `no_text_fact`

## 实现

- Capability：`capabilities/midplatform/ocr_evidence_pack_adapter_update_v0.py`
- Runner：`tools/evaluation/midplatform/run_ocr_evidence_pack_adapter_update_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_ocr_evidence_pack_adapter_update_v0.py`

## 前置合同

[LUNA_OCR_EVIDENCE_PACK_SPATIOTEMPORAL_SEMANTIC_CONTRACT_V0.md](./LUNA_OCR_EVIDENCE_PACK_SPATIOTEMPORAL_SEMANTIC_CONTRACT_V0.md)

## 评测

[LUNA_EVALUATION_OCR_EVIDENCE_PACK_ADAPTER_UPDATE_V0.md](../evaluation/LUNA_EVALUATION_OCR_EVIDENCE_PACK_ADAPTER_UPDATE_V0.md)

## 建议下一跳

**Phase-OCR-Semantic-Candidate-Generator-DryRun-001**（见 [LUNA_OCR_SEMANTIC_CANDIDATE_GENERATOR_DRYRUN_V0.md](./LUNA_OCR_SEMANTIC_CANDIDATE_GENERATOR_DRYRUN_V0.md)）完成后 → **WorldModel Attach Candidate dry-run**。
