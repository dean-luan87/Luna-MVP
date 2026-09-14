# LUNA — SceneContext-001: Scene Continuity & Zone Reasoning Contract v0

## Purpose
Define a minimal, auditable contract for:
- `macro_scene` / `zone_type` hierarchy
- continuity inertia and transition evidence gating
- local-vs-global override constraints
- interfaces for downstream consumers (scene/task/fusion/output)
- reserved interface for depicted-scene filtering (SceneContext-002)

This is definition-only (no runtime).

## Data model (v0)

### macro_scene (enum)
- `outdoor_sidewalk`
- `indoor_office`
- `indoor_waiting_area`
- `indoor_pantry`
- `unknown`

Rules:
- `macro_scene` changes must pass transition evidence gate (see below).
- `unknown` is allowed as safe fallback and must not force actions.

### zone_type (enum)
- `sidewalk_segment`
- `open_office`
- `corridor`
- `lobby`
- `pantry`
- `waiting_area`
- `unknown`

Rules:
- `zone_type` must be interpreted within the current `macro_scene`.
- `zone_type` may change more frequently than `macro_scene`, but still uses inertia.

### scene_context_state (object)
Required fields:
- `state_id`
- `macro_scene`
- `zone_type`
- `macro_scene_confidence` (0..1)
- `zone_confidence` (0..1)
- `state_timestamp_ms`
- `last_macro_scene_transition_ms`
- `last_zone_transition_ms`
- `transition_evidence_summary` (string)
- `inertia` (object; see below)
- `depicted_scene_filter` (object; interface only; see below)
- `reason_codes` (list; non-empty)

### inertia (object)
Required fields:
- `macro_scene_min_dwell_ms` (default 15000)
- `zone_min_dwell_ms` (default 5000)
- `macro_scene_hysteresis` (default "strong")
- `zone_hysteresis` (default "medium")
- `max_flip_rate_per_minute` (default 2)

Interpretation:
- A proposed transition is rejected if it violates dwell/hysteresis constraints unless transition evidence is strong.

## Continuity rules (must be enforced by any future runtime)

### Rule 1 — Macro scene inertia
- A `macro_scene` transition requires:
  - time since `last_macro_scene_transition_ms` ≥ `macro_scene_min_dwell_ms`, AND
  - transition evidence gate passes.

### Rule 2 — Zone inertia
- A `zone_type` transition requires:
  - time since `last_zone_transition_ms` ≥ `zone_min_dwell_ms`, AND
  - minimal transition evidence (weaker threshold than macro).

### Rule 3 — Local objects must not override global scene
If perception detects local objects associated with a different macro scene (e.g., “coffee machine” while in outdoor sidewalk), then:
- Do NOT change `macro_scene` based on a single local object cue.
- Instead:
  - keep `macro_scene` unchanged,
  - set `zone_type=unknown` or keep prior zone,
  - record `reason_codes` indicating local-global conflict.

### Rule 4 — Scene switching requires transition evidence
`transition evidence` must be expressed as a structured record (below) and summarized in `transition_evidence_summary`.

## Transition evidence gate (v0 schema)

### transition_evidence (object)
Required fields:
- `evidence_id`
- `proposed_macro_scene`
- `proposed_zone_type`
- `evidence_strength`: `"weak" | "medium" | "strong"`
- `evidence_sources` (list of strings)
- `sustained_duration_ms` (int)
- `notes` (string)
- `reason_codes` (list)

Gate policy (v0):
- For **macro_scene** transition: require `evidence_strength="strong"` AND `sustained_duration_ms >= 3000`.
- For **zone_type** transition: allow `evidence_strength in {"medium","strong"}` AND `sustained_duration_ms >= 1500`.
- If any depicted-scene suspicion is active (see below): cap strength to `weak` until SceneContext-002 rules confirm otherwise.

## Depicted scene / visual medium filter (interface only; SceneContext-002)

### depicted_scene_filter (object)
Required fields:
- `status`: `"not_evaluated" | "suspected" | "cleared"`
- `suspected_medium_types` (list): `"screen" | "photo" | "poster" | "billboard" | "unknown"`
- `confidence` (0..1)
- `reason_codes` (list)

v0 policy (SceneContext-001):
- This phase only defines the interface.
- Any future runtime must treat `status="suspected"` as a hard guard that prevents macro_scene transitions based solely on depicted content.

## Downstream consumption contract (candidate-only annotations)
`scene_context_annotations` may accompany perception/scene_state outputs with:
- `macro_scene`
- `zone_type`
- `transition_evidence` (if any)
- `depicted_scene_filter`
- `reason_codes`

Hard boundary:
- These annotations must never directly create an execute-now output.

## Non-claims
This contract does not claim:
- real world zone reasoning correctness
- real perception model accuracy
- any navigation execution validity

