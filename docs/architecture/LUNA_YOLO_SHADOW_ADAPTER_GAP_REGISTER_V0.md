# LUNA — YOLO Shadow Adapter Gap Register v0 (Phase-ModelPerception-002A)

## Purpose
Register gaps required to integrate existing YOLO detection into the **ModelPerception-001** contract as a future **shadow adapter**.

This is a gap list only; no implementation.

## Gaps (must include)

### 1) Input adapter gap
- Need: phone_local archive/source video → deterministic frame sampling (frame_id + timestamp)
- Current state: YOLOv5Detector accepts a single `frame` only; no phone_local archive reader here.

### 2) Output normalization gap
- Need: raw detections → PerceptionEval-001 five-signal normalized schema
- Current state: YOLOv5Detector returns list of dicts (bbox/class/conf) without envelope metadata.

### 3) Tracking gap
- Need: stability/tracking claims require track-id contract and quality metrics
- Current state:
  - YOLOv5Detector has no tracking
  - `Luna_Badge_MVP/vision/deepsort_tracker.py` exists but is simplified; cannot be treated as robust tracking without upgrades.

### 4) Depth gap
- Need: distance/depth for passability geometry and collision reasoning
- Current state: YOLO detection provides no depth; must be treated as depth_unavailable/not_available.

### 5) OCR gap
- Need: OCR signal category for Perception-001
- Current state:
  - detection-only YOLO provides none (must be not_available)
  - repository has `yolo11_ocr_*` pipeline, but it is a different capability line; not part of first “detection-only” scope by default.

### 6) Dynamic event gap
- Need: dynamic events require temporal logic (tracking/flow) with auditability
- Current state: detection-only output cannot claim dynamic events; must be not_available/candidate-only with uncertainty.

### 7) Risk interpretation gap
- Need: collision risk requires relative motion logic (TTC candidates) + confidence handling
- Current state: detection-only allows class-based risk hints only; cannot confirm collision risk.

### 8) Trace / replay / whitebox gap (ModelPerception-001 hard requirement)
- Need: record artifacts per run:
  - raw_model_output
  - normalized signals
  - schema_validation_result
  - forbidden_output_scan_result
  - replay_record + whitebox_record
- Current state:
  - MVP debug logs exist, but are not the ModelPerception-001 replay/whitebox contract
  - no standardized artifact envelope for YOLO outputs

### 9) Fallback / disable gap (ModelPerception-001 hard requirement)
- Need:
  - model_disabled switch (no model invocation needed)
  - fallback_to_baseline/mock on any failure/forbidden output
  - rollback-to-baseline policy
- Current state: not found for YOLO detection integration into phone_local eval chain.

### 10) SceneContext gate integration gap (mandatory)
- Need: YOLO normalized outputs must pass:
  - SceneContext-002 (depicted scene filter)
  - SceneContext-003 (physics consistency)
  - SceneContext-001 (continuity/transition policy)
- Current state: no integration found with phone_local evaluation chain.

## Additional inventory-specific gaps

### A) “torch.hub.load” network/caching dependency risk
- `YOLOv5Detector.initialize` uses `torch.hub.load('ultralytics/yolov5', ...)`
- Shadow integration should avoid uncontrolled downloads; prefer pinned local weights and explicit dependency management (implementation-phase decision).

### B) Mock dependency missing
- `mock_yolo.py` references `core.yolo_detector.DetectionResult`, but `core/yolo_detector.py` is **not_found**.

