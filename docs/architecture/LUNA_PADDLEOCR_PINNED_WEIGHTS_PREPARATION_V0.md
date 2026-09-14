# LUNA — PaddleOCR Pinned Local Weights Preparation v0

## Phase

- Phase: **Phase-ModelOCR-003-Fix**
- Scope: **PaddleOCR lightweight（ppocrv5 pipeline）权重固定为本地可复现资产**（det/rec/cls）

## Hard boundaries（强边界）

- 不进入 OCR runtime
- 不做 OCR 推理 / benchmark
- 不接 YOLO / 中台 / SceneTask / Fusion / Output
- 不做语义提炼；输出契约保持 raw-text only
- 默认不联网下载；只有在显式 `--allow-download true` 才允许下载（v0 未实现下载）

## Target directory layout（标准落盘）

目标目录（repo 内）：

- `models/ocr/paddleocr_ppocrv5/det/`
- `models/ocr/paddleocr_ppocrv5/rec/`
- `models/ocr/paddleocr_ppocrv5/cls/`
- `models/ocr/paddleocr_ppocrv5/model_files_manifest_v0.json`

其中 `model_files_manifest_v0.json` 记录 **file-level**：

- `relative_path`
- `sha256`
- `file_size_bytes`
- `role`: `det` | `rec` | `cls`
- `source_url_or_cache`
- `created_at`

## Tooling（v0）

### Prepare pinned weights tool

- Tool: `tools/prepare_paddleocr_pinned_weights_v0.py`
- 作用：
  - 从 **显式** `--source-root` 定位 det/rec/cls inference 目录（或用 `--det-source-dir/--rec-source-dir/--cls-source-dir` 指定）
  - 复制到 `models/ocr/paddleocr_ppocrv5/{det,rec,cls}`
  - 生成 `model_files_manifest_v0.json`
  - 更新 `configs/models/ocr/paddleocr_ppocrv5_model_manifest_v0.json`

建议用法：

```bash
python3 tools/prepare_paddleocr_pinned_weights_v0.py \
  --source-root "<paddleocr_model_cache_or_download_dir>" \
  --target-root "models/ocr/paddleocr_ppocrv5" \
  --manifest "configs/models/ocr/paddleocr_ppocrv5_model_manifest_v0.json" \
  --model-files-manifest "models/ocr/paddleocr_ppocrv5/model_files_manifest_v0.json" \
  --clean-target
```

如果 cls 暂缺但允许 pinned_partial：

```bash
python3 tools/prepare_paddleocr_pinned_weights_v0.py \
  --source-root "<paddleocr_model_cache_or_download_dir>" \
  --cls-optional \
  --clean-target
```

### Readiness checker

- Tool: `tools/check_ocr_model_readiness_v0.py`
- v0 扩展点（本阶段完成）：
  - 支持 `weights_source=pinned_partial`
  - 支持目录型权重 + `model_files_manifest_path` 校验
  - det/rec 必需；cls 可通过 `weights_policy.cls_optional=true` 显式标记为可选

## Manifest updates（目标字段）

目标 manifest（`configs/models/ocr/paddleocr_ppocrv5_model_manifest_v0.json`）更新点：

- `weights_source`: `pinned_local` 或 `pinned_partial`
- `weights_paths.*_model_path`: 指向 `models/ocr/paddleocr_ppocrv5/{det,rec,cls}`
- `model_files_manifest_path`: `models/ocr/paddleocr_ppocrv5/model_files_manifest_v0.json`
- `directory_hash_summary`: file-manifest 的聚合摘要（不伪造单文件 hash）
- `weights_policy.cls_optional`: `true/false`
- `raw_text_only=true` / `semantic_interpretation_enabled=false` / `allows_execute_now=false` / `real_tts_invoked=false`

## Acceptance outputs（验收输出）

本阶段验收应可产生：

- `models/ocr/paddleocr_ppocrv5/model_files_manifest_v0.json`
- 更新后的 `configs/models/ocr/paddleocr_ppocrv5_model_manifest_v0.json`
- readiness report（`logs/ocr_model_readiness_*.json`）

