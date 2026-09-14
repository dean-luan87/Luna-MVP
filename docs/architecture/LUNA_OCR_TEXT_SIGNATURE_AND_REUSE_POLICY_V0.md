# LUNA — OCR Text Signature & Reuse Policy v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-001**

## Signature rules（冻结生成规则）

### `crop_signature`
- hash 输入：
  - `crop_region`（坐标空间/归一化参数）
  - `source_object_class`（来自 YOLO / bridge attribution）
  - `source_detection_id`（可选但推荐）
- 目的：
  - 判断是否同一区域的 evidence 复用。

### `text_signature`
- hash 输入：
  - `normalized_raw_text`（从 `raw_text_candidates` 推导）
  - `line_order`（来自 evidence：`line_order_status` / line_order）
- 目的：
  - 判断“文字是否变化”。

### `layout_signature`
- hash 输入：
  - block bbox / line count（可选结构化摘要）
  - `raw_text_joined_strategy`
  - `reading_direction_candidate`
- 目的：
  - 判断版面/阅读顺序是否变化。

### `object_signature`
- hash 输入：
  - `yolo_class`
  - bbox quantized（用于抗小抖动）
  - `frame_id` / `source_frame_window_id`
- 目的：
  - 判断同一视觉对象窗口是否变化。

## Reuse decision policy（复用决策冻结）

可选决策：`reuse_previous | ignore_duplicate | partial_update | full_reprocess | hold_uncertain`

1) `unchanged`
- 条件：
  - `text_signature` 相同
  - `layout_signature` 相同或变化低于阈值
  - `crop_shift_ratio < 0.1`
- 动作：
  - `reuse_previous`
  - 不重复提炼（保持复用占位）

2) `duplicate`
- 条件：
  - 同一窗口多个 evidence 的 `text_signature` 相同
- 动作：
  - `ignore_duplicate`

3) `changed`
- 条件：
  - `text_signature` 不同
- 动作：
  - `partial_update` 或 `full_reprocess`

4) `layout_changed_text_same`
- 条件：
  - `text_signature` 相同
  - `layout_signature` 变化
- 动作：
  - `partial_update`

5) `uncertain`
- 条件：
  - OCR confidence 低
  - `line_order_status=uncertain`
  - `reading_direction_candidate=unknown` 且文本较长
- 动作：
  - `hold_uncertain`
  - 不进入 task-relevant extraction

6) `task_context_changed`（占位）
- 条件：
  - 任务目标/上下文变化
- 动作：
  - 即使文本未变，允许重新评估 relevance（仍不触发 runtime）

## Audit requirement（冻结审计）

- hash 输入必须记录 source fields（不可只记录 hash 值本身）。
- 本阶段不实现 runtime；只定义复用与签名规则。

