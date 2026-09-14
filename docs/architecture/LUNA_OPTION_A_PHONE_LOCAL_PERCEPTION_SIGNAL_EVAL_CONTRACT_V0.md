# LUNA — Option A Phone Local Perception Signal Eval Contract v0 (Phase-PerceptionEval-001)

## Purpose
Define the minimum schema and boundary rules for PerceptionEval-001 outputs over Option A phone_local baseline samples.

## Global boundaries (must hold)
- Output is **signals/candidates only**.
- Forbidden outputs (must never appear):
  - execute / release / retry / reopen
  - default-on enablement
  - any navigation action directive (“force_walk”, “force_turn”, “avoid_now”, etc.)
- Must preserve evidence semantics:
  - do not rewrite evidence_type
  - do not relabel as controlled_live_stream
  - do not auto-close pending flags
- If runtime is baseline/mock:
  - `perception_runtime_mode=baseline_or_mock`
  - `not_model_claimed=true`

## Per-sample result schema (minimum fields)
Each `per_sample_results` row must include:
- `sample_id`
- `archive_root`
- `source_video_path`
- `evidence_type`
- `controlled_live_stream`
- `phone_local_capture`
- `pending_real_sidewalk_run`
- `perception_runtime_mode`
- `not_model_claimed` (bool)
- `signals` (object; five keys below)
- `signal_presence` (object; five booleans)
- `metrics` (object; leakage counters + confidence checks)
- `reason_codes` (non-empty list)
- `hard_blockers` (list)
- `soft_followups` (list)

## Five signal schemas (v0 minimal)

### 1) object_stability_signal
Allowed values:
- `stability`: `"stable" | "unstable" | "unknown"`
- `tracked_object_count`: int (>=0)
- `confidence`: float in [0,1]

Forbidden:
- any action directive fields

### 2) ocr_navigation_signal
Allowed values:
- `status`: `"available" | "not_available"`
- `text_detected`: bool
- `text_type`: `"sign" | "crosswalk" | "storefront" | "unknown" | "none"`
- `navigation_relevance`: `"none" | "low" | "medium" | "high" | "unknown"`
- `confidence`: float in [0,1]

Rules:
- If OCR is not available, must set:
  - `status="not_available"`
  - `text_detected=false`
  - `text_type="none"`
  - `navigation_relevance="unknown"`
  - `confidence=0.0`
- Must not fabricate OCR text content.

### 3) spatial_passability_signal
Allowed values:
- `passability`: `"passable" | "blocked" | "narrow" | "unknown"`
- `obstacle_direction`: `"left" | "center" | "right" | "unknown"`
- `confidence`: float in [0,1]

Forbidden:
- `force_walk`, `force_turn`, or any execute-now directive.

### 4) dynamic_event_signal
Allowed values:
- `dynamic_event_detected`: bool
- `event_type`: `"person" | "vehicle" | "bike" | "unknown" | "none"`
- `urgency_level`: `"low" | "medium" | "high" | "unknown"`
- `confidence`: float in [0,1]

Forbidden:
- `immediate_execute` or any action directive.

### 5) risk_field_signal
Allowed values:
- `risk_level`: `"low" | "medium" | "high" | "unknown"`
- `recommended_handling`: `"observe" | "slow_down_candidate" | "ask_for_help_candidate" | "unknown"`
- `confidence`: float in [0,1]

Forbidden:
- any hard execute action.

## Leakage counters (must be zero)
Per sample `metrics` must include:
- `execute_leakage_count`
- `default_on_leakage_count`
- `side_effects_expansion_count`
All must be **0**.

Also include:
- `low_confidence_forced_decision_count` (must be 0)
- `unsafe_overconfident_output_count` (must be 0)

