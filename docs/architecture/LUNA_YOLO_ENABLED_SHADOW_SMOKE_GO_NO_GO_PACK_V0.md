# LUNA — YOLO Enabled Shadow Smoke Go/No-Go Pack v0 (Phase-ModelPerception-004)

## Inputs
- Definition:
  - `docs/architecture/LUNA_YOLO_ENABLED_SHADOW_SMOKE_RUN_DEFINITION_V0.md`
- Smoke result matrix:
  - `docs/architecture/LUNA_YOLO_ENABLED_SHADOW_SMOKE_RESULT_MATRIX_V0.md`
- Smoke outputs:
  - `logs/yolo_shadow_eval_option_a_phone_local_enabled_smoke_20260427_1453/`

## Decision
### Result
**CONDITIONAL_GO**

### Why CONDITIONAL_GO
- disable_yolo=false was used (enabled smoke attempted).
- YOLO was **not invoked successfully** (`invoked_count=0`) due to model load failure in this environment.
- Fail-closed behavior works:
  - fallback_count=3
  - five signals present per sample (OCR/dynamic not_available)
  - replay/whitebox/trace artifacts present
  - safety leakage=0
  - evidence boundary preserved
- Therefore:
  - We cannot claim “real YOLO inference works on this chain yet”
  - But we can proceed to a dependency/weights fix branch without losing safety guarantees.

## Required smoke metrics (recorded)
- sample_count_total=3; processed=3
- yolo_invoked_count=0
- yolo_fallback_count=3
- yolo_disabled_count=0
- yolo_exception_count=0 (surface error folded into model_load_failed)
- yolo_dependency_unavailable_count=3 (implicit via model_load_failed)
- detection_count_total=0
- trace/replay/whitebox ready rates=1.0
- allows_execute_now_false_rate=1.0
- execute/default-on leakage=0
- evidence boundary preserved rate=1.0

## Go / Conditional-Go / No-Go criteria (frozen)
### GO
Allow entering Phase-ModelPerception-005 (enabled vs baseline comparison recheck) if:
- yolo_invoked_count > 0 (at least one sample invoked successfully)
- detection artifacts present
- artifacts complete; leakage=0; boundaries preserved

### CONDITIONAL_GO (current)
- YOLO enabled smoke attempted but model load failed → all fallback
- artifacts + safety + boundaries confirmed
- next step must be dependency/weights fix (not a comparison claiming YOLO deltas)

### NO_GO
Any of:
- disable_yolo=false but no auditable record
- fallback fails or artifacts missing
- execute/default-on/release/retry/reopen leakage
- evidence boundary violated
- YOLO outputs wired to SceneTask/Fusion/Output

## Hard blockers
- `[]`

## Soft follow-ups
- Fix YOLO runtime dependencies for `torch.hub` YOLOv5 path (current observed missing dependency: `seaborn`).
- Consider pinning a minimal dependency set or using a local weights + ultralytics package path that avoids optional plotting deps.
- After dependency fix, rerun Phase-ModelPerception-004 until `invoked_count>0`, then proceed to Phase-ModelPerception-005.

## Fix/retry append (Phase-ModelPerceptionFix-002)
This section appends results; it does not delete the original CONDITIONAL_GO record.

- Readiness check output:
  - `logs/yolo_dependency_readiness_001_20260427_1500.json`
  - seaborn import: **ok**
  - dry-run model load: **ok**
- Enabled smoke retry output root:
  - `logs/yolo_shadow_eval_option_a_phone_local_enabled_smoke_retry_fix002_20260427_1503/`
- Retry summary:
  - disable_yolo: **false**
  - invoked_count: **3**
  - fallback_count: **0**
  - safety leakage: **0**
  - evidence boundary preserved: **true**

## Recommended next phase (do not auto-enter)
- Dependency fix branch for YOLO runtime (minimal, shadow-only) to eliminate `model_load_failed` due to missing python deps.

## Explicit boundary re-statement
- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- YOLO shadow 不直接进入 SceneTask/Fusion/Output
- 本阶段只做 YOLO enabled shadow smoke，不做 runtime 接入

