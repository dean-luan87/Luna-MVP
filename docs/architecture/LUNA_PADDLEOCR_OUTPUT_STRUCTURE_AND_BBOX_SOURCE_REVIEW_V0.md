# LUNA — PaddleOCR Output Structure and BBox Source Review v0

## Phase

- **Phase-ModelOCR-006C**

## Review scope

- raw output structure for PaddleOCR 3.5.0 runtime
- normalization mapping correctness
- bbox field candidates and polygon-to-xyxy conversion evidence
- bbox unavailable handling (`bbox_status=not_available`, `bbox_iou_excluded=true`)
