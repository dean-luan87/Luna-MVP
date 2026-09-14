# LUNA Evaluation — PaddleOCR Labeled Set Evaluation GO / NO-GO Pack v0（Phase-PaddleOCR-Labeled-Set-Evaluation-001）

## GO（评测闸门成立，≠ 生产质量达标）

- **Materialize = GO**；**pinned** 可读。  
- **20 ≤ sample_count ≤ 50**。  
- **ground_truth_coverage ≥ 0.8**（以 manifest 中非空 `ground_truth_text` 计）。  
- **全样本 predict 成功**；**raw / normalized / evidence / category_report / review_queue** 等产物齐全。  
- **`category_undercovered` 为空**（规范类别中已出现者每类 **≥3** 张）。  
- **审计**：无网络、无改 cache、无 routing / RapidOCR / runtime / 白盒 / MidPlatform / 世界模型 / 中台语义。  
- **`production_quality_deemed_pass` 在 v0 中必须为 false**。  
- **`labeled_set_verdict=GO`** 且 **verifier `verdict=GO`**。

## CONDITIONAL_GO

- 评测跑完且产物基本齐全，但 **样本数不在 20–50**、或 **GT 覆盖 <0.8**、或 **部分 predict 失败**（错误报告完整）、或 **`category_undercovered` 非空**。  
- **无**审计越界。

## 冻结结论归档（与治理 phase 分离）

当本 phase 在 **全量正式 manifest（如 20 张）** 上因 **SIGSEGV / exit 139** 等 **未完成全量跑通**，而 **smoke（如 3 张）** 仍为 **CONDITIONAL_GO** 时，**不得**与 **OCR-Provider-Runtime-Governance-Standard-001 = GO** 混写为同一 verdict。权威叙述见：  
`LUNA_EVALUATION_PHASE_ARCHIVE_PADDLEOCR_LABELED_SET_EVALUATION_001_V0.md`。  
后续稳定性收束见：**Phase-PaddleOCR-Labeled-Set-Stability-Recovery-001**（`LUNA_EVALUATION_OCR_PADDLEOCR_LABELED_SET_BATCH_RECOVERY_V0.md`）。

## NO_GO

- **Materialize 非 GO** 或 **pinned 不可读**。  
- **sample_count = 0** 或 **>50**。  
- **关键产物缺失**；**审计越界**（网络、改 cache、routing、RapidOCR、runtime、MidPlatform 等）。  
- **宣称生产质量通过**（`production_quality_deemed_pass=true`）或 **summary 标 GO 但与闸门矛盾**。  
- **无 GT 却宣称质量通过**（由 `production_quality_deemed_pass` 与覆盖字段约束）。
