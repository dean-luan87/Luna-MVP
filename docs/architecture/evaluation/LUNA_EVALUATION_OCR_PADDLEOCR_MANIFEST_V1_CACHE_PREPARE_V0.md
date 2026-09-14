# LUNA Evaluation — PaddleOCR Manifest v1 Cache Prepare v0（Phase-PaddleOCR-ManifestV1-CachePrepare-001）

## 目标

在 **不下载、不 `PaddleOCR()`、不 OCR、不改 routing** 的前提下，将 **v1 example manifest** 推进为 **concrete manifest candidate**（真实 `model_root` + `det/rec/cls` ref），并输出 **预期目录矩阵**、**manual acquisition plan**、**URL 模板指针**（仓库内模板，**URL 为空**）。

## 冻结事实

- **ManifestV1-Design-001** = GO  
- **ManifestV1-Snapshot-001** = CONDITIONAL_GO（example 仍为 placeholder）  
- **legacy 六文件链**不作为当前优先路线；本 phase 专注 **current API 离线缓存布局与 manifest 草案**。

## 工具

```text
python3 tools/evaluation/ocr/prepare_paddleocr_manifest_v1_cache_plan_v0.py \
  --repo-root <ABS_LUNA_CORE> \
  --manifest configs/models/ocr/paddleocr_current_api_model_manifest_v1.example.json \
  --model-root /Users/luanlei/LunaRuntime/models/ocr/paddleocr_current_api_v1 \
  [--det-ref det] [--rec-ref rec] [--cls-ref cls] \
  [--output-root <ABS_DIR>]

python3 tools/evaluation/ocr/verify_paddleocr_manifest_v1_cache_prepare_v0.py \
  --repo-root <ABS_LUNA_CORE> \
  --prepare-root <上一步 output_root>
```

## 产出（`output_root`）

| 文件 | 作用 |
|------|------|
| `paddleocr_manifest_v1_cache_prepare_summary.json` | 摘要、`constraints`、`prepare_verdict`。 |
| `paddleocr_current_api_model_manifest_v1.candidate.json` | **Concrete** manifest 草案（**不**含真实 sha pin）。 |
| `paddleocr_manifest_v1_cache_acquisition_plan.json` | 目标根目录、refs、预期目录、手工步骤；**`download_completed=false`**。 |
| `paddleocr_manifest_v1_expected_directory_matrix.json` | det/rec/cls 与 `model_root` 路径表。 |
| `paddleocr_manifest_v1_manual_copy_instructions.md` | `mkdir` / 拷贝说明。 |
| `paddleocr_manifest_v1_cache_prepare_notes.md` | 人类可读边界说明。 |

## URL 模板（仓库，不下载）

`configs/models/ocr/paddleocr_current_api_model_download_urls_v1.example.json`：`entries[].url` 为 **null**，仅作后续授权下载 phase 的模板。

## 验收

见 `LUNA_EVALUATION_OCR_PADDLEOCR_MANIFEST_V1_CACHE_PREPARE_GO_NO_GO_PACK_V0.md` 与 `verify_paddleocr_manifest_v1_cache_prepare_v0.py`。
