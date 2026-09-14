# LUNA — YOLO Enabled vs Baseline Comparison Matrix v0 (Phase-ModelPerception-005)

## Inputs
- baseline root:
  - `logs/perception_eval_option_a_phone_local_001_restore_20260427_1446/`
- yolo enabled root:
  - `logs/yolo_shadow_eval_option_a_phone_local_enabled_smoke_retry_fix002_20260427_1503/`
- comparison output root:
  - `logs/yolo_enabled_vs_baseline_compare_005_20260427_1507_v2/`

## Per-sample matrix (3 samples)

### phone_local_001_clear_path
- alignment: baseline_found=true, yolo_found=true
- yolo_invoked=true; fallback_used=false
- detection_count=7
- class_distribution (yolo): person=7
- signal_coverage: baseline=5/5, yolo=5/5
- artifacts: baseline ready; yolo trace/replay/whitebox ready
- leakage: execute/default-on = 0
- boundary: evidence_type preserved; controlled_live_stream=false

### phone_local_002_minor_obstacle
- alignment: baseline_found=true, yolo_found=true
- yolo_invoked=true; fallback_used=false
- detection_count=8
- class_distribution (yolo): person=7, bicycle=1
- signal_coverage: baseline=5/5, yolo=5/5
- artifacts: baseline ready; yolo trace/replay/whitebox ready
- leakage: execute/default-on = 0
- boundary: evidence_type preserved; controlled_live_stream=false

### phone_local_003_narrow_path
- alignment: baseline_found=true, yolo_found=true
- yolo_invoked=true; fallback_used=false
- detection_count=24
- class_distribution (yolo): person=19, potted plant=5
- signal_coverage: baseline=5/5, yolo=5/5
- artifacts: baseline ready; yolo trace/replay/whitebox ready
- leakage: execute/default-on = 0
- boundary: evidence_type preserved; controlled_live_stream=false

## Notes
- Baseline is baseline/mock; YOLO is enabled shadow detection-first.
- Differences here are **perception candidates only**; no claims about navigation outcomes.

