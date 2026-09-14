# Canonical A-Route Path Map

| Transition | Canonical owner | Source → target | Status | Evidence / missing contract |
|---|---|---|---|---|
| T1 | Evaluation Governance | Registry entry → Sample | `EXISTS_BUT_EVALUATION_ONLY` | `DatasetRegistryV1` and `DatasetSampleManifestV1`; current declaration is empty. |
| T2 | Evaluation Governance | Sample → Level-1 Case | `EXISTS_BUT_EVALUATION_ONLY` | `compose_level1_cognitive_test_case_v1`; explicit sample input, no real sample currently. |
| T3 | Evaluation Governance | Case → Run boundary | `EXISTS_BUT_EVALUATION_ONLY` | `validate_registered_case_inputs_v1`; candidate validation only. |
| T4 | Observation/FPO | Sample/recorded input → Observation/Evidence input | `PARTIAL` | Raw frame, FPO, RF-DETR, and replay-ref precedents exist; common case ingress is not connected. |
| T5 | Evidence/Gateway | Observation/Evidence → admitted cognitive evidence | `PARTIAL` | Visual Evidence and Gateway handoff candidates exist; general admission/runtime handoff is not proven. |
| T6 | Observation/FPO → A-Route | Admitted evidence → A-Route ingress | `EXISTS_BUT_NOT_CONNECTED` | `ARouteIngressRefsV1` carries observation/perception refs, but no real evidence consumer is demonstrated. |
| T7 | A / Cognitive Governance | A-Route ingress → Goal/Concern cognition | `EXISTS_BUT_SYNTHETIC_ONLY` | `ARouteOrchestrationEngineV1` rejects non-synthetic controlled requests; no real ingress proof. |
| T8 | A | Cognitive execution → Current World Candidate | `EXISTS_BUT_SYNTHETIC_ONLY` | Candidate type and Cognitive State Formation output exist; engine is synthetic-only. |
| T9 | A | Current World Candidate → Hypothesis | `EXISTS_BUT_SYNTHETIC_ONLY` | `CognitiveHypothesisCandidateV1` exists; runtime connection absent. |
| T10 | A | Hypothesis → Sufficiency/Gap | `EXISTS_BUT_SYNTHETIC_ONLY` | Sufficiency and information-gap candidates/helpers exist; no real A-route source. |
| T11 | Observation/FPO + A | Gap → Re-observation | `PARTIAL` | Re-observation policy and NextCycle candidates exist; autonomous/general loop unproven. |
| T12 | A | Sufficiency → Stop | `EXISTS_BUT_SYNTHETIC_ONLY` | Stop-condition helpers and trace nodes exist; no general runtime producer. |
| T13 | Decision Governance | Stop/result → Decision handoff | `PARTIAL` | RF-DETR smoke reaches Decision Governance target; no general A-route handoff. |
| T14 | Evaluation | Cognitive execution → White-box Trace V1 | `EXISTS_BUT_EVALUATION_ONLY` | V1 trace and synthetic fixtures exist; runtime collector absent. |
| T15 | Evaluation | Cognitive execution → Profile V1 | `EXISTS_BUT_EVALUATION_ONLY` | Profile adapter consumes supplied trace; no runtime event integration. |
| T16 | Evaluation | Failure/gap → Gap Ref V1 | `EXISTS_BUT_EVALUATION_ONLY` | V1 gap contract/validator exists; runtime attribution absent. |
| T17 | Evaluation Governance | White-box artifacts → Run result | `EXISTS_BUT_EVALUATION_ONLY` | Run boundary/archive bridge can attach references; not real-run evidence. |
| T18 | Evaluation Governance | Run → Durable Archive | `EXISTS_BUT_EVALUATION_ONLY` | `evaluation_archive/level1_cognitive_runs/` writer exists; real archive population not verified. |

No transition justifies Evaluation owning cognition or Field mutation.

