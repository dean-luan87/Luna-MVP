# LUNA — Visual Medium & Depicted Scene Schema v0 (Phase-SceneContext-002)

## Purpose
Freeze the minimal schema for the filter layer output so that:
- depicted scene signals can be recorded for audit/whitebox
- real-world macro_scene/zone reasoning is protected
- downstream (SceneContext-001 and beyond) can rely on stable flags

Definition-only; no runtime.

## Enums (v0)

### visual_medium_type
Allowed examples (expandable later):
- `none`
- `photo`
- `poster`
- `framed_picture`
- `phone_screen`
- `computer_screen`
- `tv_screen`
- `projection_screen`
- `advertisement_board`
- `book_or_magazine_cover`
- `glass_reflection`
- `mirror_reflection`
- `unknown_visual_medium`

### depicted_scene
Allowed examples (expandable later):
- `none`
- `beach`
- `kitchen`
- `hospital`
- `metro_station`
- `office`
- `mall`
- `street`
- `landscape`
- `unknown_depicted_scene`

### conflict_type
- `depicted_scene_conflict`
- `reflection_conflict`
- `screen_content_conflict`
- `advertisement_content_conflict`
- `unknown_conflict`

### filter_action
- `keep_previous_macro_scene`
- `mark_as_depicted_scene_only`
- `pass_to_scene_context_as_candidate`
- `uncertain_degraded`

## visual_medium_filter_output (object schema)
Required fields (v0):
- `visual_medium_context_id` (string)
- `visual_medium_detected` (bool)
- `visual_medium_type` (enum)
- `medium_boundary_detected` (bool)
- `flat_surface_likelihood` (0..1)
- `reflection_likelihood` (0..1)

- `depicted_scene` (enum)
- `depicted_scene_confidence` (0..1)

- `real_world_scene_evidence` (object)
- `macro_scene_transition_allowed` (bool)
- `task_trigger_allowed` (bool)
- `risk_trigger_allowed` (bool)

- `current_macro_scene` (string; may be `unknown_macro_scene`)
- `previous_macro_scene` (string; may be `unknown_macro_scene`)

- `conflict_detected` (bool)
- `conflict_type` (enum)

- `action` (enum filter_action)
- `reason_codes` (list<string>; non-empty)
- `allows_execute_now` (bool; must be false)

### real_world_scene_evidence (object, minimal)
Required fields:
- `spatial_layout_consistency` (0..1)
- `depth_or_parallax_support` (0..1)
- `fov_scene_consistency` (0..1)
- `sustained_duration_ms` (int)
- `transition_evidence_present` (bool)
- `scene_context_001_policy_required` (bool; must be true)

## Hard invariants (must be enforceable downstream)
- `allows_execute_now=false`.
- If `visual_medium_detected=true` AND `depicted_scene != none`:
  - `macro_scene_transition_allowed=false` (default)
  - `task_trigger_allowed=false`
  - `risk_trigger_allowed=false`
  - unless explicitly cleared by strong real_world_scene_evidence AND SceneContext-001 transition policy.
- depicted_scene may be recorded as `visual_content_candidate`, but cannot become a real-world trigger.

