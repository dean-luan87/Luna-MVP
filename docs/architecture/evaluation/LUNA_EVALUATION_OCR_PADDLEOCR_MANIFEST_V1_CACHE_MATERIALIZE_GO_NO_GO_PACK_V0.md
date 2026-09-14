# LUNA Evaluation — PaddleOCR Manifest v1 Cache Materialize GO / NO-GO Pack v0（Phase-PaddleOCR-ManifestV1-CacheMaterialize-001）

## GO

- **`materialize_verdict == GO`**（与 **`completion_verdict == GO`** 对齐）。  
- **`snapshot_summary_verdict == GO`**，**`pinning_complete == true`**，**`missing_ref_count == 0`**，**`sha256_by_file` 非空**（以 snapshot pinned 为准）。  
- **Snapshot verifier**、**Materialize verifier** 均为 **GO**（后者在 summary 已为 GO 时做矛盾检测）。  
- **constraints**：无构造、无推理、无 routing 变更、无 RapidOCR 替换。

## CONDITIONAL_GO

- 模型**未**完全落盘或目录仍空 → **completion CONDITIONAL_GO** → **materialize CONDITIONAL_GO**。  
- **Materialize verifier** 输出 **CONDITIONAL_GO**（结构正常、summary 未宣称端到端 GO）。

## NO_GO

- **未授权下载**却声称已完成物料化。  
- **伪造**存在、**伪造 sha256**、**空目录 `pinning_complete=true`**。  
- **summary 宣称 GO** 但与 **pinning / missing / sha** 矛盾。  
- **`PaddleOCR()`**、**OCR**、**替换 RapidOCR**、**改 routing**。

## 推荐顺序（人工 + 编排）

1. 取得官方模型（**手动**或 **`--allow-download` + 已填 URL**）。  
2. 运行 **`run_paddleocr_manifest_v1_cache_materialize_v0.py`**。  
3. 运行 **`verify_paddleocr_manifest_v1_cache_materialize_v0.py`**。  
4. 仅当 **GO** 后，再排 **Controlled-Trial-001**。
