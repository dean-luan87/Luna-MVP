# LUNA — Real Perception Model SceneContext Gate Policy v0 (Phase-ModelPerception-001)

## Purpose
Define the non-bypassable gate policy:
Real model perception outputs must pass through SceneContext defenses before downstream use.

This policy ensures:
- model cannot directly feed SceneTask/Fusion/Output
- model cannot override semantic safety constraints
- gates remain candidate-only and auditable

Definition-only; no runtime.

## Hard constraints (must be written as invariants)
- Model outputs must NOT go directly to SceneTask.
- Model outputs must pass all three gates:
  1. SceneContext-002: Visual Medium & Depicted Scene Filter
  2. SceneContext-003: Physics-Aware Perception Consistency
  3. SceneContext-001: Scene Continuity & Zone Reasoning
- Any gate may return `not_available/uncertain/degraded`, which must be respected downstream.
- Gates output **signals/candidates only**, never executable actions.
- Gate ordering in implementation may vary due to data flow, but:
  - the three defenses must all be present
  - absence requires explicit `not_available` + fallback to baseline/mock if safety cannot be asserted

## Recommended dataflow (principle)
Raw model output  
→ Adapter normalization (Perception-001 five signals)  
→ SceneContext-002 (depicted scene guard)  
→ SceneContext-003 (physics plausibility guard)  
→ SceneContext-001 (continuity + macro/zone reasoning)  
→ SceneTask/Fusion/Output Candidate

## Gate outcomes and allowed downstream effects
### SceneContext-002 blocks depicted content
If `visual_medium_detected=true` and `depicted_scene != none`:
- macro_scene transition must be blocked by default
- task/risk triggers must be blocked (candidate-only record allowed)

### SceneContext-003 blocks implausible physics
If `physical_plausibility in {implausible, uncertain}`:
- recommended_handling must degrade/uncertain
- cannot promote to certain passability or certain risk

### SceneContext-001 blocks macro flips and local overrides
- local objects cannot directly override macro_scene
- macro_scene transitions require transition evidence + inertia rules

## Non-bypass enforcement (definition)
Integration design must include a check that fails closed:
- If a pipeline path tries to feed SceneTask without gate artifacts, it must be treated as invalid and fall back to baseline/mock.

## Claims boundary
This policy does not claim model correctness.
It defines mandatory safety gating and audit constraints.

