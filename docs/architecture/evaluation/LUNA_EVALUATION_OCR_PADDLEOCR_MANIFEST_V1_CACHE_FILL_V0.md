# LUNA Evaluation — PaddleOCR Manifest v1 Cache Fill v0（Phase-PaddleOCR-ManifestV1-CacheFill-001）

## 目标

在 **不 `PaddleOCR()`、不 OCR、不改 routing** 的前提下：

1. 读取 **CachePrepare-001** 的 `prepare_root` 与 **candidate manifest**。  
2. **探测 / 可选拷贝 / 可选授权下载** 至 **`model_root`/det/rec/cls**。  
3. 产出 **fill 报告** 后，**重跑** `run_paddleocr_manifest_v1_snapshot_v0.py` + `verify_paddleocr_manifest_v1_snapshot_v0.py`。  
4. 使用 **`verify_paddleocr_manifest_v1_cache_fill_completion_v0.py`** 做 **聚合验收**。

## 边界

- **默认不下载**；仅 **`--allow-download` + 已填 URL 的 manifest** 才走 HTTPS。  
- **不**实例化 PaddleOCR、**不**推理、**不**替换 RapidOCR、**不**进主线 / 白盒 / MidPlatform。

## 工具

### Cache fill

```text
python3 tools/evaluation/ocr/fill_paddleocr_manifest_v1_cache_v0.py \
  --repo-root <ABS_LUNA_CORE> \
  --prepare-root <ABS_PREPARE_OUT> \
  [--copy-from <ABS_LOCAL_TREE>] \
  [--allow-download --download-url-manifest <ABS_URL_JSON>] \
  [--output-root <ABS_DIR>]
```

### Snapshot（candidate 常为绝对路径）

```text
python3 tools/evaluation/ocr/run_paddleocr_manifest_v1_snapshot_v0.py \
  --repo-root <ABS_LUNA_CORE> \
  --manifest <ABS_OR_REL_PATH_TO_candidate.json> \
  [--output-root <ABS_DIR>]

python3 tools/evaluation/ocr/verify_paddleocr_manifest_v1_snapshot_v0.py \
  --repo-root <ABS_LUNA_CORE> \
  --snapshot-root <SNAP_OUT>
```

### Completion

```text
python3 tools/evaluation/ocr/verify_paddleocr_manifest_v1_cache_fill_completion_v0.py \
  --repo-root <ABS_LUNA_CORE> \
  --prepare-root <ABS_PREPARE_OUT> \
  --fill-root <ABS_FILL_OUT> \
  --snapshot-root <ABS_SNAP_OUT>
```

## 产出（fill `output_root`）

| 文件 | 作用 |
|------|------|
| `paddleocr_manifest_v1_cache_fill_summary.json` | `cache_fill_verdict`、`constraints`、`next_manual_actions`。 |
| `paddleocr_manifest_v1_cache_fill_file_matrix.json` | det/rec/cls 目录存在性与文件数。 |
| `paddleocr_manifest_v1_cache_fill_missing_report.json` | 缺失或空目录。 |
| `paddleocr_manifest_v1_cache_fill_download_report.json` | 下载/拷贝审计（未授权则 `network_request_invoked=false`）。 |
| `paddleocr_manifest_v1_cache_fill_notes.md` | 人类可读摘要。 |

## 结论关系

- **缓存未齐**：fill 与 snapshot 多为 **CONDITIONAL_GO**；**completion CONDITIONAL_GO**（无伪造）。  
- **缓存齐 + snapshot GO + verifier GO**：**completion GO**（见 GO pack）。
