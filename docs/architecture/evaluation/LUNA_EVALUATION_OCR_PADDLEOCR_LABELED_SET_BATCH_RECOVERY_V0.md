# LUNA Evaluation — PaddleOCR Labeled Set Batch Recovery v0（Phase-PaddleOCR-Labeled-Set-Stability-Recovery-001）

## Phase verdict（冻结语义）

**IMPLEMENTED / PENDING_RUN**：拆批 **runner**、**verifier**、文档与索引已入库；**未**在 CI/代理环境实跑 PaddleOCR。**须本机**执行 `run_paddleocr_labeled_set_batch_recovery_v0.py` 并生成 `paddleocr_labeled_set_batch_recovery_summary.json` + `verify_...` 报告后，方可将本 phase 标为 **GO / CONDITIONAL_GO / NO_GO**。

- **STCM 设计线**：**STCM-001 / Alignment / Event-Skeleton** 均已 **GO**（design-only）；**当前阶段不再扩展 STCM 文档层**，优先收口 **PaddleOCR batch recovery 本机实跑**。

## 定位

在 **Materialize = GO** 与 **pinned manifest** 不变前提下，将 **PaddleOCR labeled set 全量评测** 从「单进程长跑易 SIGSEGV / exit 139」拆为 **可配置 batch_size、每 batch 独立子进程、独立 output_root、可 resume、可合并指标与崩溃审计** 的 **evaluation-only** 稳定性恢复路径。

**只做**：拆批、子进程隔离、崩溃字段记录、合并 raw/normalized/evidence/质量与运行时指标、resume 状态、报告与 verifier。

**不做**：runtime shadow wiring、改 routing、替换 RapidOCR、进入 MidPlatform / 白盒、写世界模型、改 model cache、无边界联网（子 runner 继承既有网络探针约束）。

## 前置

- **PaddleOCR-Labeled-Set-Evaluation-001**：允许为 **CONDITIONAL_GO**（见独立归档 `LUNA_EVALUATION_PHASE_ARCHIVE_PADDLEOCR_LABELED_SET_EVALUATION_001_V0.md`）。  
- **OCR-Provider-Runtime-Governance-Standard-001 = GO** 与本 phase **正交**（见 `LUNA_EVALUATION_PHASE_ARCHIVE_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_001_V0.md`）。

## 输入

- **full manifest**：`configs/evaluation/ocr/paddleocr_labeled_set_manifest_v0.example.json`  
- **smoke manifest**：`configs/evaluation/ocr/paddleocr_labeled_set_manifest_v0.smoke.json`（小样本；用于烟测拆批行为）  
- **materialize_root**：须含 `paddleocr_manifest_v1_cache_materialize_summary.json` 且 `materialize_verdict=GO`（示例路径由执行环境给出，如用户日志下的 materialize 目录）。

## 建议本机执行顺序（收口 verdict）

1. **`--batch-size 5`** 先跑全量 manifest。  
2. 若仍 **exit 139 / SIGSEGV**，改 **`--batch-size 1`** 缩小崩溃面。  
3. 用 **`paddleocr_labeled_set_batch_crash_report.json`** 与 **`batch_results_matrix`** 定位 **crash batch / crash_sample_candidates**。  
4. 查看 **`paddleocr_labeled_set_batch_merged_*`** 与 per-batch stderr 片段。  
5. 运行 **`verify_paddleocr_labeled_set_batch_recovery_v0.py`**，将 **`batch_recovery_verdict`** 与 verifier 对齐为 **GO / CONDITIONAL_GO / NO_GO**。

## 工具

```text
python3 tools/evaluation/ocr/run_paddleocr_labeled_set_batch_recovery_v0.py \
  --repo-root <ABS_Luna-Core> \
  --materialize-root <ABS_MATERIALIZE_ROOT> \
  --pinned-manifest <ABS_PINNED_JSON> \
  --labeled-set-manifest <ABS_FULL_OR_SMOKE_MANIFEST> \
  [--output-root <ABS_BATCH_RECOVERY_ROOT>] \
  [--batch-size 1|5|10|...] \
  [--resume] \
  [--batch-timeout-sec 7200] \
  [--no-use-angle-cls]
```

```text
python3 tools/evaluation/ocr/verify_paddleocr_labeled_set_batch_recovery_v0.py \
  --batch-recovery-root <ABS_BATCH_RECOVERY_ROOT>
```

## 产物（batch_recovery_root 下）

- `paddleocr_labeled_set_batch_recovery_summary.json`  
- `paddleocr_labeled_set_batch_plan.json`  
- `paddleocr_labeled_set_batch_results_matrix.json`（含 `exit_code` / `signal` / `last_sample_id` / `memory_peak_mb` / `batch_duration_ms` / `stderr_tail`）  
- `paddleocr_labeled_set_batch_crash_report.json`（`crash_sample_candidates`、SIGSEGV 前后可审计字段）  
- `paddleocr_labeled_set_batch_merged_quality_metrics.json`  
- `paddleocr_labeled_set_batch_merged_runtime_metrics.json`（含 `memory_peak_by_batch`）  
- `paddleocr_labeled_set_batch_resume_state.json`  
- `paddleocr_labeled_set_batch_audit_report.json`（各成功子 batch 审计字段聚合）  
- `paddleocr_labeled_set_batch_recovery_notes.md`  
- `paddleocr_labeled_set_batch_recovery_verifier_report.json`（verifier 写入）

每批子目录：`batches/batch_XXX/manifest_slice.json` + 该批 **完整** labeled-set runner 产物（与单跑一致）。

## 总状态表

见 `LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md`。
