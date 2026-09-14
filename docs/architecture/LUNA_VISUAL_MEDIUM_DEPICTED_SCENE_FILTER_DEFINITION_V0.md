# LUNA — Visual Medium & Depicted Scene Filter Definition v0 (Phase-SceneContext-002)

## Phase
- Phase: **Phase-SceneContext-002**
- Type: **Definition-only (no runtime)**

## One thing only (scope)
Define **Visual Medium & Depicted Scene Filter** to prevent the system from mistaking:
- **scene inside an object** (photo/screen/poster/ad/book cover/mirror/glass reflection)
as
- **real world scene** (真实世界可行动的 macro_scene / zone reasoning)

## Layer position (frozen)
Perception Signals  
→ **Visual Medium & Depicted Scene Filter**  
→ Scene Continuity & Zone Reasoning (SceneContext-001)  
→ Scene State  
→ Task Candidate  
→ Fusion / Output Candidate

## Current established facts (inputs)
- EndToEndOfflineEval-001 completed (offline candidate chain closed; baseline_or_mock).
- SceneContext-001 completed and **GO** (macro/zone separation, inertia, transition evidence gating, degraded fallback).

## Problems this phase must address (explicit)
- Photo beach → mistaken as real beach
- Screen kitchen → mistaken as real kitchen
- Poster hospital → mistaken as current hospital
- Ads (mall/metro/scenic spot) → mistaken as current macro_scene
- Mirror/glass reflection → spatial misinterpretation / macro jump
- Phone/PC/TV/projector content → induces macro_scene flip

## Goals (must all be satisfied by definition)
1. Distinguish `real_world_scene` vs `depicted_scene`.
2. Identify visual media types: photo/poster/screen/ad/glass_reflection/mirror/book_cover.
3. Block depicted_scene from directly overriding `macro_scene`.
4. Block depicted_scene from triggering **task/risk/navigation action**.
5. Record medium content as **whitebox** `visual_content_candidate`.
6. On conflict: keep `previous_macro_scene` or enter `uncertain_scene` / degraded mode.
7. Output is **candidate-only**; `allows_execute_now=false`.

## Hard boundaries (must be written as invariants)
- **scene inside object cannot become real_world_scene**.
- **depicted_scene must not directly override macro_scene**.
- depicted_scene must not trigger `execute/release/retry/reopen`.
- depicted_scene must not trigger real navigation task.
- depicted_scene must not trigger real risk task.
- filter outputs only `filter/candidate` signals; no execution authority.
- low confidence/conflict must degrade OR keep previous macro_scene.
- must not change `evidence_type` or evidence collection workflow.
- must not bypass SceneContext-001 policy.
- must not claim real visual-medium detection is validated.

## Non-goals (explicit)
- No runtime code, no integration, no model wiring.
- No new evidence type.
- No new Option A behaviors.
- No controlled_live_stream, no full controlled trial, no real user testing.

## Deliverables (required files)
1. `docs/architecture/LUNA_VISUAL_MEDIUM_DEPICTED_SCENE_SCHEMA_V0.md`
2. `docs/architecture/LUNA_VISUAL_MEDIUM_SCENE_GROUNDING_POLICY_V0.md`
3. `docs/architecture/LUNA_VISUAL_MEDIUM_DEPICTED_SCENE_TEST_MATRIX_V0.md`
4. `docs/architecture/LUNA_VISUAL_MEDIUM_DEPICTED_SCENE_GO_NO_GO_PACK_V0.md`
5. Update `docs/architecture/README.md`

## Stop condition
Stop when deliverables above are complete and internally consistent with SceneContext-001 constraints.

