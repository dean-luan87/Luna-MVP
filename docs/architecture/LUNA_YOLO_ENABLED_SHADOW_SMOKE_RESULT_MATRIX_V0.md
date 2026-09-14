# LUNA — YOLO Enabled Shadow Smoke Result Matrix v0 (Phase-ModelPerception-004)

## Smoke run
- output_root:
  - `logs/yolo_shadow_eval_option_a_phone_local_enabled_smoke_20260427_1453/`
- disable_yolo: **false**

## Summary (from yolo_shadow_summary.json)
- sample_count_total: 3
- sample_count_processed: 3
- yolo_invoked_count: **0**
- yolo_fallback_count: **3**
- yolo_disabled_count: **0**
- detection_count_total: **0**
- safety_leakage: **0**
- artifacts ready (root): trace/replay/whitebox **present**

## Per-sample matrix

### phone_local_001_clear_path
- yolo_invoked: false
- fallback_used: true
- fallback_reason: **model_load_failed**
- detection_count: 0
- five signals present: yes (OCR/dynamic not_available)
- artifacts (sample): trace/replay/whitebox present: yes
- execute/default-on leakage: 0
- evidence boundary preserved: yes

### phone_local_002_minor_obstacle
- yolo_invoked: false
- fallback_used: true
- fallback_reason: **model_load_failed**
- detection_count: 0
- five signals present: yes (OCR/dynamic not_available)
- artifacts (sample): trace/replay/whitebox present: yes
- execute/default-on leakage: 0
- evidence boundary preserved: yes

### phone_local_003_narrow_path
- yolo_invoked: false
- fallback_used: true
- fallback_reason: **model_load_failed**
- detection_count: 0
- five signals present: yes (OCR/dynamic not_available)
- artifacts (sample): trace/replay/whitebox present: yes
- execute/default-on leakage: 0
- evidence boundary preserved: yes

## Notes
- This enabled smoke run attempted YOLO invocation, but model load failed in this environment.
- The failure mode is contained: fallback outputs are produced, artifacts are complete, and boundary leakage remains zero.

