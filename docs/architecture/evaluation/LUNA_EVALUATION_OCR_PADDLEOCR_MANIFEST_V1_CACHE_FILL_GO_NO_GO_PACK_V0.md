# LUNA Evaluation — PaddleOCR Manifest v1 Cache Fill GO / NO-GO Pack v0（Phase-PaddleOCR-ManifestV1-CacheFill-001）

## GO（端到端）

- **模型缓存已落盘**（det/rec/cls 非空），**`run_paddleocr_manifest_v1_snapshot_v0`** 输出 **`verdict: GO`**。  
- **`pinning_complete: true`**，**`missing_ref_count = 0`**，**`sha256_by_file` 非空**。  
- **`verify_paddleocr_manifest_v1_snapshot_v0` verdict GO**。  
- **`verify_paddleocr_manifest_v1_cache_fill_completion_v0` completion_verdict GO**。  
- **constraints**：无构造、无推理、无 routing 变更、无未授权下载（若未授权则 `network_download_invoked=false`）。

## CONDITIONAL_GO

- **缓存未齐**或 **snapshot 仍为 CONDITIONAL_GO**；**missing 报告完整**；**不伪造** pinning / sha。  
- **completion CONDITIONAL_GO**：聚合器记录 blockers（如 `snapshot_verdict_not_go`）。

## NO_GO

- **未授权下载**却 **`network_request_invoked=true`**（与审计策略冲突时由后续 phase 细化；本工具仅记录 fill report）。  
- **逻辑矛盾**：`snapshot_verdict == GO` 但 **`pinning_complete` false**、**`missing_refs` 非空**、或 **sha 为空**。  
- **`PaddleOCR()`**、**OCR 推理**、**替换 RapidOCR**、**修改 OCR routing**。  
- **伪造**缓存或 sha256。

## 推荐顺序

1. `prepare_paddleocr_manifest_v1_cache_plan_v0.py`（已完成则复用 `prepare_root`）  
2. `fill_paddleocr_manifest_v1_cache_v0.py`（手动或授权拷贝/下载）  
3. `run_paddleocr_manifest_v1_snapshot_v0.py` + `verify_paddleocr_manifest_v1_snapshot_v0.py`  
4. `verify_paddleocr_manifest_v1_cache_fill_completion_v0.py`
