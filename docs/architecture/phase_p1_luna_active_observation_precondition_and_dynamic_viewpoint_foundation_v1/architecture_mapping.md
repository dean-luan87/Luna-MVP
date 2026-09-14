# Architecture mapping

| Concern | Existing canonical owner / asset | Phase use |
|---|---|---|
| Self state | `docs/architecture/cognitive_self_state_awareness_v1/` | Reused as candidate-only Self input; no new Self owner |
| Observation Demand / Request | Field Perception Orchestrator / Active Observation Control | Reused `ObservationDemandCandidateV1` and `ObservationRequestCandidateV1` |
| Capability Requirement | Field Perception Orchestrator integration contracts | Reused `CapabilityRequirementCandidateV1`; identity remains distinct from Observation Requirement |
| Observation regulation | Field Perception Orchestrator | New additive precondition candidates owned here |
| Cognitive Gap / Re-observation | Cognitive State Formation Governance + Field Perception Orchestrator | Not rewritten; this phase only adds an upstream eligibility gate |
| Provider execution | Provider Runtime | Not entered; `eligible_now` is not invocation |

Identity namespaces remain separate: observation requirement, capability
requirement, demand, request, Self state, relative state, window, eligibility,
and condition gap each have their own reference.

