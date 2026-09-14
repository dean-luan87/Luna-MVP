# LUNA — Physics Consistency (SceneContext-003) Go/No-Go Pack v0

## Inputs (documents)
- Definition:
  - `docs/architecture/LUNA_PHYSICS_AWARE_PERCEPTION_CONSISTENCY_DEFINITION_V0.md`
- Schema:
  - `docs/architecture/LUNA_PHYSICS_CONSISTENCY_SIGNAL_SCHEMA_V0.md`
- Policy:
  - `docs/architecture/LUNA_PHYSICS_CONSISTENCY_POLICY_V0.md`
- Test matrix:
  - `docs/architecture/LUNA_PHYSICS_CONSISTENCY_TEST_MATRIX_V0.md`

## Decision
### Result
**GO**

### Why GO
- Freezes `physics_consistency_signal` minimal schema (temporal/spatial/depth/motion/geometry/collision/parallax).
- Writes Rule 1–7 hard constraints:
  - physical conflicts force downgrade/uncertain/degraded handling
  - no forced certainty under low confidence
  - no execution semantics (`allows_execute_now=false`)
- Test matrix A–J covers core failure modes (jump/depth/motion/geometry/risk/flat-surface/parallax/reflection).
- Explicitly non-overriding: does not decide macro_scene; does not override SceneContext-001/002.
- No runtime code introduced; no model integration.

## Go / Conditional-Go / No-Go criteria (frozen)
### GO
- schema complete (fields/enums/invariants present)
- policy covers:
  - temporal/spatial continuity
  - depth stability
  - motion plausibility
  - passability geometry plausibility
  - collision risk relative-motion logic
  - flat-surface/parallax checks (including reinforcing depicted-scene safety)
  - downgrade rules under conflict/low confidence
- test matrix covers A–J
- candidate-only boundary explicit:
  - no execute/release/retry/reopen
  - no real navigation action output
- **no runtime implementation**
- **no real model integration**

### CONDITIONAL_GO
Allowed to defer:
- numeric threshold calibration
- detailed TTC computation and calibration
- fine-grained geometry scoring taxonomy
Must still be true:
- any key physics conflict forces downgrade/uncertain/degraded handling
- low confidence cannot force certainty
- this layer cannot trigger actions

### NO_GO
Any of:
- physics layer directly triggers actions or implies execution
- missing low-confidence downgrade requirement
- missing depth/motion/passability/collision (at least three) definitions
- allows implausible signals to pass as certain
- introduces runtime code / default-on behavior / user testing / model integration

## Hard blockers
- `[]`

## Soft follow-ups
- Define standardized “relative motion candidate” structure (still non-executing) for risk audit.
- Define how this layer references source ids across Perception + SceneContext-002 (id conventions), without changing evidence types.

## Recommended next phase (do not auto-enter)
- **Phase-ModelPerception-001 — Real Perception Model Integration Readiness Definition v0**

## Explicit boundary re-statement (for audit)
- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- 未接真实模型
- 本阶段只定义 Physics-Aware Perception Consistency，不实现 runtime

