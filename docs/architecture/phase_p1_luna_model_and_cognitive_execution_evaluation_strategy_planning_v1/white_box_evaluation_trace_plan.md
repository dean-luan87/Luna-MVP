# White-box Evaluation Trace Plan

Machine-readable trace is planned before any White-box UI. Existing nodes are
referenced; absent runtime nodes are not fabricated.

| Node / edge | Current status | Existing evidence |
|---|---|---|
| Goal / Intent / Concern | Partially observable | RF-DETR request/summary refs; no unified evaluation node. |
| Context / Field / Role | Partially observable | Current World candidate refs and context/field fields. |
| Observation Demand | Currently observable in controlled FPO assets | `ObservationDemandCandidateV1`, information-gap path. |
| Observation Request | Currently observable | `ObservationRequestCandidateV1` and RF-DETR request refs. |
| Capability Requirement | Currently observable at governed seam | `CapabilityRequirementCandidateV1` and capability registry refs. |
| Model Resolution | Partially observable | Model registry/binding and real RF-DETR lineage. |
| Provider Resolution | Partially observable | Provider registry/binding and provider admission candidate. |
| Observation | Partially observable | Provider request and Gateway handoff; full lifecycle is not unified. |
| Evidence | Currently observable | normalized visual evidence candidates. |
| Evidence quality/conflict/missing | Partially observable | sufficiency fields, uncertainty/conflict refs, failure taxonomy. |
| Current World Candidate | Currently observable | RF-DETR cognitive bridge output; candidate-only. |
| Hypothesis | Currently observable as candidate | `CognitiveHypothesisCandidateV1`; A-owned semantics. |
| Sufficiency | Currently observable as candidate | `EvidenceSufficiencyCandidateV1`. |
| Information Gap | Currently observable in controlled path | information-gap detector and sufficiency refs. |
| Re-observation | Partially observable | policy and `NextCycleIngressCandidateV1`; real automatic cycle is out of scope. |
| Decision Governance handoff | Partially observable | `next_target`/handoff refs; adapter does not own Decision. |
| Result / closure | Partially observable | result envelopes, evaluation reports, TestBoard evidence. |

## Trace contract shape

Each future evaluation profile should carry `trace_id`, parent transition refs,
node status, input/output refs, source versions, provenance, failure/gap refs,
and candidate/admission/execution flags. A node marked unavailable must carry
an explicit reason rather than a synthetic success node.

## UI boundary

This phase defines the data surface only. Model Test Lens may later visualize
it, but the evaluation trace must remain usable without a UI.
