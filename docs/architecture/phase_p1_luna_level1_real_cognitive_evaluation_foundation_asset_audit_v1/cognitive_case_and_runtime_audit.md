# Cognitive Case and A-Route Runtime Audit

## Case composition

`compose_level1_cognitive_test_case_v1` accepts a `DatasetSampleManifestV1` and composes sample, task, Goal/Concern, Role, conditions, cognitive difficulty, perturbations, capability refs, observation budget, expected observation refs, layered GT refs, assertions, and optional trace/profile refs. It never loads media and rejects runtime-applied perturbations.

This is a reusable composition function, not a persisted Test Case Registry. It does not independently prove that the sample belongs to the current `DatasetRegistryV1`, and the Golden Corpus manifest intentionally has zero registered data. No second cognitive Test Case system should be created; the existing function should be extended later with explicit registry membership and case persistence if required.

## Runtime reachability matrix

| Cognitive node | Classification | Evidence |
|---|---|---|
| Goal / Concern / Intent | `PARTIALLY_OBSERVABLE` | Candidate refs occur in FPO/controlled traces; no general real A-Route entry from a registered case was found. |
| Context / Role / Field | `PARTIALLY_OBSERVABLE` | Candidate input fields and Current World refs exist; runtime state connection is not proven. |
| Attention | `IMPLEMENTED_NOT_CONNECTED` | Cognitive State Formation emits synthetic attention candidates; `CognitiveStateFormationEngineV1` is explicitly a synthetic-only placeholder. |
| Information Need | `IMPLEMENTED_NOT_CONNECTED` | Active observation controls and cognitive-analysis types carry candidate/ref concepts; no real end-to-end producer is evidenced. |
| Observation Demand / Request | `PARTIALLY_OBSERVABLE` | Existing FPO control types and Roboflow request path produce candidate/request artifacts. |
| Capability Requirement / Resolution | `PARTIALLY_OBSERVABLE` | Governance records and real provider smoke refs exist; general case-to-resolution runtime is not proven. |
| External Capability Invocation | `PARTIALLY_OBSERVABLE` | Real Roboflow RF-DETR smoke observed one provider invocation; it is a narrow precedent, not a general A-Route runtime. |
| Observation / Evidence | `PARTIALLY_OBSERVABLE` | Visual detection candidate and Gateway handoff contracts exist; real RF-DETR evidence is available only in the narrow PoC. |
| Relevance / Missing / Uncertainty / Conflict | `PARTIALLY_OBSERVABLE` | Roboflow cognitive adapter has evidence-coverage logic; no general A-route collector is established. |
| Current World Candidate | `IMPLEMENTED_NOT_CONNECTED` | Candidate type and controlled formation exist; not proven as output of a real registered-case cognitive run. |
| Hypothesis / Revision | `IMPLEMENTED_NOT_CONNECTED` | Candidate types, cognitive-analysis types, and synthetic fixtures exist; general runtime formation is not proven. |
| Sufficiency | `IMPLEMENTED_NOT_CONNECTED` | Candidate and structural evidence-coverage assessment exist; no general real A-route source is proven. |
| Information Gap / Re-observation | `PARTIALLY_OBSERVABLE` | FPO policy and NextCycle candidates exist; autonomous or general runtime loop is not evidenced. |
| Stop Reason | `SCHEMA_ONLY` | White-box node/profile support exists; no general runtime producer. |
| Decision Governance handoff | `PARTIALLY_OBSERVABLE` | RF-DETR smoke ended at `next_target=Decision Governance`; downstream Decision authority is not owned by the PoC. |
| Result / Closure | `SCHEMA_ONLY` | Controlled execution/report artifacts exist; no durable cognitive evaluation result archive. |

## Important distinction

The presence of a type, controlled engine, or RF-DETR smoke result does not establish a real Level-1 cognitive runtime. The current evidence supports “narrow real provider-to-candidate precedent” and “synthetic/candidate cognitive foundation,” not `IMPLEMENTED_AND_RUNTIME_REACHABLE` for the full chain.

