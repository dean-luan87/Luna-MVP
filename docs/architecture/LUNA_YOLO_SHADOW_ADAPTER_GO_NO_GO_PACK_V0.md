# LUNA — YOLO Shadow Adapter Go/No-Go Pack v0 (Phase-ModelPerception-002B)

## Inputs (artifacts + docs)
- Adapter implementation:
  - `capabilities/model_perception/yolo_shadow_adapter_v0.py`
- Evaluation tool:
  - `tools/evaluate_option_a_phone_local_yolo_shadow_v0.py`
- Verifier:
  - `tools/verify_yolo_shadow_adapter_v0.py`
- Implementation note:
  - `docs/architecture/LUNA_YOLO_SHADOW_ADAPTER_IMPLEMENTATION_V0.md`
- Evaluation matrix:
  - `docs/architecture/LUNA_YOLO_SHADOW_ADAPTER_EVALUATION_MATRIX_V0.md`
- Upstream contracts:
  - ModelPerception-001 docs (I/O, adapter+fallback, gate policy, admission matrix)
  - ModelPerception-002A mapping + gap register

## Decision
### Result
**CONDITIONAL_GO**

### Why CONDITIONAL_GO
- Adapter + eval tool + verifier exist and are shadow-only/candidate-only by design.
- Disable switch + fallback paths are implemented (fail-closed).
- Forbidden token scanning + schema validation exist and fallback on failure.
- Replay/whitebox/trace artifacts are produced per sample.
- Gates are not executed in 002B (by requirement); outputs are marked `gate_required=true` and `*_gate_status=not_executed_in_002b`.

Conditional aspect:
- Real YOLO invocation depends on local dependencies/weights and is not guaranteed in all environments.
- Detection quality is explicitly non-blocking in v0; this phase validates **contracts + safety** first.

## Go / Conditional-Go / No-Go criteria (frozen)
### GO
Allow entering ModelPerception-003 (YOLO shadow vs baseline comparison) if:
- Adapter runs on FieldBatch-002 sample_matrix and produces outputs for all samples (either real detections or fallback)
- Five signals always present (some may be not_available)
- disable/fallback verified
- replay/whitebox/trace present
- forbidden semantics leakage = 0
- evidence boundary preserved
- outputs are not wired to SceneTask/Fusion/Output

### CONDITIONAL_GO (current)
- Real YOLO may fallback due to dependency/weights
- Smoke verification may rely on mock detector for forbidden/disable paths
But must still hold:
- no execution semantics
- no default-on
- fail-closed fallback
- artifacts complete

### NO_GO
Any of:
- YOLO output can trigger execute/release/retry/reopen/default-on semantics
- disable switch does not prevent invocation
- fallback missing or non-auditable
- replay/whitebox missing
- evidence_type modified or controlled_live_stream becomes true
- adapter output wired directly into SceneTask/Fusion/Output

## Hard blockers
- `[]`

## Soft follow-ups
- Make real YOLO invocation deterministic by pinning local weights and avoiding torch.hub download paths.
- Add a “real-run evidence” note per run to separate mock/verifier runs from real YOLO runs (still shadow-only).
- If/when tracking is added, define a real tracking contract; do not upgrade claims silently.

## Recommended next phase (do not auto-enter)
- **Phase-ModelPerception-003 — YOLO Shadow PerceptionEval Comparison v0**
  - compares YOLO-shadow signals vs baseline/mock signals on phone_local baseline, still candidate-only, still gated.

## Explicit boundary re-statement (for audit)
- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- YOLO shadow 不直接进入 SceneTask/Fusion/Output
- 本阶段实现 YOLO Shadow Adapter，但不赋予执行权

