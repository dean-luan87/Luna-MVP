# LUNA — Physics Consistency Signal Schema v0 (Phase-SceneContext-003)

## Purpose
Freeze the minimal schema for `physics_consistency_signal` so downstream layers can:
- audit physical plausibility decisions (whitebox)
- degrade/handle unstable perception outputs safely

Definition-only; no runtime.

## Enums (v0)

### physical_plausibility
- `plausible`
- `implausible`
- `uncertain`
- `not_available`

### consistency_level
- `high`
- `medium`
- `low`
- `unknown`

### conflict_type
- `object_position_jump`
- `depth_jump`
- `impossible_motion`
- `passability_geometry_conflict`
- `collision_risk_conflict`
- `flat_surface_depth_conflict`
- `parallax_conflict`
- `unknown_physics_conflict`

### recommended_handling
- `keep_candidate`
- `downgrade_confidence`
- `mark_uncertain`
- `degraded_mode`
- `ask_for_help_candidate`
- `ignore_as_unstable`

## physics_consistency_signal (object schema)
Required fields (v0):
- `physics_consistency_id` (string)
- `source_perception_signal_ids` (list<string>)
- `source_scene_context_ids` (list<string>)  # may include visual-medium context ids; can be empty list but must exist

- `temporal_continuity_score` (0..1)
- `spatial_consistency_score` (0..1)
- `depth_stability_score` (0..1)
- `motion_plausibility_score` (0..1)
- `passability_geometry_score` (0..1)
- `collision_risk_consistency_score` (0..1)
- `flat_surface_consistency` (0..1)
- `parallax_consistency` (0..1)

- `physical_plausibility` (enum)
- `consistency_level` (enum)

- `conflict_detected` (bool)
- `conflict_type` (enum)

- `recommended_handling` (enum)
- `confidence` (0..1)
- `reason_codes` (list<string>; non-empty)

- `allows_execute_now` (bool; must be false)

## Hard invariants (must be enforceable downstream)
- `allows_execute_now=false`.
- If `physical_plausibility in {implausible, uncertain}` OR `consistency_level in {low, unknown}`:
  - downstream must treat related candidates as non-final:
    - must degrade confidence, or mark uncertain/degraded
    - must not produce executable navigation actions
- If `conflict_detected=true`:
  - `recommended_handling` must NOT imply execution; it can only influence confidence and candidate suppression.

