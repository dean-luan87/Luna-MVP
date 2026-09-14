# LUNA — Scene Continuity & Zone Reasoning Definition v0 (Phase-SceneContext-001)

## Phase
- Phase: **Phase-SceneContext-001**
- Type: **Definition-only (no runtime)**

## Background (current facts)
- EndToEndOfflineEval-001 completed; Option A phone_local offline candidate chain is closed and traceable.
- Chain result: **CONDITIONAL_GO**, reason: `baseline_or_mock_chain_in_effect`.
- safety leakage = 0; evidence boundary preserved; candidate-only preserved; no-real-TTS preserved.

## Problem to solve (this phase)
Continuous-space misclassification in real environments (examples):
- In WeWork/coworking:
  - seeing desks ≠ “generic office macro_scene”
  - seeing coffee machine/fridge/sink ≠ “kitchen macro_scene”
- In hospital:
  - seeing chairs ≠ “living_room macro_scene”
- In metro station:
  - seeing billboard/photo ≠ “macro_scene switched”

Core principle:
**local object cues may produce zone candidates, but must not directly override macro_scene**.

## Layer position (frozen)
Perception Signals
→ **Scene Continuity & Zone Reasoning**
→ Scene State
→ Task Candidate
→ Fusion / Output Candidate

## Single goal
Define Scene Continuity & Zone Reasoning layer contracts to:
1. distinguish `macro_scene` and `zone_type`
2. introduce inertia (avoid frequent flips)
3. map local object cues to zone candidates (not macro_scene switches)
4. require strong transition evidence for macro_scene switching
5. define task-context constraints on scene interpretation
6. define uncertain/degraded fallback
7. output is candidate-only; no execution authority

## Hard boundaries (must remain true)
- No runtime implementation.
- No Option A expansion.
- No controlled_live_stream; no full controlled trial.
- No open user testing; no default-on.
- No side effects surface expansion.
- No navigation action execution; no real TTS.
- No real model integration.
- Must not claim real-world understanding validated.

## Deliverables (required files)
1. `docs/architecture/LUNA_SCENE_CONTEXT_MACRO_ZONE_SCHEMA_V0.md`
2. `docs/architecture/LUNA_SCENE_CONTEXT_TRANSITION_POLICY_V0.md`
3. `docs/architecture/LUNA_SCENE_CONTEXT_ZONE_REASONING_TEST_MATRIX_V0.md`
4. `docs/architecture/LUNA_SCENE_CONTEXT_GO_NO_GO_PACK_V0.md`
5. `docs/architecture/README.md` index update

## Go / Conditional-Go / No-Go
### GO
- macro/zone schema complete
- transition policy complete (Rule 1–6, transition evidence, degraded fallback)
- test matrix covers core cases (WeWork/hospital/metro/mall/home)
- candidate-only + no execute/release/retry/reopen boundaries explicit
- no runtime changes

### CONDITIONAL_GO
- enums and thresholds may be extended later
- test matrix may be expanded later
but must still lock:
- local objects cannot directly switch macro_scene
- macro_scene switching requires transition evidence
- low confidence must degrade/uncertain

### NO_GO
- allows single-frame object to override macro_scene
- no macro vs zone distinction
- no transition evidence definition
- no degraded/uncertain rule
- any executable output semantics
- any runtime added

## Stop condition
Stop when the deliverables above are complete.

