# LUNA Evaluation — STCM Cross-Contract Field Alignment v0（Phase-STCM-Contract-Field-Alignment-001）

## 前置状态（用户冻结）

- **OCR-Provider-Runtime-Governance-Standard-001** = GO  
- **Spatiotemporal-Consistency-Manager-001** = GO（verifier 输出目录示例：`/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/spatiotemporal_consistency_manager_v0`）  
- **PaddleOCR-Labeled-Set-Stability-Recovery-001** = **IMPLEMENTED / PENDING_RUN**（须本机实跑后定 verdict）

## 定位

**只做** `SpatiotemporalAnchor` / `ModelCallDeadline` / `ModelCallOutcome` / `InformationValueAssessment` 与 **OCRRequest**、**OCRDispatchDecision**、**OcrEvidencePack**、**Voice Output Governance**、**Vision 感知合同** 的 **字段级静态对齐**、缺口与冲突报告；**不**运行模型、**不**接 runtime、**不**改 OCR routing、**不**替换 RapidOCR、**不实装** MidPlatform、**不**写世界模型。

## 权威对齐正文

`docs/architecture/midplatform/LUNA_STCM_CROSS_CONTRACT_FIELD_ALIGNMENT_V0.md`

## 工具

```text
python3 tools/evaluation/midplatform/verify_stcm_cross_contract_field_alignment_v0.py \
  --repo-root <ABS_Luna-Core> \
  [--output-root <ABS_OUT>]
```

默认 **`--output-root`**：`<repo-root>/_eval_out/stcm_cross_contract_field_alignment_v0`。

## 后续（事件骨架）

- **Phase-STCM-Event-Skeleton-001**：`LUNA_EVALUATION_STCM_EVENT_SKELETON_V0.md`（STCM 事件类型与 trace contract，承接本对齐产物）。

## 产物

- `stcm_cross_contract_alignment_summary.json`  
- `stcm_cross_contract_field_matrix.json`  
- `stcm_missing_contract_reference_report.json`  
- `stcm_gap_report.json`  
- `stcm_conflict_report.json`  
- `stcm_alignment_notes.md`  
- `stcm_cross_contract_alignment_verifier_report.json`
