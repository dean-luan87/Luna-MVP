# LUNA — YOLO × OCR Delta Control Placeholder v0

## Purpose

Reserve fields for future mid-platform delta control (processed-information reuse), without implementing it in Bridge-001.

## Deferred mechanism (not implemented in this phase)

- Compare current OCR information with previously processed information.
- Skip unchanged information.
- Process only changed information via partial/full update.

## Placeholder fields

```json
{
  "crop_signature": "hash(crop_region + source_object_class)",
  "text_signature": "hash(normalized_text + line_order + layout_block_id)",
  "layout_signature": "hash(block_bbox + line_count + raw_text_joined_strategy)",
  "source_frame_window_id": "...",
  "previous_result_ref": null,
  "delta_control_deferred": true
}
```

## Boundary

- no mid-platform integration
- no semantic extraction
- no downstream invocation
