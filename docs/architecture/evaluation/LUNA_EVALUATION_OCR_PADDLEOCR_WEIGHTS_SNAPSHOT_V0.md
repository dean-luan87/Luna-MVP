# LUNA Evaluation — PaddleOCR Weights Snapshot & SHA256 Pin v0（Phase-PaddleOCR-Weights-001）

## 目的

在 **不下载**、**不** `PaddleOCR()`、**不** OCR 推理的前提下，对 `paddleocr_ppocrv5_model_files_manifest_v0.json` 列出的 **det / rec / cls** 权重文件做 **存在性扫描** 与 **SHA256 计算**，并生成 **pinned manifest candidate**。

## 工具

- `tools/evaluation/ocr/run_paddleocr_weights_snapshot_v0.py`  
- `tools/evaluation/ocr/verify_paddleocr_weights_snapshot_v0.py`

## 输入

- `configs/models/ocr/paddleocr_evaluation_readiness_manifest_v0.json`  
- `configs/models/ocr/paddleocr_ppocrv5_model_files_manifest_v0.json`

## 输出

默认：`~/LunaRuntime/logs/evaluation/paddleocr_weights_snapshot_001_<UTC>/`

## GO / CONDITIONAL

- **GO**：全部计划文件存在且 sha256 已写入 candidate。  
- **CONDITIONAL_GO**：缺失文件仅记录在 `paddleocr_model_missing_files_report.json`，等待 **授权下载/拷贝** 后再重跑。
