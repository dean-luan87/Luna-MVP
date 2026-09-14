# LUNA — OCR Raw Text Segment Schema v0

## Phase

- **Phase-ModelOCR-001-Patch-002**

## Segment schema

```json
{
  "raw_text_candidates": [],
  "raw_text_joined": "",
  "raw_text_joined_truncated": false,
  "raw_text_joined_length": 0,
  "raw_text_segments": [
    {
      "segment_id": "seg_001",
      "layout_block_id": "block_001",
      "text": "",
      "line_ids": ["txt_001", "txt_002"],
      "char_count": 0,
      "segment_order": 1,
      "segment_strategy": "layout_block",
      "truncated": false,
      "truncated_reason": null
    }
  ],
  "length_policy": {
    "candidate_text_max_chars": 128,
    "joined_text_max_chars": 512,
    "segment_text_max_chars": 256,
    "max_candidates_per_frame": 50,
    "max_segments_per_frame": 20
  }
}
```

## Required constraints

- `line_ids` must reference original `raw_text_candidates.text_id`.
- `char_count` must match segment text length.
- `segment_order` must preserve deterministic replay order.
- `segment_strategy` allowed values:
  - `layout_block`
  - `line_window`
  - `length_split`
