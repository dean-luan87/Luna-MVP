# Cognitive Analysis Controlled DryRun Plan v1

## 1. Planning-only purpose

This plan reserves a future fixture-only, deterministic DryRun. It does not
create a runner, verifier, fixture, implementation, model call, runtime, or
test. All future cases must consume a fixed Current Cognitive Context and must
prove that A3 cannot write Field State or execute observation/action.

## 2. Fixture principles

- Fixtures provide immutable Context inputs with declared source Snapshot,
  provenance, trace, lifecycle, gaps, and sufficiency.
- Expected objects are planned candidates, never Facts, State changes, or
  Actions.
- Each case must record an expected status, expected warning/failure where
  relevant, a negative guard, and a stop condition.
- No case may access Raw Observation, Reducer internals, external models,
  database, network, camera, OCR, SLAM, or runtime services.

## 3. Fixed future cases

| Case | Fixture input | Expected objects / status | Expected warning or failure | Negative guard | Stop condition |
| --- | --- | --- | --- | --- | --- |
| 1. Supported single hypothesis | Sufficient current Context; one explanation has complete supporting evidence and no material contradiction. | Admission `admitted`; Frame; one `supported` Hypothesis; sufficient Result, still candidate-only. | No warning required. | No Fact/State/Decision/Action emitted. | Stop after candidate Result is recorded. |
| 2. Competing hypotheses | Sufficient Context; two explanations receive partial support. | Two Hypotheses; Competing Set `unresolved`; Result `provisional` or `incomplete`. | `competing_hypotheses_unresolved`. | No forced dominant candidate. | Stop with both hypotheses preserved. |
| 3. Contradicted evidence | Context contains evidence contradicting an earlier proposed explanation. | Evidence Assessment `contradicts`; Hypothesis `contradicted` or `underdetermined`; reassessed Result. | `evidence_conflict`. | Contradicted Evidence remains referenced. | Stop after downgrade; no deletion. |
| 4. Insufficient Context | Context Sufficiency is insufficient or a critical gap blocks analysis. | Admission `blocked`; no valid conclusion; Gap Refinement if needed. | `context_insufficient` or `critical_information_gap`. | No Frame/Result presented as complete. | Stop at block. |
| 5. Revoked evidence | Previously usable Evidence is revoked in Context lifecycle information. | Admission conditional/blocked; affected assessment `revoked`; Result `stale` or refresh-required. | `evidence_revoked`, `context_refresh_required`. | No historical result deletion. | Stop after refresh requirement is recorded. |
| 6. Unknown time | Context has temporal uncertainty material to the question. | Admission `conditionally_admitted`; temporal assessment unknown; Result conditionally sufficient or unknown. | `temporal_validity_unknown`. | Unknown time is not filled with a timestamp. | Stop without a current factual claim. |
| 7. Gap-to-observation request | Context exposes a material information gap. | Gap Refinement plus Observation Request Candidate. | `critical_information_gap` if blocking. | No Camera/OCR/SLAM/Network/Model invocation. | Stop when the request candidate is emitted. |
| 8. State-writeback attempt | Candidate analysis tries to express a world update. | Permission boundary blocks writeback; optional Field Event Candidate is only a future candidate. | `analysis_blocked` / permission violation. | No State/Version/Transition/Snapshot mutation. | Stop at boundary block. |

## 4. Future validation scope

Future controlled validation must check object/reference completeness,
admission/sufficiency status, unknown preservation, candidate-only outputs,
absence of external execution, and absence of every A1/A2 writeback route. It
must not claim semantic truth, production readiness, or Phase GO.
