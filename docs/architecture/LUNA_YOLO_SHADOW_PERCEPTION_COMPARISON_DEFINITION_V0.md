# LUNA — YOLO Shadow Perception Comparison Definition v0 (Phase-ModelPerception-003)

## Phase
- Phase: **Phase-ModelPerception-003**
- Type: **Comparison evaluation only (no runtime integration)**

## One thing only (scope)
Compare, on the same FieldBatch-002 phone_local baseline:
1. **PerceptionEval-001 baseline/mock outputs**
2. **ModelPerception-002B YOLO shadow adapter outputs**

Goal: decide whether YOLO shadow is a viable **perception candidate source** for the next controlled step.

## Inputs (declared)
- FieldBatch-002:
  - `logs/phone_local_field_batch_002_20260427_111431/`
- Baseline PerceptionEval-001 output root (expected):
  - `logs/perception_eval_option_a_phone_local_001_20260427_113330/`
- YOLO shadow output root:
  - `logs/yolo_shadow_eval_option_a_phone_local_001_20260427_1425/`

## Outputs (required)
- comparison summary (JSON)
- per-sample comparison records (JSON)
- comparison notes (MD)
- docs: contract + matrix + go/no-go pack

## Hard boundaries (must be written as invariants)
- Comparison only; no runtime integration.
- Do not modify PerceptionEval-001 or downstream SceneTask/Fusion/Output.
- YOLO shadow must not enter SceneTask/Fusion/Output.
- No execute/release/retry/reopen; no default-on; no side effects expansion.
- If YOLO was not invoked (fallback-only), must state it explicitly.
- Must not present fallback outputs as real YOLO capability.

## Stop condition
Stop when:
- definition, contract, matrix, go/no-go pack complete
- comparison tool implemented
- comparison report generated (even if baseline root is missing, report must fail-closed and record blockers)

