# Luna Evaluation — OCR Provider Governance Standard v0（Phase-OCR-Provider-Runtime-Governance-Standard-001）

## 定位

本组文档与 **静态 verifier** 用于确认：**Multi-OCR Provider Dispatch & Runtime Governance Standard v0**（OCR Provider Runtime Governance Standard v0）已在仓库内 **文档化、可索引、可静态验收**，含 **OCRRequest / OCRDispatchDecision、OCR Orchestrator、禁止业务直连 provider** 等闸门字段；且与 **evaluation 边界**（不跑 OCR、不改 routing）一致。

## 与 architecture/ocr 的关系

- **规范正文与拆分**：`docs/architecture/ocr/LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md` 及同目录配套文档。  
- **本 evaluation 文档**：面向 **Phase 闸门与 CI 静态检查** 的入口说明。

## 工具

```text
python3 tools/evaluation/ocr/verify_ocr_provider_runtime_governance_standard_v0.py \
  --repo-root <ABS_Luna-Core> \
  [--output-root <ABS_OUT>]
```

默认 **`--output-root`**：`<repo-root>/_eval_out/ocr_provider_governance_standard_v0`（若不可写可显式传入可写目录）。

## 产物

- `ocr_provider_governance_standard_summary.json`  
- `ocr_provider_governance_standard_policy_matrix.json`  
- `ocr_provider_governance_standard_verifier_report.json`  
