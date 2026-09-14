# LUNA — YOLO Shadow vs Baseline Perception Comparison Matrix v0 (Phase-ModelPerception-003)

## Purpose
Matrix the comparison outcomes for the three FieldBatch-002 samples:
- baseline/mock PerceptionEval-001 outputs
vs
- YOLO shadow outputs (ModelPerception-002B)

This is a reporting matrix; it must not claim navigation improvement.

## Inputs (declared)
- FieldBatch-002 sample_matrix:
  - `logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`
- Baseline root (expected; may be missing in local workspace):
  - `logs/perception_eval_option_a_phone_local_001_20260427_113330/`
- YOLO shadow root:
  - `logs/yolo_shadow_eval_option_a_phone_local_001_20260427_1425/`

## Samples

### phone_local_001_clear_path
- baseline_found: **not_found_in_local_workspace** (must not fabricate)
- yolo_found: **true**
- yolo_invoked: **false** (disable_yolo=true run)
- fallback_used: **true**
- fallback_reason: **yolo_disabled**
- signals:
  - baseline coverage: **unknown** (baseline missing)
  - yolo coverage: **5/5 present** (OCR/dynamic not_available)
- artifacts:
  - yolo trace/replay/whitebox: **present**
- boundaries:
  - execute/default leakage: **0**

### phone_local_002_minor_obstacle
- baseline_found: **not_found_in_local_workspace**
- yolo_found: **true**
- yolo_invoked: **false**
- fallback_used: **true**
- fallback_reason: **yolo_disabled**
- signals: yolo **5/5 present** (limited passability/risk; OCR/dynamic not_available)
- artifacts: yolo trace/replay/whitebox **present**
- leakage: **0**

### phone_local_003_narrow_path
- baseline_found: **not_found_in_local_workspace**
- yolo_found: **true**
- yolo_invoked: **false**
- fallback_used: **true**
- fallback_reason: **yolo_disabled**
- signals: yolo **5/5 present** (limited passability/risk; OCR/dynamic not_available)
- artifacts: yolo trace/replay/whitebox **present**
- leakage: **0**

## Notes / constraints
- This matrix reflects the current environment where baseline PerceptionEval-001 output root was not found.
- Therefore, this phase can only validate:
  - YOLO shadow artifact integrity and boundaries
  - comparison tooling behavior under missing-baseline blocker
It cannot quantify baseline vs YOLO differences until baseline outputs are available at the declared path.

