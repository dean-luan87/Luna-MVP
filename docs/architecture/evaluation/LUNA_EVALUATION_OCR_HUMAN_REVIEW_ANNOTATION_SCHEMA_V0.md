# LUNA Evaluation — OCR Human Review Annotation Schema v0（Real-World）

## 文件

- `annotations/<sample_id>.annotation.json`：逐图结构化模板（初值多为空数组 / `pending`）。  
- `human_review/review_annotations_template.json`：复核人填写总表。  
- `human_review/human_review_index.json`：样本索引与 `human_review_status`。

## `annotation.json` 核心块

- `visible_text_regions`：文本区域 + `reading_order_index` + `ground_truth_confidence`。  
- `visual_symbols` / `visual_glyphs`：符号 / 字形，`should_enter_raw_text` 默认 **false**。  
- `layout_groups`：版面组与 `reading_order`。  
- `expected_ocr_behavior`：**`global_raw_text_joined_allowed: false`**；`expected_route` 与 manifest 对齐。

## 状态

初值 **`human_review_status: pending`**；人工补全后再进入 RealEval。
