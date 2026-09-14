# LUNA — YOLO → OCR Crop Proposal Schema v0

## Schema: `OCRCropProposal`

```json
{
  "proposal_id": "ocr_prop_001",
  "proposal_source": "yolo_detection",
  "source_detection_id": "det_001",
  "frame_id": "...",
  "timestamp_ms": 0,
  "image_ref": "...",
  "crop_region": {
    "x1": 0,
    "y1": 0,
    "x2": 0,
    "y2": 0,
    "coordinate_space": "image_pixel",
    "padding_policy": {
      "padding_ratio": 0.15,
      "min_padding_px": 8,
      "max_padding_px": 64,
      "clamped_to_image_bounds": true
    }
  },
  "source_object": {
    "class_name": "sign",
    "confidence": 0.0,
    "bbox": [0, 0, 0, 0]
  },
  "ocr_trigger_type": "yolo_guided_crop",
  "ocr_priority": "normal",
  "ocr_reason": "possible_text_region",
  "allows_execute_now": false,
  "semantic_interpretation_enabled": false,
  "downstream_invocation_allowed": false,
  "real_tts_invoked": false
}
```

## OCR-worthy classes (v0 definition)

Preferred: sign, traffic sign, poster, screen, label, bus, train, elevator, door, storefront, board, unknown_text_like_region.

Normally excluded: person, bicycle, car, tree, chair, road, sky, floor, wall (except future sign-like detection refinement).

## Padding rules

- `padding_ratio=0.15`
- `min_padding_px=8`
- `max_padding_px=64`
- always clamp to image bounds
- keep original YOLO bbox and padded crop together
