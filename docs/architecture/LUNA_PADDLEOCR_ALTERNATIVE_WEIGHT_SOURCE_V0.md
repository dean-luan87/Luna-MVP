# LUNA — PaddleOCR Alternative Weight Source v0

## Phase

- **Phase-ModelOCR-003-Fix-003** — *PaddleOCR Alternative Weight Source Acquisition v0*

## 目标

在默认 Paddle 模型托管不可达时，通过**替代来源**获取 **det/rec/cls（可为 optional）** 的 Paddle 推理资产（`inference.pdmodel` + `inference.pdiparams` 同目录），随后：

1. 固定到 `models/ocr/paddleocr_ppocrv5/{det,rec,cls}`  
2. 生成 `model_files_manifest_v0.json`（file-level sha256/size + provenance）  
3. 更新 `paddleocr_ppocrv5_model_manifest_v0.json`  
4. 重跑 `tools/check_ocr_model_readiness_v0.py`  

**禁止**：运行时依赖自动下载；禁止在本阶段跑 OCR 推理 / benchmark；禁止接 runtime / YOLO / 中台 / 语义层。

## 允许的来源类型（`--source-type`）

| 类型 | 说明 |
|------|------|
| `local_dir` | 用户已下载好的目录（最稳） |
| `manual_url` / `gitee` | 显式 HTTP(S) URL（压缩包或已解压目录的上级路径） |
| `huggingface` | `--hf-det-repo` / `--hf-rec-repo`（需 `huggingface_hub`）或直接 `--det-url`/`--rec-url` 指向 HF `resolve` 链接 |
| `official` | 扫描本地缓存 + 可选 init-only（仍禁止 OCR 推理） |

## 工具

- **获取**：`tools/acquire_paddleocr_weights_v0.py`  
  - 默认 `--allow-download false`  
  - 仅 `--allow-download true` 时联网下载  
  - 成功后默认 `--invoke-prepare true` 调用 `prepare`  
  - 可选 `--run-readiness true` 调用 readiness  

- **固定**：`tools/prepare_paddleocr_pinned_weights_v0.py`  
  - **永不下载**（若传入 `--allow-download true` 会直接退出提示先用 acquire）  
  - 支持子树内查找 inference 目录；支持 `--det-source-url` 等按 role 写入 manifest  

## Provenance

每条下载须在 acquisition log 的 `downloads[]` 中记录 `source_url`、`sha256`、`file_size_bytes`。  
`prepare` 可将 `--det-source-url` / `--rec-source-url` / `--cls-source-url` 写入 file-manifest 的 `source_url_or_cache`（按 role）。

## 校验

解压或本地目录须能在某子目录找到 **同一文件夹内** 同时存在的：

- `inference.pdmodel`  
- `inference.pdiparams`  

可选：`inference.yml`、`inference.pdiparams.info`（不作为硬门禁，但建议在矩阵中记录是否存在）。
