# LUNA — SceneContext-001: Scene Continuity & Zone Reasoning Definition v0

## Phase
- Phase: **Phase-SceneContext-001**
- Name: **Scene Continuity & Zone Reasoning Definition v0**
- Type: **Definition-only (no runtime)**

## Motivation (why now)
We have an end-to-end offline candidate chain closure (phone_local → perception → scene/task → fusion → output).  
Before integrating real perception models, we must define **real-world scene continuity guards** so that:
- local object recognition does not incorrectly imply global scene change
- office / WeWork / pantry / waiting area transitions are not over-triggered
- scene switching requires explicit transition evidence

This phase defines the contract and governance rules only.

## Single goal
Freeze a minimal, auditable definition for:
1. `macro_scene` + `zone_type` hierarchy (global vs local)
2. scene continuity inertia (do not flip scene rapidly)
3. “local objects must not override global scene” rule
4. scene transitions must be supported by **transition evidence**
5. an explicit interface point for **depicted-scene / visual-medium filtering** (detailed rules deferred to SceneContext-002)

## Hard boundaries (must remain true)
- No new runtime.
- No controlled_live_stream.
- No full controlled trial.
- No default-on.
- No expansion of real side effects surface.
- No navigation execution authority.
- No claims of real model capability validation.

## Scope (in-scope)
- Definitions for scene context representation:
  - `macro_scene`
  - `zone_type`
  - `scene_context_state` (persistent state across frames)
- Continuity rules:
  - inertia / hysteresis
  - transition evidence thresholds
- Conflict rules:
  - local-vs-global override constraints
- Outputs for downstream layers:
  - `scene_context_annotations` (candidate-only metadata to accompany perception/scene_state)

## Non-goals (explicit)
- No implementation of zone reasoning runtime.
- No training or evaluation of real perception models.
- No expanding scenario set beyond Option A baseline.
- No “live” execution, no audio output, no actions.

## Terms (v0)
- **macro_scene**: high-level environment class (e.g., `outdoor_sidewalk`, `indoor_office`, `indoor_waiting_area`, `unknown`).
- **zone_type**: sub-region within a macro scene (e.g., `pantry`, `open_office`, `corridor`, `lobby`, `sidewalk_segment`, `unknown`).
- **transition evidence**: signals that justify a macro_scene/zone change (e.g., sustained visual-medium cues, geometry shift, lighting profile change, sustained landmark pattern change).
- **depicted scene / visual medium**: content that is not the current physical scene (photos, screens, posters, billboards). Detailed filter rules are deferred to SceneContext-002.

## Deliverables (documents)
- Contract: `docs/architecture/LUNA_SCENE_CONTEXT_SCENE_CONTINUITY_AND_ZONE_REASONING_CONTRACT_V0.md`
- Decision pack: `docs/architecture/LUNA_SCENE_CONTEXT_SC001_BRANCH_DECISION_PACK_V0.md`
- README index update

## Go / No-Go (for definition phase)
### GO
- contract defines hierarchy + continuity + transition evidence gates
- depicted-scene filter interface is explicitly reserved for SceneContext-002
- no runtime changes

### NO_GO
- any attempt to introduce runtime behavior or expand scope

## Stop condition
Stop when the contract + decision pack + README index are complete.

