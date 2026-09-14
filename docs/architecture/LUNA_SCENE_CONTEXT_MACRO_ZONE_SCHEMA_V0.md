# LUNA — SceneContext Macro/Zone Schema v0 (Phase-SceneContext-001)

## Purpose
Freeze schemas for:
- `macro_scene`
- `zone_type`
- `scene_transition`
- task relevance hooks
so downstream layers can consume a stable scene context representation.

Definition-only; no runtime.

## macro_scene (enum, v0)
Allowed examples (expandable later; v0 must include at least):
- `coworking_space`
- `office_building`
- `hospital`
- `metro_station`
- `shopping_mall`
- `residential_home`
- `outdoor_sidewalk`
- `unknown_macro_scene`

## zone_type (enum, v0)
Allowed examples (expandable later; v0 must include at least):
- `workspace_area`
- `pantry_area`
- `meeting_room`
- `corridor`
- `reception_area`
- `waiting_area`
- `elevator_area`
- `restroom_area`
- `entrance_area`
- `platform_area`
- `checkout_area`
- `food_court_area`
- `unknown_zone`

## scene_transition_type (enum)
- `no_change`
- `zone_shift`
- `macro_scene_candidate`
- `macro_scene_confirmed`
- `uncertain_transition`

## task_relevance (enum)
- `primary_task_context`
- `path_context_only`
- `distractor`
- `unknown`

## scene_context_output (object schema)
Must include at least:
- `scene_context_id`
- `previous_macro_scene`
- `current_macro_scene`
- `macro_scene_confidence` (0..1)
- `previous_zone_type`
- `current_zone_type`
- `zone_type_confidence` (0..1)
- `scene_transition_type` (enum)
- `transition_confidence` (0..1)
- `visual_evidence` (object)
- `spatial_evidence` (object)
- `temporal_evidence` (object)
- `task_context` (object; may be empty but must exist)
- `task_relevance` (enum)
- `conflict_detected` (bool)
- `degraded_mode` (bool)
- `reason_codes` (list; non-empty)
- `allows_execute_now=false`

### visual_evidence (object, minimal)
- `local_object_cues` (list of strings)
- `scene_landmark_cues` (list of strings)
- `depicted_scene_suspected` (bool; interface for SceneContext-002)

### spatial_evidence (object, minimal)
- `layout_change_detected` (bool)
- `doorway_or_entrance_detected` (bool)
- `distance_or_displacement_estimate` (string or number; optional)

### temporal_evidence (object, minimal)
- `sustained_duration_ms` (int)
- `inertia_guard_applied` (bool)

## Invariants (must be stated)
- `allows_execute_now` must be `false`.
- local object cues may update `zone_type`, but must not directly confirm `macro_scene`.
- `macro_scene_confirmed` requires transition evidence (defined in transition policy doc).

