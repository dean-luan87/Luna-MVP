# LUNA — YOLO Enabled Shadow Smoke Run Definition v0 (Phase-ModelPerception-004)

## Phase
- Phase: **Phase-ModelPerception-004**
- Type: **Single enabled smoke run (shadow-only)**

## One thing only (scope)
Run a YOLO enabled shadow evaluation once (disable_yolo=false) on FieldBatch-002 to validate:
1. Whether YOLO can be invoked at least once
2. Whether detection candidates can be produced (if invocation succeeds)
3. If invocation fails, fail-closed fallback still works
4. replay/whitebox/trace artifacts are complete
5. no execute/default-on/release/retry/reopen leakage
6. evidence boundary preserved

No SceneTask/Fusion/Output integration.

## Inputs
- FieldBatch-002 sample_matrix:
  - `logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`
- Tool:
  - `tools/evaluate_option_a_phone_local_yolo_shadow_v0.py`

## Outputs (required)
- `yolo_shadow_summary.json`
- `per_sample_yolo_shadow_results.json`
- `yolo_shadow_trace.jsonl`
- `yolo_shadow_replay.jsonl`
- `yolo_shadow_whitebox.jsonl`
- `evaluation_notes.md`

## Hard boundaries (frozen)
- shadow-only / candidate-only
- no navigation actions; no real TTS
- no default-on; no side effects expansion
- YOLO outputs must not enter SceneTask/Fusion/Output
- failure must fallback; fallback must be auditable

## Stop condition
Stop after one enabled smoke run and producing:
- result matrix
- go/no-go pack
- README index update

