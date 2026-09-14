# LUNA — YOLO × OCR Offline Bridge Skeleton v0

## Phase

- **Phase-ModelOCR-YOLO-Bridge-002** — offline skeleton implementation only.

## Scope

Implements offline skeleton to convert YOLO detections into OCR crop proposals, run OCR via `ocr_default_offline_raw_text_source_policy_v0`, and emit bridge results with attribution + trace/replay/whitebox.

## Implemented artifacts

- `capabilities/model_ocr/yolo_ocr_bridge_v0.py`
  - `build_ocr_crop_proposals_v0(...)`
  - `run_yolo_ocr_bridge_v0(...)`
- `tools/evaluate_yolo_ocr_offline_bridge_v0.py`
- `tools/verify_yolo_ocr_offline_bridge_v0.py`
- `datasets/yolo_ocr_bridge_samples_v0/sample_matrix.json`

## Runtime boundary

- Offline tooling only.
- No product runtime integration.
- No MidPlatform wiring, no SceneTask/Fusion/Output, no semantic interpretation.

## Evidence run (example)

- `logs/yolo_ocr_offline_bridge_002_20260429_151332`

## Key outcomes

- OCR-worthy detections produced proposals with clamped padded crops.
- OCR source policy used for provider selection.
- Bridge results include YOLO + OCR attribution and delta placeholder fields.
- Verifier A-Q: **GO**.
