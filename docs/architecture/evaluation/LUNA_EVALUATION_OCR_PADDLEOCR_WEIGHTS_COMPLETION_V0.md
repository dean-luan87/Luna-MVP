# LUNA Evaluation — PaddleOCR Weights Completion v0（Phase-PaddleOCR-Weights-003）

## 目标

将 **Weights-001 snapshot** 从 **CONDITIONAL_GO** 推进到 **GO**：六份 **det/rec/cls** 的 `inference.pdmodel` + `inference.pdiparams` 在 **manifest 规划路径** 落盘，**sha256 全量 pin**，**pinned manifest candidate** 完整，**`verify_paddleocr_weights_snapshot_v0` GO**。

## 边界

- **不**运行 PaddleOCR OCR、**不** `PaddleOCR()`、**不**替换 RapidOCR、**不**进主线 / 白盒 / MidPlatform、**不**改 OCR routing。  
- **不**把 PaddleOCR 设为默认 provider。

## 输入（仓库内）

- `configs/models/ocr/paddleocr_evaluation_readiness_manifest_v0.json`  
- `configs/models/ocr/paddleocr_ppocrv5_model_files_manifest_v0.json`  
- `configs/models/ocr/paddleocr_evaluation_weight_download_urls_v0.example.json`（下载时填 URL 后另存为实际 manifest）

## 获取权重（仍用 Weights-002 工具）

- **A 本地拷贝**：`prepare_paddleocr_evaluation_weights_v0.py --copy-from <绝对路径> ...`  
- **B 授权下载**：`--allow-download --download-url-manifest <已填 URL 的 JSON>`  
- **C 未授权**：仅 missing 报告，**不得**伪造成功。

## Snapshot 与聚合验收

```text
run_paddleocr_weights_snapshot_v0.py
verify_paddleocr_weights_snapshot_v0.py
verify_paddleocr_weights_completion_v0.py --snapshot-root <snapshot 输出目录>
```
