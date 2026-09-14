# LUNA — Real Perception Model Integration Readiness Go/No-Go Pack v0 (Phase-ModelPerception-001)

## Inputs (documents)
- Readiness definition:
  - `docs/architecture/LUNA_REAL_PERCEPTION_MODEL_INTEGRATION_READINESS_DEFINITION_V0.md`
- Input/output contract:
  - `docs/architecture/LUNA_REAL_PERCEPTION_MODEL_INPUT_OUTPUT_CONTRACT_V0.md`
- Adapter & fallback policy:
  - `docs/architecture/LUNA_REAL_PERCEPTION_MODEL_ADAPTER_AND_FALLBACK_POLICY_V0.md`
- SceneContext gate policy:
  - `docs/architecture/LUNA_REAL_PERCEPTION_MODEL_SCENECONTEXT_GATE_POLICY_V0.md`
- Admission test matrix:
  - `docs/architecture/LUNA_REAL_PERCEPTION_MODEL_ADMISSION_TEST_MATRIX_V0.md`

## Decision
### Result
**GO**

### Why GO
- Freezes strict model I/O boundaries (no governance/execute/default-path inputs; no executable outputs).
- Freezes forbidden-output blocking requirements and “block + fallback” behavior.
- Requires adapter normalization into Perception-001 five-signal shape with audit/replay artifacts.
- Requires disable switch + rollback-to-baseline.
- Writes non-bypassable SceneContext gate policy (002 → 003 → 001; ordering flexible but all required).
- Defines admission tests A–M covering malformed/forbidden/low-confidence/gate conflicts/fallback/audit/disable.
- No runtime, no model invocation, no Option A expansion.

## Go / Conditional-Go / No-Go criteria (frozen)
### GO
Allowed to enter ModelPerception-002 implementation only if:
- input/output contract is complete and forbids execute/default-path/governance override
- adapter/fallback policy complete (schema validation, forbidden scan, not_available, disable, rollback, replay/whitebox)
- SceneContext gate policy complete (no bypass of 001/002/003)
- admission test matrix complete (A–M)
- explicit candidate-only boundary remains intact
- **no runtime code in this phase**
- **no real model calls in this phase**

### CONDITIONAL_GO
May defer:
- exact model selection and model family taxonomy
- numeric thresholds for low-confidence/fallback rates
- staged capability rollout (OCR/depth/dynamic) in later phase
Must still be true:
- model has no execution authority
- model is disable-able and rollback-able
- all outputs pass SceneContext gates
- non-auditable runs are treated as no-go (fail closed)

### NO_GO
Any of:
- model can directly trigger actions or implies execution semantics
- model can bypass SceneContext gates
- model can enable default path / side effects surface expansion
- missing fallback or disable switch
- missing replay/whitebox audit artifacts
- input boundary leaks governance controls
- schema is uncontrolled / unmappable to five-signal contract
- any runtime model integration introduced in this definition phase

## Hard blockers
- `[]`

## Soft follow-ups
- Define a versioned “policy bundle id” that ties together:
  - adapter policy version
  - forbidden scan vocabulary version
  - SceneContext gate policy version
  (still definition-only; no runtime changes here)

## Recommended next phase (do not auto-enter)
- **Phase-ModelPerception-002 — Single Real Perception Model Shadow Integration Implementation v0**
  - constraints remain: shadow mode, candidate-only, no execute, no default-on, disable/fallback, replay/whitebox, admission tests on phone_local baseline.

## Explicit boundary re-statement (for audit)
- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- 未接真实模型（本阶段不调用模型）
- 本阶段只定义 Real Perception Model Integration Readiness，不实现 runtime

