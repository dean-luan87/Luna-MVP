# LUNA Evaluation — STCM Cross-Contract Field Alignment GO / NO-GO Pack v0（Phase-STCM-Contract-Field-Alignment-001）

## GO

- **STCM 四文档 + STCM example config** 存在。  
- **OCR 治理主文 + OCR governance example config** 存在。  
- **OcrEvidencePack 合同 md + `ocr_evidence_pack_contract_v0.py`** 存在。  
- **`LUNA_STCM_CROSS_CONTRACT_FIELD_ALIGNMENT_V0.md`** 含 **五段强制映射标题**（OCRRequest、Dispatch、EvidencePack、Voice、Vision）。  
- **`stcm_cross_contract_field_alignment_v0.example.json`** 结构完整（`mappings`、`known_gaps`、`known_conflicts`）。  
- **Voice / Vision 主引用文件**在仓库内 **可解析存在**（非伪造路径）。  
- **verifier `verdict = GO`**。

## CONDITIONAL_GO

- **OCR + OcrEvidencePack** 对齐完整；**Voice 或 Vision** 部分二级引用缺失，但 **`stcm_missing_contract_reference_report.json` 记录完整**、无伪造路径。  
- **gap** 仅为 **low/medium** 设计缺口（如 pack 顶层缺 `observed_at`），无原则冲突。

## NO_GO

- **STCM 或 OCR 治理主文档缺失**；**对齐主文档缺失**；**example json 缺失或 schema 错误**。  
- **未显式列出 OCRRequest → ModelCallDeadline** 等强制章节。  
- **缺 gap / conflict 报告**（verifier 未产出）。  
- **伪造不存在的 Voice/Vision 合同路径**；或 **README 无本 phase 索引**。  
- **宣称已接 runtime / 改 routing**（与 phase 边界矛盾）。
