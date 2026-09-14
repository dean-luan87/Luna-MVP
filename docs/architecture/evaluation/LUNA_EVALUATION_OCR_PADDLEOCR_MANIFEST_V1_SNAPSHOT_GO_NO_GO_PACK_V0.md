# LUNA Evaluation — PaddleOCR Manifest v1 Snapshot GO / NO-GO Pack v0（Phase-PaddleOCR-ManifestV1-Snapshot-001）

## GO

- v1 manifest **可读**且 **策略字段**满足（`runtime_default_enabled` / `mainline_provider` / `network_required` / `download_authorized` 为 false，`evaluation_candidate` 为 true）。  
- det / rec / cls **全部解析成功**且路径存在（文件或非空目录），**`missing_refs` 为空**，**`pinning_complete=true`**，sha256 矩阵完整（无 cap 截断未完成 pin）。  
- **`verify_paddleocr_manifest_v1_snapshot_v0.py` verdict GO**。  
- **`constraints`**：无下载、无构造、无推理、无 routing 变更。

## CONDITIONAL_GO

- manifest 与策略 **合法**，但 **缓存未齐**（占位符、路径不存在、空目录、或目录文件数超 cap 导致 sha 不完整）。  
- **`pinning_complete=false`**，`missing_cache_report` **完整**；**verifier 仍可通过**（若结构自洽：`verdict=CONDITIONAL_GO` 且 `missing_refs` 非空时不得标 GO）。

## NO_GO

- manifest **不可读**或 **必填键缺失**或 **策略布尔错误**。  
- **伪造**存在或 **伪造** sha256（本工具链仅对已存在文件计算 hash）。  
- **`verdict=GO`** 但 **`missing_refs` 非空** 或 **`pinning_complete=false`**（逻辑矛盾）。  
- **调用** `PaddleOCR()`、**运行** OCR、**下载**模型、**改** OCR routing。

## 与下游 phase

Snapshot **GO** 后再进入 **受控 trial / prepare 缓存**；仅为 **CONDITIONAL_GO** 时，应先 **准备离线缓存** 或 **更新 manifest 占位符为真实路径**，再重跑 snapshot。
