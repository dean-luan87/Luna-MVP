# LUNA — Physics-Aware Perception Consistency Definition v0 (Phase-SceneContext-003)

## Phase
- Phase: **Phase-SceneContext-003**
- Type: **Definition-only (no runtime)**

## One thing only (scope)
Define **Physics-Aware Perception Consistency Layer** to check whether:
- perception signals and upstream context signals
are consistent with basic physical reality constraints (time/space/depth/motion/geometry),
and prevent downstream from being driven by discontinuous/unstable/implausible visual outputs.

## Layer position (recommended; frozen principle)
Perception Signals  
→ Visual Medium & Depicted Scene Filter (SceneContext-002)  
→ **Physics-Aware Perception Consistency** (this phase)  
→ Scene Continuity & Zone Reasoning (SceneContext-001)  
→ Scene State → Task Candidate → Fusion / Output Candidate

Note:
- Implementation may place this immediately after Perception Signals and before SceneContext, but must preserve semantics:
  - this layer **cannot** decide macro_scene
  - this layer **cannot** create executable actions
  - this layer outputs only consistency candidates and downgrade recommendations

## Established facts (inputs)
- EndToEndOfflineEval-001 completed (Option A phone_local offline candidate chain closed; baseline_or_mock).
- SceneContext-001 GO (macro/zone separation, inertia, transition evidence gating, degraded fallback).
- SceneContext-002 GO (depicted scene cannot trigger macro switches / task / risk).

## Problems this phase must address (explicit)
- Object position jumps across frames
- Unstable depth/distance estimates
- Dynamic target motion violates continuity/common sense
- Passability decision conflicts with geometry (width/boundaries/ground continuity)
- Risk judged by class only (ignoring relative distance/velocity/direction)
- Low-confidence signals without physical consistency constraints
- Plane/depth/parallax inconsistency causing space misunderstanding

## Goals (must be satisfied by definition)
1. Check temporal/spatial continuity across frames.
2. Check depth/distance stability.
3. Check motion plausibility for dynamic targets.
4. Check passability geometry plausibility (ground continuity, corridor width, boundaries).
5. Check collision/approach risk logic using relative motion candidates (TTC etc.).
6. Cross-check flat surface / parallax consistency, especially to avoid “screen corridor = real corridor”.
7. Degrade implausible/low-confidence outputs to `uncertain/degraded`.
8. Output **consistency candidates** only; no execution.

## Hard boundaries (must be written as invariants)
- Physics layer only outputs `consistency / plausibility / risk candidate` signals.
- Must not trigger `execute/release/retry/reopen`.
- Must not output real navigation actions.
- Must not override SceneContext-001/002 semantic rules.
- Must not decide `macro_scene` by itself.
- Must not change evidence types / evidence workflows.
- Must not bypass SceneTask/Fusion/Output.
- Must not claim real physics model capability validated.
- Under low confidence or physics conflict: must degrade (cannot force certainty).

## Deliverables (required files)
1. `docs/architecture/LUNA_PHYSICS_CONSISTENCY_SIGNAL_SCHEMA_V0.md`
2. `docs/architecture/LUNA_PHYSICS_CONSISTENCY_POLICY_V0.md`
3. `docs/architecture/LUNA_PHYSICS_CONSISTENCY_TEST_MATRIX_V0.md`
4. `docs/architecture/LUNA_PHYSICS_CONSISTENCY_GO_NO_GO_PACK_V0.md`
5. Update `docs/architecture/README.md`

## Stop condition
Stop when deliverables above are complete and internally consistent with SceneContext-001/002 constraints.

