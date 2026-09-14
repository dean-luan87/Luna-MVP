# LUNA — YOLO Enabled Smoke Retry After Fix v0 (Phase-ModelPerceptionFix-002)

## Purpose
Record the retry of Phase-ModelPerception-004 after fixing dependency readiness (seaborn).

## Fix actions (summary)
- Installed missing dependency:
  - `seaborn`
- Ran readiness check:
  - `logs/yolo_dependency_readiness_001_20260427_1500.json`
  - dry-run model load: **ok**

## Enabled smoke retry
- Tool:
  - `tools/evaluate_option_a_phone_local_yolo_shadow_v0.py`
- Input:
  - `logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`
- Output root (retry):
  - `logs/yolo_shadow_eval_option_a_phone_local_enabled_smoke_retry_fix002_20260427_1503/`
- disable_yolo: **false**

### Retry outcome (from yolo_shadow_summary.json)
- invoked_count: **3**
- fallback_count: **0**
- ok_count: **3**
- detection_count_total: **>0 expected per-sample** (see per-sample results)
- safety leakage: **0**
- artifacts (trace/replay/whitebox): **present**
- evidence boundary preserved: **true**

## Notes on remaining risks
- torch.hub emits warnings about auto-updating requirements using `pip` (shell `pip` not found).
  - This does not block invocation now, but it reinforces the recommendation to move toward pinned local weights + pinned dependencies to avoid implicit installs/downloads.

