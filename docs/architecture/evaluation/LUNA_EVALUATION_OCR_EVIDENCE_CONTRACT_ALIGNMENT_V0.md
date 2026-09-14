# LUNA Evaluation — OCR Evidence Contract Alignment v0（Phase-OCR-Evidence-Contract-Alignment-001）

## 定位

在 **PaddleOCR-API-Adapter-Contract-001 = GO** 的前提下，将 **`paddleocr_api_adapter_normalized_result.json`** 映射为 **统一 OCR evidence contract v0**（`ocr_evidence_unified_result_v0` 文档结构）。

**只做**：字段治理、**source_reference_chain**、**confidence_summary**、**reading_order_candidate**（provider 顺序）、**layout_assumption**（显式未做版面治理）、审计与 verifier。

**不做**：主线接入、RapidOCR 替换、OCR routing 变更、runtime / 白盒 / MidPlatform、中台语义、批量质量评测、provider 切换。

## 前置

- **adapter_contract_root**：`paddleocr_api_adapter_contract_summary.json` 中 **`adapter_contract_verdict == GO`**。  
- **materialize_root**、**pinned manifest** 与 adapter 输入一致，用于 **来源链**。

## 工具

```text
python3 tools/evaluation/ocr/align_paddleocr_normalized_to_ocr_evidence_v0.py \
  --repo-root <ABS_Luna-Core> \
  --adapter-contract-root <ABS_ADAPTER_ROOT> \
  --materialize-root <ABS_MATERIALIZE_ROOT> \
  --pinned-manifest <ABS_PINNED_JSON> \
  [--output-root <ABS_ALIGNMENT_OUT>]
```

```text
python3 tools/evaluation/ocr/verify_ocr_evidence_contract_alignment_v0.py \
  --alignment-root <ABS_ALIGNMENT_OUT> \
  [--adapter-contract-root <ABS_ADAPTER_ROOT>]
```

## 产物

`ocr_evidence_*` JSON、`ocr_evidence_alignment_notes.md`、**`ocr_evidence_alignment_verifier_report.json`**。
