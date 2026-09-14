# LUNA — YOLO Enabled vs Baseline Comparison Go/No-Go Pack v0 (Phase-ModelPerception-005)

## Inputs
- Comparison output root:
  - `logs/yolo_enabled_vs_baseline_compare_005_20260427_1507_v2/`
- FieldBatch-002:
  - `logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`
- Baseline root:
  - `logs/perception_eval_option_a_phone_local_001_restore_20260427_1446/`
- YOLO enabled shadow root:
  - `logs/yolo_shadow_eval_option_a_phone_local_enabled_smoke_retry_fix002_20260427_1503/`

Docs:
- `docs/architecture/LUNA_YOLO_ENABLED_BASELINE_COMPARISON_RECHECK_V0.md`
- `docs/architecture/LUNA_YOLO_ENABLED_BASELINE_COMPARISON_MATRIX_V0.md`

## Decision
### Result
**GO**

### Why GO
- Alignment is complete (3/3 samples) by `sample_id`.
- YOLO enabled shadow actually ran:
  - `yolo_invoked_count=3`
  - `yolo_fallback_count=0`
  - `detection_count_total=39` with per-sample breakdown recorded.
- Signal coverage parity:
  - baseline coverage=1.0
  - yolo coverage=1.0
- Boundary integrity preserved:
  - execute leakage=0; default-on leakage=0
  - `allows_execute_now_false_rate=1.0`
  - evidence boundary preserved rate=1.0
- Artifacts integrity:
  - baseline artifact ready rate=1.0
  - YOLO trace/replay/whitebox ready rate=1.0
- No integration into SceneTask/Fusion/Output occurred.

## Hard boundaries (re-affirmed)
- This does not prove navigation quality.
- This does not validate depth/OCR/dynamic/collision risk.
- YOLO remains shadow-only / candidate-only.

## Hard blockers
- `[]`

## Soft follow-ups
- torch.hub remains a reproducibility risk; prioritize pinned local weights + pinned dependencies.
- Consider adding a “model-load once per run” optimization later (avoid repeated hub load per sample) without changing boundaries.

## Recommended next phase (do not auto-enter)
- **Phase-ModelPerception-006 — YOLO Shadow PerceptionEval Replacement Trial v0**
  - Still shadow-only/candidate-only; still gated; still no SceneTask/Fusion/Output execution authority.

## Explicit boundary re-statement
- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- YOLO enabled shadow 不直接进入 SceneTask/Fusion/Output
- 本阶段只做 enabled YOLO vs baseline comparison

