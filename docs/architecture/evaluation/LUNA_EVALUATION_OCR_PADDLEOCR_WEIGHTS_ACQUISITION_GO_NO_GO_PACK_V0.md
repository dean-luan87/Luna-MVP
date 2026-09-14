# LUNA Evaluation — PaddleOCR Weights Acquisition Go/No-Go Pack v0

## GO

- 6 个计划文件均在 repo 内存在。  
- 重跑 Weights-001 snapshot 后 **`verdict: GO`**、`missing_count=0`、sha256 全齐。  
- `verify_paddleocr_weights_snapshot_v0` **GO**。  
- `constraints`：`paddleocr_constructor_invoked` / `paddleocr_inference_invoked` 为 **false**；`runtime_default_enabled` / `mainline_provider` 仍为 **false**。

## CONDITIONAL_GO

- 用户 **未授权下载** 或 URL 清单未填全 → 仅 **manual / copy** 计划与缺失报告（预期）。  
- `prepare` 的 **`verdict: CONDITIONAL_GO`** 且 **`missing_count_after > 0`**。

## NO_GO

- **未授权**却发起网络下载（无 `--allow-download` 或 URL 为空仍下载）。  
- 文件缺失却伪造 **已 pin** 或 **sha256**。  
- 调用 **PaddleOCR 推理**、**替换 RapidOCR**、**改主线 routing**、将 PaddleOCR 设为 **默认 provider**。
