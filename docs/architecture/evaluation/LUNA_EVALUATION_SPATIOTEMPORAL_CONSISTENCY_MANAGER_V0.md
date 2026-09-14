# LUNA Evaluation — Spatiotemporal Consistency Manager v0（Phase-Spatiotemporal-Consistency-Manager-001）

## 定位

本组文档与 **静态 verifier** 用于确认：**Time-Space Consistency & Model Call Governance v0**（**时空间一致性管理器 / STCM**）已在仓库内 **文档化、可索引、可静态验收**，且与 **OCR Provider Runtime Governance** 的边界说明一致。

**只做**：架构规范、合同字段、governance 文档、**example JSON**、**静态 verifier**。

**不做**：运行 OCR / 视觉 / 语音模型；接主线；改 routing；实装 MidPlatform runtime；写世界模型；中台语义解释；provider 切换；benchmark。

## 与 OCR 治理的关系

- **OCR Provider Runtime Governance**：**哪个 OCR**、**OCRRequest / OCRDispatchDecision**、Bridge 与证据。  
- **STCM**：**是否仍来得及、结果是否仍时空有效、超时后如何处理、是否允许进入任务链与语音**。  
- **OCR Orchestrator** 裁定执行计划时 **必须查询 STCM**（见主架构文档）。

## 工具

```text
python3 tools/evaluation/midplatform/verify_spatiotemporal_consistency_manager_v0.py \
  --repo-root <ABS_Luna-Core> \
  [--output-root <ABS_OUT>]
```

默认 **`--output-root`**：`<repo-root>/_eval_out/spatiotemporal_consistency_manager_v0`。

## 后续（合同对齐）

- **Phase-STCM-Contract-Field-Alignment-001**：`LUNA_EVALUATION_STCM_CROSS_CONTRACT_FIELD_ALIGNMENT_V0.md`（与 OCRRequest / EvidencePack / Voice / Vision 字段级对齐，防 STCM 孤立）。

## 产物

- `spatiotemporal_consistency_manager_summary.json`  
- `spatiotemporal_consistency_manager_policy_matrix.json`  
- `spatiotemporal_consistency_manager_verifier_report.json`
