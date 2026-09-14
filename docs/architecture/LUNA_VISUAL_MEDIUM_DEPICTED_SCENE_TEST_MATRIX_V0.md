# LUNA — Visual Medium & Depicted Scene Test Matrix v0 (Phase-SceneContext-002)

## Purpose
Matrix cases that previously caused macro_scene jumps due to depicted content:
- photo/screen/poster/ad/book cover
- mirror/glass reflections
and define expected filter outputs that protect SceneContext-001.

Definition-only; no runtime.

## Case format (v0)
Each case specifies:
- `previous_macro_scene`
- `visual_medium_type` + likelihood cues
- `depicted_scene` content
- (optional) `real_world_scene_evidence`
- expected:
  - `macro_scene_transition_allowed`
  - `task_trigger_allowed`
  - `risk_trigger_allowed`
  - `action`
  - conflict fields

## Cases (A–I) — must cover

### A. Office beach poster
- previous_macro_scene: `coworking_space`
- visual_medium_type: `poster`
- depicted_scene: `beach`
- expected:
  - visual_medium_detected=true
  - macro_scene_transition_allowed=false
  - task_trigger_allowed=false
  - risk_trigger_allowed=false
  - action=keep_previous_macro_scene
  - conflict_detected=true
  - conflict_type=depicted_scene_conflict

### B. Office kitchen photo (framed picture)
- previous_macro_scene: `coworking_space`
- visual_medium_type: `framed_picture`
- depicted_scene: `kitchen`
- expected:
  - depicted_scene only; no macro switch to kitchen
  - action=mark_as_depicted_scene_only
  - macro_scene_transition_allowed=false

### C. Metro hospital advertisement
- previous_macro_scene: `metro_station`
- visual_medium_type: `advertisement_board`
- depicted_scene: `hospital`
- expected:
  - no hospital_navigation trigger
  - task_trigger_allowed=false
  - risk_trigger_allowed=false
  - action=keep_previous_macro_scene
  - conflict_type=advertisement_content_conflict

### D. Computer screen showing meeting room
- previous_macro_scene: `coworking_space`
- visual_medium_type: `computer_screen`
- depicted_scene: `office` (or `unknown_depicted_scene` if content ambiguous)
- expected:
  - screen_content_conflict
  - depicted_scene only
  - macro_scene_transition_allowed=false
  - action=mark_as_depicted_scene_only

### E. TV showing beach in home
- previous_macro_scene: `residential_home`
- visual_medium_type: `tv_screen`
- depicted_scene: `beach`
- expected:
  - no outdoor macro switch
  - no water_edge risk trigger
  - macro_scene_transition_allowed=false
  - risk_trigger_allowed=false

### F. Mirror reflection (reflected corridor visible)
- previous_macro_scene: `coworking_space`
- visual_medium_type: `mirror_reflection`
- depicted_scene: `office` (or `unknown_depicted_scene`)
- expected:
  - reflection_conflict
  - macro_scene_transition_allowed=false unless strong grounding evidence exists
  - action=uncertain_degraded

### G. Glass reflection in mall (reflected street appears)
- previous_macro_scene: `shopping_mall`
- visual_medium_type: `glass_reflection`
- depicted_scene: `street`
- expected:
  - macro_scene_transition_allowed=false
  - action=mark_as_depicted_scene_only OR uncertain_degraded
  - conflict_type=reflection_conflict

### H. Real doorway transition (no medium detected)
- previous_macro_scene: `coworking_space`
- visual_medium_type: `none`
- depicted_scene: `none`
- real_world_scene_evidence:
  - doorway/exit present
  - sustained multi-frame
  - spatial consistency high
- expected:
  - this layer does not decide macro switch
  - macro_scene_transition_allowed=true (meaning: allowed to pass to SceneContext-001 policy)
  - action=pass_to_scene_context_as_candidate
  - task_trigger_allowed remains false here (still candidate-only)

### I. Unknown flat image (medium likely but uncertain)
- previous_macro_scene: `metro_station`
- visual_medium_type: `unknown_visual_medium`
- depicted_scene: `unknown_depicted_scene`
- expected:
  - degraded
  - macro_scene_transition_allowed=false
  - task_trigger_allowed=false
  - risk_trigger_allowed=false
  - action=uncertain_degraded

