# LUNA — OCR Raw Text Benchmark Dataset v0

## Phase

- **Phase-ModelOCR-005**
- Scope: raw text GT dataset only; no semantic/navigation labels.

## Dataset root

- `datasets/ocr_raw_text_benchmark_v0/`
  - `images/`
  - `videos/`
  - `frames/`
  - `ground_truth/`
  - `manifests/`
  - `README.md`

## Manifest

- `datasets/ocr_raw_text_benchmark_v0/manifests/ocr_benchmark_samples_v0.json`
- Required fields: `sample_id/source_type/image_path/video_path/frame_id/timestamp_ms/expected_text_type/gt_path`

## GT schema

Each GT file:
- `sample_id`
- `gt_version`
- `image_size`
- `text_lines[]` with `text/bbox/line_order/block_id/reading_direction`
- `raw_text_joined`
- `raw_text_joined_strategy`
- `semantic_labels_enabled=false`
- `navigation_labels_enabled=false`

Forbidden fields:
- `scene_type`
- `task_label`
- `navigation_action`
- `route_advice`
- `semantic_summary`
- `should_speak`
- `should_turn`
- `go_direction`

## v0 note

v0 is a small seed set (manual GT) to validate benchmark pipeline completeness.
