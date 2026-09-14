# LUNA Evaluation — OCR Real-World Sample Manifest Schema v0

## `manifest.jsonl`（每行一条 JSON）

| 字段 | 说明 |
|------|------|
| `sample_id` | `rw_000001` 格式 |
| `image_path` | 相对数据集根的 `images/...` |
| `annotation_path` | `annotations/<id>.annotation.json` |
| `content_type` | OCR-006 taxonomy 之一 |
| `sample_source` | `manual_import` \| `user_fixture` \| `captured_frame` \| `public_reference` \| **`placeholder`** |
| `language` | `zh` \| `en` \| `mixed` \| `none` \| `unknown` |
| `has_ground_truth` | 占位条目为 **false** |
| `ground_truth_quality` | 占位为 **`not_applicable`** 或 `missing` |
| `expected_route` | 与类型相关的建议路由（非强制 runtime） |
| `should_enter_fact_text_layer` | RealSamples-001 固定 **false** |
| `sha256` / `width` / `height` | 文件指纹与尺寸 |

## 与 OCR-006-RealEval 的关系

本 manifest + `ocr_realworld_dataset_registry.json` 作为后续 **RealEval** 的注册输入；**不**自动触发评测。
