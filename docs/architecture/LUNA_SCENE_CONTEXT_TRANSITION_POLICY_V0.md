# LUNA — SceneContext Transition Policy v0 (Phase-SceneContext-001)

## Purpose
Define the core rules that prevent continuous-space misclassification:
- local object cues → zone candidates (not macro switches)
- macro_scene switching requires strong transition evidence
- inertia/hysteresis blocks flip-flops
- task context constrains interpretation
- low confidence/conflict → degraded/uncertain output

Definition-only; no runtime.

## Core rules (must be written as hard constraints)

### Rule 1 — 局部物体不得直接覆盖 macro_scene
Local object cues (single-frame or short burst) may only produce:
- `zone_type` candidates or shifts
and must NOT directly confirm a macro_scene change.

Examples:
- `coffee_machine`, `sink`, `fridge`, `cups` → `pantry_area` candidate
  - must NOT switch macro_scene to `residential_home` kitchen
- `desk`, `monitor`, `chair` → `workspace_area` candidate
  - must NOT switch macro_scene to `office_building`

### Rule 2 — 优先在当前 macro_scene 内解释 zone
If `current_macro_scene=coworking_space`, then:
- coffee_machine → `pantry_area`
- desk/monitor → `workspace_area`
- glass_room → `meeting_room`
Instead of mapping to:
- kitchen / living_room / generic office.

### Rule 3 — macro_scene 切换必须有强转场证据
Macro_scene transitions must be gated by **transition evidence** that is:
- multi-source (≥ 2 evidence categories), AND
- sustained (multi-frame / time), AND
- consistent with spatial/temporal change, AND
- not contradicted by depicted-scene suspicion.

Minimal transition evidence categories (v0):
- **doorway/entrance/exit evidence**: doorway frames, turnstile, gate, elevator threshold, etc.
- **signage evidence**: sustained signage patterns consistent with new macro scene (e.g., hospital signage, metro platform signage).
- **spatial/layout evidence**: strong geometry shift (platform vs office corridor vs outdoor sidewalk).
- **temporal evidence**: sustained duration \(>=3000ms\) for macro scene candidate to become confirmed.

Hard rule:
- single-frame local objects are insufficient for macro_scene confirmation.

### Rule 4 — scene inertia
Inertia policy (v0 defaults):
- `macro_scene_min_dwell_ms=15000`
- `zone_min_dwell_ms=5000`
- `max_macro_flip_rate_per_minute=2`

If transition evidence is not strong:
- keep `previous_macro_scene`
- allow `zone_type` updates
- or output `uncertain_transition`

### Rule 5 — 任务上下文约束解释
If `task_context=find_meeting_room`:
- `pantry_area` must be treated as `path_context_only`
- must not replace the primary task
- must not auto-switch to a different task

### Rule 6 — 低置信/冲突时降级
If:
- zone candidates conflict strongly, OR
- macro_scene candidate lacks transition evidence, OR
- depicted-scene suspicion exists,
then:
- set `degraded_mode=true` and/or `scene_transition_type=uncertain_transition`
- restrict downstream to candidate-only safe set:
  - `observe_candidate`
  - `ask_for_help_candidate`

## Transition evidence record schema (v0)
Required fields:
- `evidence_id`
- `proposed_macro_scene`
- `proposed_zone_type`
- `evidence_strength`: `weak | medium | strong`
- `evidence_sources` (list)
- `sustained_duration_ms` (int)
- `reason_codes` (list)

Gate thresholds (v0):
- macro_scene_confirmed requires:
  - `evidence_strength=strong`
  - `sustained_duration_ms >= 3000`
  - `depicted_scene_suspected=false`
- zone_shift allows:
  - `evidence_strength in {medium,strong}`
  - `sustained_duration_ms >= 1500`

## Depicted scene interface note (SceneContext-002)
This policy reserves a hard guard:
- if `depicted_scene_suspected=true`, cap evidence_strength to `weak` for macro_scene switching until SceneContext-002 filter rules clear it.

