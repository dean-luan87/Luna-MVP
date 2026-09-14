# LUNA — MidPlatform Text Extraction Candidate Contract v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-001**

## Candidate name

- `MidPlatformTextExtractionCandidate`

## Schema（合同字段）

```json
{
  "text_candidate_id": "mid_text_001",
  "source_evidence_id": "ocr_evidence_001",
  "delta_control_id": "scene_delta_001",

  "raw_text_ref": "...",
  "segment_refs": [],

  "extraction_scope": "raw_line | segment | layout_block | joined_preview",

  "text": "...",
  "confidence": 0.0,

  "task_relevance_status": "unknown | potentially_relevant | irrelevant | blocked",
  "reason_for_relevance": null,

  "semantic_summary": null,

  "navigation_action": null,

  "candidate_only": true,
  "requires_further_validation": true,
  "allows_execute_now": false
}
```

## Non-governance (冻结约束)

- 本阶段不允许生成 `semantic_summary`（必须为 `null`）。
- 本阶段不生成 `navigation_action`（必须为 `null`）。
- 本阶段所有输出仍保持 `candidate_only=true` 且 `allows_execute_now=false`。

## Filtering & blocking (占位冻结)

MidPlatform 必须对下列类别做“阻断占位”并记录原因，但不得删除原始 OCR evidence：
- advertisement_like_text
- promotional_text
- background_static_text
- low_confidence_text
- reading_order_uncertain_long_text
- irrelevant_to_current_task
- expired_scene_text

block_reason：
- 必须可追责（包含签名与 delta 决策的引用）。

