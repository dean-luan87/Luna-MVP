# LUNA — Real Perception Model Integration Readiness Definition v0 (Phase-ModelPerception-001)

## Phase
- Phase: **Phase-ModelPerception-001**
- Type: **Definition-only (no runtime, no model calls)**

## One thing only (scope)
Define **Real Perception Model Integration Readiness** to prepare a future phase where:
- PerceptionEval-001 `baseline/mock` perception source can be **replaced** by a real perception model output,
while strictly preserving:
- candidate-only boundaries
- evidence boundary and replay/auditability
- disable/fallback/rollback-to-baseline
- mandatory SceneContext gates (001/002/003)

This phase produces **contracts and policies only**.

## Established facts (inputs)
- PhoneLocalReview-002: FieldBatch-002 accepted as Option A phone_local baseline v0.
- EndToEndOfflineEval-001: offline chain is closed (candidate-only; baseline/mock chain in effect).
- PerceptionEval-001: CONDITIONAL_GO (baseline_or_mock).
- SceneTask/Fusion/Output: CONDITIONAL_GO (baseline_or_mock_downstream).
- SceneContext-001: GO (continuity & zone reasoning).
- SceneContext-002: GO (visual medium & depicted scene filter).
- SceneContext-003: GO (physics-aware consistency).

## Goals (must be satisfied by definition)
Answer:
1. What model class can be integrated (at the boundary level; model choice deferred).
2. What inputs the model is allowed to read.
3. What perception signals the model must output.
4. How raw outputs are mapped via adapter into Perception-001 five signal categories.
5. How outputs are gated by SceneContext-001/002/003 (no bypass).
6. How failures/timeouts/forbidden outputs fall back to baseline/mock.
7. How admission tests are run on phone_local baseline.
8. What conditions allow entering ModelPerception-002 implementation.

## Hard boundaries (must be written as invariants)
- No runtime model integration; no model invocation.
- Model output is **perception candidate/signal only**.
- Model must not trigger `execute/release/retry/reopen`.
- Model must not open default path; must not expand side effects surface.
- Model must not directly output scene/task/fusion/output.
- Model output must not be treated as governance conclusion.
- Model must be **disable-able**.
- Model must be **rollback-able** to baseline/mock.
- Inputs/outputs must be **auditable and replayable**.
- Must not bypass SceneContext-001/002/003 gates.
- Must not change evidence types or evidence workflows.

## Layer position (frozen principle)
Perception source (baseline/mock OR real model via adapter)  
→ Perception Signals (5 categories, normalized)  
→ SceneContext-002 (depicted scene filter)  
→ SceneContext-003 (physics consistency)  
→ SceneContext-001 (continuity & zone reasoning)  
→ SceneTask → Fusion → Output Candidate

## Deliverables (required files)
1. `docs/architecture/LUNA_REAL_PERCEPTION_MODEL_INPUT_OUTPUT_CONTRACT_V0.md`
2. `docs/architecture/LUNA_REAL_PERCEPTION_MODEL_ADAPTER_AND_FALLBACK_POLICY_V0.md`
3. `docs/architecture/LUNA_REAL_PERCEPTION_MODEL_SCENECONTEXT_GATE_POLICY_V0.md`
4. `docs/architecture/LUNA_REAL_PERCEPTION_MODEL_ADMISSION_TEST_MATRIX_V0.md`
5. `docs/architecture/LUNA_REAL_PERCEPTION_MODEL_READINESS_GO_NO_GO_PACK_V0.md`
6. Update `docs/architecture/README.md`

## Stop condition
Stop when deliverables above are complete, mutually consistent, and preserve all invariants.

