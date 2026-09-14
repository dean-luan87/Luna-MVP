# LUNA Evaluation — OCR Bridge Evidence Pack Alignment v0（Phase-OCR-Bridge-Evidence-Pack-Alignment-001）

## 定位

在 **OCR-Evidence-Contract-Alignment-001 = GO** 的前提下，将 **`ocr_evidence_unified_result_v0.json`**（及对齐阶段附属 JSON）映射为 **OcrEvidencePackV0 形态的 evaluation-only candidate**，并与既有 **`LUNA_OCR_EVIDENCE_PACK_CONTRACT_V0`**（文档 + `ocr_evidence_pack_contract_v0.py` 骨架）做 **字段级 diff** 与 **mapping matrix**。

**只做**：字段 diff、schema mapping、candidate 生成、**source_reference_chain** 保留、审计、verifier、**migration notes**。

**不做**：PaddleOCR 执行、OCR 推理、RapidOCR 替换、routing 变更、runtime / 白盒 / MidPlatform、世界模型写入、中台语义、provider 切换、质量 benchmark。

## 前置

- **`evidence_alignment_root`**：`ocr_evidence_alignment_summary.json` 中 **`alignment_verdict == GO`**。  
- 建议链上仍含 **adapter_contract_root**、**materialize_root**、**pinned_manifest_path**（由上游 alignment 写入 `ocr_evidence_source_reference_chain.json`）。

## 既有 Bridge contract 参照

若仓库内同时存在：

- `docs/architecture/ocr_bridge/LUNA_OCR_EVIDENCE_PACK_CONTRACT_V0.md`  
- `capabilities/ocr_bridge/ocr_evidence_pack_contract_v0.py`  

则 **`contract_reference_found=true`**，align summary 方可 **GO**（在其余条件满足时）。任一缺失则 summary / verifier 为 **CONDITIONAL_GO**（`missing_contract_reference`），**不得**宣称 **GO**。

## 工具

```text
python3 tools/evaluation/ocr/align_ocr_evidence_to_bridge_pack_v0.py \
  --repo-root <ABS_Luna-Core> \
  --evidence-alignment-root <ABS_EVIDENCE_ALIGNMENT_ROOT> \
  [--output-root <ABS_BRIDGE_ALIGNMENT_OUT>]
```

```text
python3 tools/evaluation/ocr/verify_ocr_bridge_evidence_pack_alignment_v0.py \
  --bridge-alignment-root <ABS_BRIDGE_ALIGNMENT_OUT>
```

## 产物

- `ocr_bridge_evidence_pack_alignment_summary.json`  
- `ocr_bridge_evidence_pack_candidate_v0.json`  
- `ocr_bridge_evidence_pack_field_diff.json`  
- `ocr_bridge_evidence_pack_mapping_matrix.json`  
- `ocr_bridge_evidence_pack_source_reference_chain.json`  
- `ocr_bridge_evidence_pack_migration_notes.md`  
- `ocr_bridge_evidence_pack_audit_report.json`  
- `ocr_bridge_evidence_pack_verifier_report.json`  

## Candidate 标注

每个 pack 含 **`evaluation_flags`**：`evaluation_only`、`not_runtime_input`、`not_midplatform_input`，以及 **`api_family` / `call_method`**。超出骨架的 PaddleOCR 专用字段（如 **`polygon`**、**`score`**、**`reading_order_index`**、`paddleocr_source_reference_chain`）在 summary 的 **`provisional_fields`** 中列出，供后续 schema migration 收敛。
