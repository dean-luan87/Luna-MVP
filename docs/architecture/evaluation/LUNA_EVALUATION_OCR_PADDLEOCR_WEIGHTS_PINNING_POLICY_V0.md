# LUNA Evaluation — PaddleOCR Weights Pinning Policy v0

## 路径约定（repo 根相对）

- `models/ocr/paddleocr_ppocrv5/det/`  
- `models/ocr/paddleocr_ppocrv5/rec/`  
- `models/ocr/paddleocr_ppocrv5/cls/`  

每目录至少：`inference.pdmodel` + `inference.pdiparams`（与 `paddleocr_ppocrv5_model_files_manifest_v0.json` 一致）。

## Pinning 流程

1. **Weights-002**：拷贝或授权下载落盘。  
2. **Weights-001**：`run_paddleocr_weights_snapshot_v0.py` 计算 **sha256**，生成 **pinned manifest candidate**。  
3. `verify_paddleocr_weights_snapshot_v0.py`：**verifier GO** 且 `missing_count=0`。

## 禁止

- **未授权**自动联网拉取。  
- 在 **sha256 未齐** 前进入 **Controlled Trial** 或 **RapidOCR vs PaddleOCR A/B**。  
- 将 PaddleOCR 设为 **主线默认** provider。
