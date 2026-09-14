# LUNA — YOLO Shadow Perception Comparison Go/No-Go Pack v0 (Phase-ModelPerception-003)

## Inputs
- Definition:
  - `docs/architecture/LUNA_YOLO_SHADOW_PERCEPTION_COMPARISON_DEFINITION_V0.md`
- Comparison contract:
  - `docs/architecture/LUNA_YOLO_SHADOW_PERCEPTION_COMPARISON_CONTRACT_V0.md`
- Comparison tool:
  - `tools/compare_yolo_shadow_vs_baseline_perception_v0.py`
- Comparison matrix:
  - `docs/architecture/LUNA_YOLO_SHADOW_PERCEPTION_COMPARISON_MATRIX_V0.md`

Declared runtime inputs (expected):
- baseline root:
  - `logs/perception_eval_option_a_phone_local_001_20260427_113330/`
- yolo shadow root:
  - `logs/yolo_shadow_eval_option_a_phone_local_001_20260427_1425/`
- fieldbatch root:
  - `logs/phone_local_field_batch_002_20260427_111431/`

## Decision
### Result
**CONDITIONAL_GO**

### Why CONDITIONAL_GO
- Comparison mechanism is implemented and fail-closed:
  - if baseline root is missing, it records an explicit blocker and does not fabricate baseline outputs.
- YOLO shadow side can be read and aligned by sample_id (FieldBatch-002).
- Report focuses on:
  - coverage fields
  - invocation/fallback status
  - artifact integrity (trace/replay/whitebox)
  - boundary leakage counts (execute/default-on)
- Current environment indicates baseline root may be missing; thus the comparison cannot yet quantify baseline-vs-YOLO differences.

## Go / Conditional-Go / No-Go criteria (frozen)
### GO
Allow entering **Phase-ModelPerception-004 YOLO Enabled Shadow Smoke Run v0** if:
- comparison tool runs
- all three samples align
- artifacts complete
- safety leakage=0
- baseline root is available and comparable OR explicitly recorded as missing without misrepresentation

### CONDITIONAL_GO (current)
- baseline root not found in local workspace, but:
  - tool and contract exist
  - YOLO shadow alignment and boundary checks are reportable
  - report explicitly labels fallback-only and missing-baseline as blockers

### NO_GO
Any of:
- sample alignment fails (sample_id mismatch) without explicit reporting
- YOLO artifacts missing
- execute/default/release/retry/reopen leakage detected
- evidence_type modified or controlled_live_stream becomes true
- fallback outputs mislabeled as real YOLO invocation
- comparison output not reproducible

## Hard blockers
- `[]` (comparison tool can run even if baseline root is missing; it records blocker)

## Soft follow-ups
- Ensure baseline PerceptionEval-001 output root exists at the declared path before interpreting deltas.
- After baseline root is available, rerun comparison to produce real delta metrics (still no integration).

## Recheck after baseline restore (ModelPerceptionFix-001)
This section appends results; it does not rewrite the original conditional_go record.

- Baseline restored root:
  - `logs/perception_eval_option_a_phone_local_001_restore_20260427_1446/`
- Comparison re-run output:
  - `logs/yolo_shadow_vs_baseline_compare_003_after_restore_fix_20260427_1447/`
- Recheck summary assertions:
  - `baseline_artifact_ready_rate=1.0`
  - baseline sample alignment by `sample_id`: **3/3**
  - yolo sample alignment by `sample_id`: **3/3**
  - execute/default leakage: **0**
  - YOLO invocation status unchanged in this run: `invoked_count=0` (fallback-only; disable_yolo=true)

## Recommended next phase (do not auto-enter)
- **Phase-ModelPerception-004 — YOLO Enabled Shadow Smoke Run v0**
  - Only after comparison report is complete and baseline path is available (or explicitly accepted as missing with a defined remediation).

## Explicit boundary re-statement
- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- YOLO shadow 不直接进入 SceneTask/Fusion/Output
- 本阶段只做 baseline vs YOLO shadow comparison，不做 runtime 接入

