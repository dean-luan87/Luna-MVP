# LUNA — SceneContext-001 Branch Decision Pack v0

## Pack intent
Consolidate SceneContext-001 definition + contract and record the branch decision.

Definition-only; no runtime changes.

## Inputs
- Definition:
  - `docs/architecture/LUNA_SCENE_CONTEXT_SCENE_CONTINUITY_AND_ZONE_REASONING_DEFINITION_V0.md`
- Contract:
  - `docs/architecture/LUNA_SCENE_CONTEXT_SCENE_CONTINUITY_AND_ZONE_REASONING_CONTRACT_V0.md`

## Decision
### Result
**GO**

### What is approved now
- Freeze `macro_scene` / `zone_type` hierarchy and `scene_context_state` v0 schema.
- Freeze continuity inertia rules and transition evidence gates.
- Freeze “local objects must not override global scene” rule.
- Freeze depicted-scene filter **interface** and its guard semantics.

### What is explicitly deferred
- **SceneContext-002**: Visual Medium & Depicted Scene Filter Definition v0
  - detailed classification of screen/photo/poster/billboard content
  - stronger rules for preventing depicted content from driving macro_scene transitions

### Recommended next phase
- **Phase-SceneContext-002: Visual Medium & Depicted Scene Filter Definition v0**

## Boundary statement (must remain true)
- No runtime implementation in SceneContext-001.
- No controlled_live_stream.
- No full controlled trial.
- No default-on.
- No expansion of real side effects surface.
- No claims of real model/navigation capability validation.

