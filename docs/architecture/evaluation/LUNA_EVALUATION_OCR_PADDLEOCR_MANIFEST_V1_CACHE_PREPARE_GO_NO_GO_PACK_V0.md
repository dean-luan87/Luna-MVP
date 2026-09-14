# LUNA Evaluation — PaddleOCR Manifest v1 Cache Prepare GO / NO-GO Pack v0（Phase-PaddleOCR-ManifestV1-CachePrepare-001）

## GO

- **concrete candidate** 已生成：`model_root` 与 det/rec/cls **ref 均非占位**。  
- **acquisition plan**、**expected directory matrix**、**manual MD**、**notes** 齐全。  
- 仓库内 **URL 模板** `configs/models/ocr/paddleocr_current_api_model_download_urls_v1.example.json` 存在（**url 可为 null**）。  
- **`verify_paddleocr_manifest_v1_cache_prepare_v0.py` verdict GO**。  
- **constraints**：无下载、无构造、无推理、无 routing 变更。  
- **不得**在 candidate / acquisition 中标记 **`pinning_complete=true`**、**`download_completed=true`** 或填入 **伪造 sha256**。

## CONDITIONAL_GO（评审 / 环境）

- 官方目录命名仍待人工确认 → 仅调整 `--det-ref` 等并重跑 prepare；**不改变**本 phase 的「无下载」边界。  
- URL 模板中 **url 仍为空**：预期，直至单独授权下载 phase。

## NO_GO

- **执行下载**或声称 **`network_download_invoked`**。  
- **`PaddleOCR()`** 或 **OCR 推理**。  
- **替换 RapidOCR**、**将 PaddleOCR 设为默认**、**修改 OCR routing**。  
- candidate 中 **`pinning_complete=true`** 或 **`sha256_by_file` 非空**（本 phase 禁止假装已 pin）。  
- verifier 发现 **缺输出**、**策略布尔错误**、或 **URL 模板缺失**。

## 与 Snapshot-001 的关系

- **CachePrepare** 产出 **可执行的目录与 manifest 草案**；**Snapshot** 负责 **存在性 + sha + pinning_complete** 观测。二者 **不合并**为一步伪造 GO。
