# LUNA — YOLO → Perception Signal Adapter Mapping v0 (Phase-ModelPerception-002A)

## Purpose
Define how existing YOLO-style object detection outputs can be mapped into the **PerceptionEval-001** five signal categories **without implementing runtime**.

This mapping is explicitly **candidate-only** and designed for future shadow adapter work.

## Hard boundaries (frozen)
- 本阶段只做映射定义，不实现 adapter。
- 不调用 YOLO 推理，不生成新模型结果。
- 不改变 PerceptionEval-001 现有结构与 runtime。
- 不声称 tracking / depth / OCR / dynamic 能力存在，除非明确模块提供且可审计。

## Source: existing detection shapes (inventory-derived)

### A) YOLOv5Detector detection item (current shape)
From `Luna_Badge_MVP/vision/yolov5_detector.py`:
- `bbox`: `[x1, y1, x2, y2]` (xyxy int)
- `confidence`: float
- `class_id`: int
- `class_name`: str

Missing (must be added by future adapter wrapper):
- `frame_id`, `timestamp`, `model_run_id`, `model_config_id`

### B) Optional track candidate shape (if a tracker is later added)
`Luna_Badge_MVP/vision/deepsort_tracker.py` can emit:
- `track_id` + detection fields
Constraint:
- current implementation is simplified; must be labeled as **track_id_candidate**, not stable tracking claim.

## Target: PerceptionEval-001 five categories (mapping)

### 1) object_stability_signal (primary mapping)
#### Inputs
- detections per frame (bbox/class/conf)
- optional track_id_candidate (if available)

#### Outputs (candidate-only fields, conceptual)
- `detected_objects` (list):
  - `bbox_xyxy`
  - `class_id` / `class_name`
  - `confidence`
  - `frame_id`
  - `ts`
  - `source=model_yolo_shadow` (future)
- `object_count`
- `class_distribution`
- `confidence_summary` (min/mean/max)
- `tracked_object_candidates`:
  - only if track_id_candidate exists
  - must include `tracking_quality=unknown` unless a real tracker contract exists

#### Required disclaimers (must be carried forward)
- If no track_id: **do not claim stability across frames**; label as `object_detection_candidates_only`.

### 2) spatial_passability_signal (secondary, limited mapping)
YOLO detections can only contribute as **obstacle presence candidates**.

#### Allowed inference (candidate-only)
- obstacle class candidates (person/bicycle/vehicle/large obstacle)
- rough direction candidates from bbox horizontal position (left/center/right)
- rough occlusion/coverage from bbox area ratio

#### Hard limitations (must be explicit)
YOLO alone cannot confirm:
- true distance/depth
- ground plane geometry
- step height / slope
- corridor width in meters
- passability certainty

#### Required output flags (must be frozen)
- `passability_source=object_detection_only`
- `depth_unavailable=true` OR `not_available`
- `passability_confidence_limited=true`
- default to **unknown / uncertain** if no additional geometry module exists

### 3) risk_field_signal (secondary, limited mapping)
YOLO can contribute **class-based risk candidates** only.

#### Allowed candidates
- presence of `person`, `bicycle`, `vehicle`, `obstacle` as risk contributors
- confidence-weighted risk hint (still not collision risk)

#### Hard limitations (must be explicit)
YOLO alone cannot confirm:
- relative velocity
- approach direction
- time-to-contact
- collision risk certainty

#### Required output flags
- `risk_source=class_candidate_only`
- `motion_unavailable=true` unless temporal logic exists and is auditable
- `collision_risk_not_confirmed=true`

### 4) ocr_navigation_signal (not supported by YOLO detection-only)
If the first model scope is **object detection only**:
- must output `status=not_available`
- must not fabricate OCR tokens

Note:
- repository has a separate `yolo11_ocr_*` line, but that is **OCR token extraction**, not the “first object detection model” scope.

### 5) dynamic_event_signal (not supported unless tracking/temporal module exists)
If no robust temporal module is integrated:
- must output `dynamic_event_status=not_available` (or candidate-only with explicit uncertainty)
- must not claim real dynamic event recognition

## Cross-layer constraints (must be enforced in future implementation)
- Normalized signals must still pass:
  - SceneContext-002 (depicted scene guard)
  - SceneContext-003 (physics consistency)
  - SceneContext-001 (continuity + transition evidence)
- Adapter must run:
  - schema validation
  - forbidden output scan
  - replay/whitebox recording
  - disable switch + fallback to baseline/mock

## Explicit “cannot claim” list (frozen)
Unless separate audited modules are present:
- cannot claim stable tracking
- cannot claim depth/distance
- cannot claim OCR
- cannot claim dynamic event semantics
- cannot claim collision risk certainty

