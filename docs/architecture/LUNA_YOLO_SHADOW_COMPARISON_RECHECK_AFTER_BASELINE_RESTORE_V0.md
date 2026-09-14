# LUNA — YOLO Shadow Comparison Recheck After Baseline Restore v0 (ModelPerceptionFix-001)

## Purpose
Record the comparison re-run after restoring baseline PerceptionEval-001 outputs, without rewriting history.

## Inputs
- FieldBatch-002:
  - `logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`
- Restored baseline PerceptionEval-001 root:
  - `logs/perception_eval_option_a_phone_local_001_restore_20260427_1446/`
- YOLO shadow root (disable_yolo=true run):
  - `logs/yolo_shadow_eval_option_a_phone_local_001_20260427_1425/`

## Comparison runs
### Comparison run (after restore; fixed baseline parsing)
- Output root:
  - `logs/yolo_shadow_vs_baseline_compare_003_after_restore_fix_20260427_1447/`
- Summary:
  - baseline_root_not_found_or_not_dir: **false**
  - baseline_artifact_ready_rate: **1.0**
  - yolo_artifact_ready_rate (trace/replay/whitebox): **1.0**
  - baseline_signal_coverage_rate: **1.0**
  - yolo_signal_coverage_rate: **1.0**
  - yolo_invoked_count: **0**
  - yolo_fallback_count: **3**
  - yolo_disabled_count: **3**
  - execute/default leakage (baseline/yolo): **0**

## Interpretation boundary
This recheck demonstrates:
- baseline and yolo outputs are both readable and alignable by sample_id
- comparison is reproducible
- YOLO is still fallback-only in this run (disable_yolo=true) and must not be treated as real model capability

It does NOT demonstrate:
- real YOLO invocation on this chain
- any quality delta from enabling YOLO

