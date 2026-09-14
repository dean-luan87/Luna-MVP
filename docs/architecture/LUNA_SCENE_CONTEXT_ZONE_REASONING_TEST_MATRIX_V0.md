# LUNA — SceneContext Zone Reasoning Test Matrix v0 (Phase-SceneContext-001)

## Purpose
Matrix continuous-scene misclassification cases to validate the **definition**:
- local objects → zone candidate (not macro switch)
- macro switches require transition evidence
- inertia blocks rapid flips
- task context constrains interpretation
- low confidence/conflict → uncertain/degraded

Definition-only; no runtime.

## Case format (v0)
Each case must specify:
- `previous_macro_scene`
- `local_object_cues`
- (optional) `transition_evidence`
- (optional) `task_context`
- expected:
  - `macro_scene` behavior
  - `zone_type`
  - `scene_transition_type`
  - `conflict_detected`
  - `degraded_mode`

## Cases (A–H)

### A. WeWork workspace → pantry (zone shift only)
- **previous_macro_scene**: `coworking_space`
- **local_object_cues**: `coffee_machine`, `sink`, `cups`
- **expected**
  - macro_scene remains `coworking_space`
  - zone_type = `pantry_area`
  - scene_transition_type = `zone_shift`
  - conflict_detected = false
  - degraded_mode = false

### B. WeWork pantry → workspace (zone shift only)
- previous_macro_scene: `coworking_space`
- local_object_cues: `desk`, `monitor`, `chair`
- expected:
  - macro_scene remains `coworking_space`
  - zone_type = `workspace_area`
  - scene_transition_type = `zone_shift`

### C. Hospital waiting area (chairs/queue/screen are not living_room)
- previous_macro_scene: `hospital` (or macro candidate supported by signage)
- local_object_cues: `chairs`, `queue`, `screen`
- expected:
  - macro_scene = `hospital`
  - zone_type = `waiting_area`
  - not `residential_home`

### D. Metro station commercial corridor (ads do not imply mall)
- previous_macro_scene: `metro_station`
- local_object_cues: `shops`, `signs`, `turnstile_nearby`, `ads`
- expected:
  - macro_scene remains `metro_station`
  - zone_type = `corridor` or `entrance_area` (depending on evidence)
  - not `shopping_mall` unless strong transition evidence exists

### E. Mall food court (tables/counters imply food_court zone)
- previous_macro_scene: `shopping_mall`
- local_object_cues: `tables`, `food_counters`, `trays`
- expected:
  - macro_scene remains `shopping_mall`
  - zone_type = `food_court_area`
  - not `residential_home` kitchen

### F. Home kitchen vs office pantry ambiguity (no prior macro)
- previous_macro_scene: `unknown_macro_scene`
- local_object_cues: `fridge`, `sink`
- expected:
  - macro_scene_candidate allowed but not confirmed
  - scene_transition_type = `macro_scene_candidate` or `uncertain_transition`
  - degraded_mode = true

### G. Sudden macro jump without transition evidence (block it)
- previous_macro_scene: `coworking_space`
- local_object_cues: `beach_image` (depicted content) or unrelated cues
- transition_evidence: none
- expected:
  - conflict_detected = true
  - macro_scene remains previous
  - scene_transition_type = `uncertain_transition` (blocked)

### H. Task context suppresses zone distraction (no task replacement)
- previous_macro_scene: `coworking_space`
- task_context: `find_meeting_room`
- local_object_cues: `coffee_machine`
- expected:
  - zone_type may become `pantry_area`
  - task_relevance = `path_context_only`
  - no task replacement / no new task insertion

