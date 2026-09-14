# LUNA Evaluation — OCR Bridge Evidence Pack Consumer Static Test v0（Phase-OCR-Bridge-Evidence-Pack-Consumer-Static-Test-001）

## 定位

在 **OCR-Bridge-Evidence-Pack-Alignment-001 = GO** 的前提下，对 **`ocr_bridge_evidence_pack_candidate_v0.json`** 做 **consumer 侧静态契约测试**：使用既有 **`validate_ocr_evidence_pack_v0`** 完成加载级校验，并 **逐项遍历 `eligible_text_evidence`**，验证 **text / confidence / bbox / polygon / score / reading_order_index**、**`uncertainty.paddleocr_confidence_summary`**、**`paddleocr_source_reference_chain`**、**`evaluation_flags` / `hard_audit`** 可被静态读取且 **不触发** runtime / MidPlatform / routing 语义。

**只做**：读 candidate、validator 静态校验、字段访问矩阵、provisional 容忍策略说明、审计回显、报告与 verifier。

**不做**：PaddleOCR / OCR 推理、RapidOCR 替换、routing 变更、runtime / 白盒 / MidPlatform、世界模型、中台语义、真实业务消费、benchmark。

## 前置

- **`bridge_alignment_output_root`**：`ocr_bridge_evidence_pack_alignment_summary.json` 中 **`bridge_pack_verdict == GO`**，且 **`ocr_bridge_evidence_pack_verifier_report.json`** 中 **`verdict == GO`**。

## 工具

```text
python3 tools/evaluation/ocr/test_ocr_bridge_evidence_pack_consumer_static_v0.py \
  --bridge-alignment-root <ABS_BRIDGE_ALIGNMENT_OUT> \
  [--output-root <ABS_CONSUMER_STATIC_OUT>]
```

默认 **`--output-root`**：`<bridge-alignment-root>/ocr_bridge_pack_consumer_static_v0`。

```text
python3 tools/evaluation/ocr/verify_ocr_bridge_evidence_pack_consumer_static_v0.py \
  --consumer-static-root <ABS_CONSUMER_STATIC_OUT>
```

## Contract loader

- **`capabilities.ocr_bridge.ocr_evidence_pack_validator_v0.validate_ocr_evidence_pack_v0`**（设计期静态校验；`non_ocr_types=∅`）。  
- 骨架参照：**`build_ocr_evidence_pack_skeleton_v0`**（用于记录相对骨架的顶层扩展键，**不**作为运行时 parser）。

## 产物

- `ocr_bridge_pack_consumer_static_summary.json`  
- `ocr_bridge_pack_consumer_static_field_access_matrix.json`  
- `ocr_bridge_pack_consumer_static_item_walk_report.json`  
- `ocr_bridge_pack_consumer_static_provisional_field_report.json`  
- `ocr_bridge_pack_consumer_static_source_chain_report.json`  
- `ocr_bridge_pack_consumer_static_audit_report.json`  
- `ocr_bridge_pack_consumer_static_notes.md`  
- `ocr_bridge_pack_consumer_static_verifier_report.json`（由 verifier 写入）
