# LUNA — YOLO Shadow Adapter Implementation v0 (Phase-ModelPerception-002B)

## Phase
- Phase: **Phase-ModelPerception-002B**
- Type: **Implementation (shadow-only, candidate-only)**

## Purpose
Implement a **single-model YOLO detection-first shadow adapter** that:
- reads phone_local sample source video (offline replay)
- samples frames
- runs YOLO detection *only if enabled*
- maps detections into Perception-001 five signal categories (limited support)
- writes replay/trace/whitebox artifacts
- supports disable switch and fallback to baseline/mock-shaped outputs

This implementation **does not** modify PerceptionEval-001 nor the downstream eval chain.

## Hard boundaries (frozen)
- Shadow-only; candidate-only; `allows_execute_now=false`.
- No default path; no side effects expansion.
- No SceneTask/Fusion/Output wiring in this phase.
- No claims of tracking/depth/OCR/dynamic/collision risk validation.
- Evidence boundary preserved:
  - `evidence_type=phone_local_controlled_capture`
  - `controlled_live_stream=false`
- Disable switch must prevent any model invocation.
- Any failure/forbidden output/schema failure must fallback.

## Code deliverables (paths)
- Adapter core:
  - `capabilities/model_perception/yolo_shadow_adapter_v0.py`
- Evaluation tool:
  - `tools/evaluate_option_a_phone_local_yolo_shadow_v0.py`
- Verifier:
  - `tools/verify_yolo_shadow_adapter_v0.py`

## Adapter input/output (v0)
### Inputs (per sample)
- sample_id
- source_video_path
- archive_root (recorded for audit; not used for inference)
- evidence_type / controlled_live_stream / phone_local_capture flags
- model_config_id
- disable switch
- max_frames / frame_step

### Outputs (per sample)
- normalized five signals:
  - object_stability_signal (from detections)
  - spatial_passability_signal (candidate-only, limited, depth unavailable)
  - risk_field_signal (class-based risk candidate only)
  - ocr_navigation_signal (not_available)
  - dynamic_event_signal (not_available)
- fallback_used + fallback_reason
- schema_validation_result
- forbidden_output_scan_result
- gate markers:
  - scene_context_gate_required=true
  - *_gate_status=not_executed_in_002b

## Mapping alignment
This implementation follows Phase-ModelPerception-002A mapping:
- `object_stability_signal` is the primary supported mapping.
- passability and risk are conservative candidates only with explicit limitation flags.
- OCR/dynamic are explicitly not_available.

## Replay / trace / whitebox (v0)
Per sample directory emits:
- `per_sample_yolo_shadow_results.json`
- `yolo_shadow_trace.jsonl`
- `yolo_shadow_replay.jsonl`
- `yolo_shadow_whitebox.jsonl`

Root eval emits:
- `yolo_shadow_summary.json`
- `per_sample_yolo_shadow_results.json` (aggregated)
- `yolo_shadow_trace.jsonl` (root)
- `yolo_shadow_replay.jsonl` (root)
- `yolo_shadow_whitebox.jsonl` (root)
- `evaluation_notes.md`

## SceneContext gate policy
This phase does not run gates; it marks:
- required=true
- status=not_executed_in_002b
and enforces: output cannot be used for SceneTask directly.

