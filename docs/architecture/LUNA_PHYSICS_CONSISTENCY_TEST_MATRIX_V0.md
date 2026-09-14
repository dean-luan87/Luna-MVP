# LUNA — Physics Consistency Test Matrix v0 (Phase-SceneContext-003)

## Purpose
Matrix physical inconsistency cases and expected outputs of `physics_consistency_signal`.
This is definition-only; it specifies expected flags/handling, not numeric threshold calibration.

## Case format (v0)
Each case includes:
- upstream signals (conceptual): object tracks, depth estimates, motion cues, passability cues
- expected:
  - `conflict_detected`
  - `conflict_type`
  - `physical_plausibility`
  - `consistency_level`
  - `recommended_handling`
  - key constraints (no execute, no forced action)

## Cases (A–J) — must cover

### A. Object position jump
- scenario: same obstacle track jumps laterally between adjacent frames without corresponding camera motion
- expected:
  - conflict_detected=true
  - conflict_type=object_position_jump
  - physical_plausibility=uncertain
  - recommended_handling=downgrade_confidence (or ignore_as_unstable)

### B. Depth jump
- scenario: obstacle distance 2m → 10m → 1m within short window
- expected:
  - conflict_type=depth_jump
  - depth_stability_score low
  - passability not confirmed from this obstacle/boundary
  - recommended_handling=mark_uncertain or degraded_mode

### C. Impossible moving pedestrian
- scenario: pedestrian horizontal position changes too fast to be continuous
- expected:
  - conflict_type=impossible_motion
  - motion_plausibility_score low/uncertain
  - recommended_handling=mark_uncertain
  - no forced avoidance action implied

### D. Fast approaching bicycle
- scenario: dynamic target distance shrinking fast with consistent trajectory
- expected:
  - collision_risk_consistency_score high
  - physical_plausibility=plausible
  - recommended_handling=keep_candidate
  - downstream allowed only: slow_down_candidate (still non-executing)

### E. Static poster mistaken as open path
- scenario: screen/poster shows corridor-like content; depth/parallax indicates flat plane
- expected:
  - conflict_type=flat_surface_depth_conflict
  - parallax_conflict may be present
  - recommended_handling=degraded_mode or ignore_as_unstable
  - real path not confirmed

### F. Narrow passage geometry
- scenario: left/right boundaries close; width below comfortable margin; near-field clutter
- expected:
  - passability_geometry_score low/medium
  - conflict_type=passability_geometry_conflict
  - recommended_handling=mark_uncertain (narrow_candidate downstream)

### G. Clear sidewalk geometry
- scenario: ground continuous; no near-field obstacles; stable depth; stable tracks
- expected:
  - physical_plausibility=plausible
  - consistency_level=high/medium
  - recommended_handling=keep_candidate

### H. Low confidence depth unavailable
- scenario: no reliable depth (low light / motion blur); object tracks unstable
- expected:
  - physical_plausibility=not_available or uncertain
  - consistency_level=unknown/low
  - recommended_handling=degraded_mode or ask_for_help_candidate

### I. Conflicting risk classification
- scenario: object class is “low risk” but relative motion suggests imminent collision
- expected:
  - conflict_type=collision_risk_conflict
  - collision risk candidate elevated (still non-executing)
  - recommended_handling=downgrade_confidence (on class) + keep risk candidate

### J. Mirror/reflection with inconsistent parallax
- scenario: reflected corridor appears but parallax/depth inconsistent with real space
- expected:
  - conflict_type=parallax_conflict (and/or flat_surface_depth_conflict)
  - recommended_handling=uncertain_degraded or ignore_as_unstable
  - must not enable macro_scene switching by itself

