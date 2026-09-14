# LUNA — Visual Medium & Depicted Scene (SceneContext-002) Go/No-Go Pack v0

## Inputs (documents)
- Definition:
  - `docs/architecture/LUNA_VISUAL_MEDIUM_DEPICTED_SCENE_FILTER_DEFINITION_V0.md`
- Schema:
  - `docs/architecture/LUNA_VISUAL_MEDIUM_DEPICTED_SCENE_SCHEMA_V0.md`
- Grounding policy:
  - `docs/architecture/LUNA_VISUAL_MEDIUM_SCENE_GROUNDING_POLICY_V0.md`
- Test matrix:
  - `docs/architecture/LUNA_VISUAL_MEDIUM_DEPICTED_SCENE_TEST_MATRIX_V0.md`

## Decision
### Result
**GO**

### Why GO
- Distinguishes `depicted_scene` vs real-world grounding evidence.
- Freezes `visual_medium_type` and `depicted_scene` enums (v0 baseline; expandable).
- Writes hard constraints:
  - depicted_scene cannot override `macro_scene`
  - depicted_scene cannot trigger task/risk/navigation actions
  - conflict → keep previous macro_scene or degrade
- Explicitly requires SceneContext-001 transition policy for any macro_scene transition.
- Maintains candidate-only boundaries; `allows_execute_now=false`.
- No runtime code introduced.

## Go / Conditional-Go / No-Go criteria (frozen)
### GO
- schema complete (fields listed in schema doc)
- grounding policy includes:
  - photo/screen/poster/ad/book cover handling
  - mirror/glass reflection handling
  - conflict/degraded handling
  - explicit SceneContext-001 dependency
- test matrix covers A–I (poster/screen/ad/reflection + real doorway)
- explicit “no task/risk trigger” and “no execute/release/retry/reopen”
- **no runtime implementation**
- **no model integration**

### CONDITIONAL_GO
Allowed to defer:
- thresholds tuning
- enum extensions
- fine-grained reflected-content taxonomy
Must still be true:
- depicted_scene never overrides macro_scene
- depicted_scene never triggers task/risk
- conflict forces keep/degrade

### NO_GO
Any of:
- allows photo/screen/ad content to directly modify macro_scene
- allows depicted_scene to trigger task/risk/navigation action
- missing reflection/mirror policy
- missing hard invariants / `allows_execute_now=false`
- introduces runtime code / default path / user testing / model integration

## Hard blockers
- `[]`

## Soft follow-ups
- Expand `depicted_scene` taxonomy only if it improves auditability, not actionability.
- Define a dedicated “whitebox visual_content_candidate ledger” shape if needed (still non-actionable).

## Recommended next phase (do not auto-enter)
If you want to continue, pick one:
- **A. Phase-SceneContext-003 — Physics-Aware Perception Consistency Definition v0**
- **B. Phase-ModelPerception-001 — Real Perception Model Integration Readiness Definition v0**

## Explicit boundary re-statement (for audit)
- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- 未接真实模型
- 本阶段只定义 Visual Medium & Depicted Scene Filter，不实现 runtime

