# Cognitive White-box Trace Plan

This is a machine-readable data plan, not a UI implementation.

| Node | Status | Reuse/evidence |
|---|---|---|
| Goal / Intent / Concern | partially_observable | Request and cognitive refs exist; no single unified A-route trace yet. |
| Context / Role / Field | partially_observable | Context/field refs appear in candidate contracts; role lineage needs a joined trace. |
| Attention | partially_observable | Attention candidate/architecture assets exist; actual selection trace is incomplete. |
| Information Need | partially_observable | Observation demand and information-gap assets provide adjacent evidence. |
| Observation Demand / Request | currently_observable | `ObservationDemandCandidateV1` and `ObservationRequestCandidateV1`. |
| Capability Requirement | currently_observable | `CapabilityRequirementCandidateV1` and governed resolution refs. |
| Capability Resolution | partially_observable | Governance records exist; unified cognitive trace linkage is incomplete. |
| External Capability Invocation | partially_observable | RF-DETR real smoke exposes provider invocation evidence; not all providers. |
| Observation | partially_observable | Request/result/handoff boundary exists; complete lifecycle trace is not universal. |
| Evidence | currently_observable | Visual evidence and Gateway handoff candidates. |
| Evidence relevance/conflict/missing/uncertainty | partially_observable | Sufficiency and information-gap fields exist; responsibility attribution needs extension. |
| Current World Candidate | currently_observable | Existing candidate type and RF-DETR bridge output. |
| Hypothesis / Revision | currently_observable as candidate | `CognitiveHypothesisCandidateV1`; revision lineage must be joined across cycles. |
| Sufficiency | currently_observable as candidate | `EvidenceSufficiencyCandidateV1`. |
| Information Gap | currently_observable in controlled path | Existing information-gap detector. |
| Re-observation | partially_observable | Policy and NextCycle candidate exist; no autonomous provider retry. |
| Stop Reason | planned | Must be added to a cognitive profile, not inferred from missing fields. |
| Decision Governance Handoff | partially_observable | `next_target`/handoff refs; Decision remains external owner. |
| Result / Closure | partially_observable | Evaluation reports/TestBoard exist; field-goal closure needs explicit candidate semantics. |

## Required trace fields

`trace_id`, parent transition refs, node status, producer/consumer, authority
owner, responsibility owner, input/output refs, versions, evidence refs,
constraint refs, information-gap refs, failure refs, stop reason, next target,
provenance, and candidate/admission/execution flags.

Unavailable nodes must be marked unavailable with a reason; they must not be
filled with synthetic success.
