# LUNA Evaluation — PaddleOCR Weights Acquisition v0（Phase-PaddleOCR-Weights-002）

## 目的

在 **用户明确授权** 的前提下，通过 **本地拷贝（`--copy-from`）** 或 **HTTPS 下载（`--allow-download` + URL manifest）** 将 PP-OCRv5 **det / rec / cls** 的 `inference.pdmodel` / `inference.pdiparams` 放入仓库规划路径；随后应重跑 **Weights-001 snapshot** 以生成 sha256 与 pinned candidate。

## 工具

- `tools/evaluation/ocr/prepare_paddleocr_evaluation_weights_v0.py`

## 默认行为

- **不联网**、**不** `PaddleOCR()`、**不** OCR 推理。  
- 输出 **manual acquisition plan**、`download_report`（`download_authorized=false` 时无请求）、**file matrix**（before/after）。

## 授权下载

- 必须同时传入 **`--allow-download`** 与 **`--download-url-manifest <path>`**（JSON 内每条 `url` 非空）。  
- `paddleocr_weights_download_report.json` 记录：`download_authorized`、`download_source`、`download_time`、`files_downloaded`、`network_request_invoked`。

## URL 清单模板

`configs/models/ocr/paddleocr_evaluation_weight_download_urls_v0.example.json`
