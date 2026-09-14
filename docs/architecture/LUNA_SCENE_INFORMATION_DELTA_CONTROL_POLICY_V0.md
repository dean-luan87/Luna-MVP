# LUNA — Scene Information Delta Control Policy v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-001**

## Contract name

- `SceneInformationDeltaControl`

## Schema（合同字段）

```json
{
  "delta_control_id": "scene_delta_001",
  "current_evidence_id": "ocr_evidence_001",
  "previous_result_ref": null,

  "crop_signature": "...",
  "text_signature": "...",
  "layout_signature": "...",
  "object_signature": "...",

  "comparison_window_ms": 3000,

  "delta_status": "new | unchanged | changed | uncertain | duplicate | expired",
  "delta_decision": "reuse_previous | ignore_duplicate | partial_update | full_reprocess | hold_uncertain",

  "change_summary": {
    "text_changed": false,
    "layout_changed": false,
    "crop_shift_ratio": 0.0,
    "confidence_delta": 0.0,
    "line_order_changed": false
  },
  "reason": "..."
}
```

## Delta decision rules（冻结逻辑）

1) `unchanged`
- 条件：
  - `text_signature` 相同
  - `layout_signature` 相同（或变化低于阈值）
  - `crop_shift_ratio < 0.1`
- 动作：
  - `delta_decision = reuse_previous`
  - 不重复提炼（保持复用占位）

2) `duplicate`
- 条件：
  - 同一窗口内存在多个 evidence，`text_signature` 相同
- 动作：
  - `delta_decision = ignore_duplicate`

3) `changed`
- 条件：
  - `text_signature` 不同
- 动作：
  - `delta_decision = partial_update` 或 `full_reprocess`（由后续 text extraction scope 决定）

4) `layout_changed_text_same`
- 条件：
  - `text_signature` 相同
  - `layout_signature` 变化
- 动作：
  - `delta_decision = partial_update`

5) `uncertain`
- 条件：
  - OCR confidence 低
  - `line_order_status` 为 `uncertain`
  - `reading_direction_candidate` 为 unknown 且文本较长
- 动作：
  - `delta_decision = hold_uncertain`
  - 不进入 task-relevant extraction

6) `expired`
- 条件：
  - 超出 `comparison_window_ms` 或上一 evidence 证据窗口不可复用
- 动作：
  - `delta_decision = full_reprocess`

## Reason / audit requirement

- `reason` 必须解释 delta 状态为何成立（用于后续审计复盘）。
- 本阶段只定义 delta control，不实现 runtime 调用链。

