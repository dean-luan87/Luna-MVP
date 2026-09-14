# Ownership and boundaries

The existing owners remain unchanged:

- Cognitive Flow owns Observation Demand formation.
- Capability Registry / Capability Governance owns capability inventory and
  resolution.
- This phase owns only the candidate-only perception routing projection.
- Observation Gateway owns later ingress/admission and runtime observation
  handling.
- FPO owns its existing active-observation/provider-facing controls.
- Provider/Model Governance owns later concrete binding.

`ObservationRequestCandidateV1` is a historical FPO/task-driven request
candidate with task, model-requirement, budget, and provider-facing fields. It
is not the cognitive Perception Routing Candidate. `ObservationGateway` accepts
runtime ingress contracts such as `ObservationIngressRequestV1`; this phase
does not call it. FPO active observation control is likewise not invoked.

The phase creates no routing admission, route ranking, route winner, slot
reservation, provider/model binding, FPO request, Gateway submission, or
observation execution.
