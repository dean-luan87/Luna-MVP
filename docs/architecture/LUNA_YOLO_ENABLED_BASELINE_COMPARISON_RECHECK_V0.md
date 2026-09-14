# LUNA — YOLO Enabled vs Baseline Comparison Recheck v0 (Phase-ModelPerception-005)

## Purpose
Perform the formal comparison recheck between:
- baseline/mock PerceptionEval-001 outputs
vs
- **YOLO enabled** shadow outputs (invoked_count>0),
on the same FieldBatch-002 baseline samples.

This is comparison-only; it does not integrate YOLO into SceneTask/Fusion/Output.

## Inputs
- FieldBatch-002:
  - `logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`
- baseline/mock PerceptionEval-001 root:
  - `logs/perception_eval_option_a_phone_local_001_restore_20260427_1446/`
- YOLO enabled shadow root:
  - `logs/yolo_shadow_eval_option_a_phone_local_enabled_smoke_retry_fix002_20260427_1503/`
- Comparison output root (this phase):
  - `logs/yolo_enabled_vs_baseline_compare_005_20260427_1507_v2/`

## Key results (from comparison summary)
- Alignment:
  - sample_alignment_rate: **1.0** (3/3) via `sample_id`
- YOLO enabled runtime:
  - invoked_count: **3**
  - fallback_count: **0**
  - detection_count_total: **39**
  - detection_count_per_sample:
    - clear_path: 7
    - minor_obstacle: 8
    - narrow_path: 24
  - detected_class_distribution:
    - person: 33
    - bicycle: 1
    - potted plant: 5
- Signal coverage:
  - baseline_signal_coverage_rate: **1.0**
  - yolo_signal_coverage_rate: **1.0**
  - yolo_object_detection_available_rate: **1.0**
- Boundary/safety:
  - execute leakage: **0**
  - default-on leakage: **0**
  - allows_execute_now_false_rate: **1.0**
  - evidence boundary preserved: **1.0**
- Artifacts:
  - baseline_artifact_ready_rate: **1.0**
  - yolo trace/replay/whitebox ready rates: **1.0**

## Interpretation boundary (must hold)
- This comparison shows **incremental object detection candidates** exist when YOLO is enabled.
- It does NOT prove:
  - navigation quality improvements
  - depth/OCR/dynamic/collision risk capability
  - readiness to execute actions

