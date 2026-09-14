# Cognition Runtime Reachability Audit

| Node / transition | Classification | Evidence |
|---|---|---|
| Goal / Concern / Intent | `PARTIALLY_OBSERVABLE` | Refs exist in controlled traces and FPO inputs; no registered-case runtime entry. |
| Context / Role / Field | `IMPLEMENTED_NOT_CONNECTED` | A-Route request fields and candidate inputs exist; real case-to-context connection is absent. |
| Attention | `EXISTS_BUT_SYNTHETIC_ONLY` | `CognitiveStateFormationEngineV1` is documented as a synthetic-only deterministic placeholder. |
| Information Need | `EXISTS_BUT_SYNTHETIC_ONLY` | FPO and cognitive-analysis candidates exist; no real producer is evidenced. |
| Observation planning | `PARTIAL` | FPO goal/capability planning helpers exist; not a general cognitive runtime. |
| Capability requirement/resolution | `PARTIAL` | Governance records and provider paths exist; case-to-resolution runtime not proven. |
| Observation/Evidence | `PARTIAL` | Real RF-DETR evidence exists narrowly; general runtime ingress absent. |
| Current World | `EXISTS_BUT_SYNTHETIC_ONLY` | Candidate types/controlled formation exist; no real A-route chain. |
| Hypothesis | `EXISTS_BUT_SYNTHETIC_ONLY` | Candidate and cognitive-analysis types exist; runtime formation not proven. |
| Sufficiency/Information Gap | `EXISTS_BUT_SYNTHETIC_ONLY` | Evidence-coverage and FPO gap helpers exist; no general real source. |
| Re-observation | `PARTIAL` | Policy and NextCycle candidates exist; real loop not established. |
| Stop / Decision handoff | `PARTIAL` | Narrow RF-DETR handoff target is observed; general handoff is not. |

`ARouteOrchestrationEngineV1` explicitly requires `synthetic_only` and `candidate_only` for its controlled path and has a deferred real-ingress branch. This is direct evidence against claiming real runtime reachability.

