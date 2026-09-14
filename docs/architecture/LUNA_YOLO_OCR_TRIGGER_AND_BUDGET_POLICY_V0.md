# LUNA — YOLO × OCR Trigger and Budget Policy v0

## Trigger ownership and scheduling boundary

- TaskChain proposes goals/intents, not module-level direct commands.
- MidPlatform decides whether to trigger OCR, which trigger type to use, and budget/fallback behavior.
- YOLO can trigger `yolo_guided_crop`, but YOLO is not the only OCR trigger source.

## Trigger types

1. `full_frame_low_frequency`
2. `yolo_guided_crop`
3. `task_hint_guided_crop` (placeholder)
4. `scene_context_probe` (placeholder)
5. `manual_debug_sample`

## v0 focus

- `full_frame_low_frequency`
- `yolo_guided_crop`

## Budget definition (policy-only)

```json
{
  "max_ocr_proposals_per_frame": 3,
  "max_full_frame_ocr_per_window": 1,
  "ocr_cooldown_ms_per_region": 2000,
  "duplicate_region_iou_threshold": 0.85,
  "duplicate_text_signature_enabled": true
}
```

## Fallback and degradation

- No YOLO detection: optional low-frequency full-frame OCR or `not_available`.
- Non OCR-worthy class: do not create proposal.
- Out-of-bounds crop: clamp; if invalid after clamp, block proposal.
- OCR failure: use OCR offline source policy fallback chain.
- Empty OCR output: keep empty candidates + reason (`no_text_detected`/`not_available_reason`).
- Invalid OCR schema: block bridge result.
- Governance leakage: hard blocker.


## Dedup and delta placeholder (deferred)

Bridge-001 defines budget/dedup policy but does not implement delta control.
Future MidPlatform delta mechanism will own:
- previously processed information comparison
- no-change skip
- changed-information-only processing
