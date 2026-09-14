# LUNA Evaluation — PaddleOCR Labeled Set Batch Recovery GO / NO-GO Pack v0（Phase-PaddleOCR-Labeled-Set-Stability-Recovery-001）

## GO

- **full manifest** 被拆批 **完整跑完**（`completed_batch_count == batch_count`，`failed_batch_count == 0`）。  
- **merged_sample_count_present == merged_sample_count_expected** 且 **expected ≥ 20**。  
- **merged ground_truth_coverage ≥ 0.8**（与 manifest 一致口径）。  
- **所有 batch `exit_code=0` 且无 signal**（子进程未遭信号终止）。  
- **merged metrics** 与 **crash_report 为空列表**（无崩溃条目）。  
- **merged audit** 无越界 true 标志；`production_quality_deemed_pass` 仍为 false。  
- **`batch_recovery_verdict=GO`** 且 **verifier `verdict=GO`**。

## CONDITIONAL_GO

- **部分 batch 崩溃**但 **crash_report / results_matrix** 记录完整（含 `exit_code`、`last_sample_id`、`stderr_tail`、`crash_sample_candidates`）。  
- 或 **merge 未覆盖全部样本**但原因可解释且 **无伪造**（summary 中 `missing_sample_ids` 非空等）。  
- 或 **样本数 / GT 覆盖** 仍不满足严格 GO 但符合 smoke / 部分集语义。  
- **无**审计越界。

## NO_GO

- **无法生成 batch plan**（manifest 非法或空）。  
- **崩溃但未记录** `exit_code` / `last_sample_id`（矩阵或 crash 条目缺失关键字段）。  
- **审计越界**（网络、改 cache、routing、RapidOCR、MidPlatform、世界模型等任一为 true）。  
- **summary 宣称 GO** 但与上述客观字段矛盾（verifier 会判 **NO_GO**）。

**说明**：本 phase GO **只表示** 在本机/本配置下 **全量拆批稳定性跑通与产物可合并**；**不**表示 PaddleOCR 可作为默认 runtime provider，也 **不**替代 **OCR Provider Runtime Governance** 的准入流程。
