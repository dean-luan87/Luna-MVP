# LUNA Evaluation — PaddleOCR Manifest v1 Snapshot v0（Phase-PaddleOCR-ManifestV1-Snapshot-001）

## 目标

在 **不下载、不 `PaddleOCR()`、不 OCR、不改 routing、不替换 RapidOCR** 的前提下，读取 **v1 example manifest**，解析 **`model_root` / det/rec/cls `*_model_ref`**，在 **`--repo-root`** 与可选 **`--cache-root`** 下探测路径，生成 **cache 矩阵**、**缺失报告**、**已存在文件的 sha256** 与 **pinned manifest candidate**。

## 输入

- **Manifest（默认）**：`configs/models/ocr/paddleocr_current_api_model_manifest_v1.example.json`（`--manifest` 可改为 repo 内相对路径）。  
- **`--cache-root`**（可选）：例如 `~/LunaRuntime/models/ocr/paddleocr_current_api_v1`；**不存在不判 NO_GO**，仅影响解析候选路径。

## 工具

```text
python3 tools/evaluation/ocr/run_paddleocr_manifest_v1_snapshot_v0.py \
  --repo-root <ABS_LUNA_CORE> \
  --manifest configs/models/ocr/paddleocr_current_api_model_manifest_v1.example.json \
  [--cache-root <ABS_CACHE>] \
  [--output-root <ABS_DIR>]

python3 tools/evaluation/ocr/verify_paddleocr_manifest_v1_snapshot_v0.py \
  --repo-root <ABS_LUNA_CORE> \
  --snapshot-root <上一步 output_root>
```

## 产出（`output_root`）

| 文件 | 作用 |
|------|------|
| `paddleocr_manifest_v1_snapshot_summary.json` | `verdict`、`pinning_complete`、`constraints`、`model_root_probe`。 |
| `paddleocr_manifest_v1_field_matrix.json` | 必填字段存在性检查。 |
| `paddleocr_manifest_v1_model_cache_matrix.json` | det/rec/cls 解析路径、存在性、目录文件数。 |
| `paddleocr_manifest_v1_sha256_matrix.json` | 逐文件 sha256 列表。 |
| `paddleocr_manifest_v1_missing_cache_report.json` | 占位符 / 未找到 / 空目录 / cap 截断等事件。 |
| `paddleocr_manifest_v1_pinned_manifest_candidate.json` | 原 manifest + `resolved_model_refs`、`sha256_by_file`、`missing_refs`、`pinning_complete`。 |
| `paddleocr_manifest_v1_snapshot_notes.md` | 人类可读摘要。 |

## 结论口径

- **GO**：三 ref 均可解析且存在、目录非空或文件存在、**无** `missing_refs`、**`pinning_complete=true`**、manifest 策略字段合法。  
- **CONDITIONAL_GO**：manifest 可读且策略合法，但缓存缺失 / 占位符 / 空目录 / sha 截断等导致 **`pinning_complete=false`**。  
- **NO_GO**：manifest 不可读、**必填字段或策略布尔**不满足（如 `runtime_default_enabled!=false`）；**不得**伪造 sha256。
