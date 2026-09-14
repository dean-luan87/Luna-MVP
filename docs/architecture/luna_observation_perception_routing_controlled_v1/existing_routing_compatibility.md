# Existing routing compatibility

Repository reconnaissance found:

1. `core/observation_gateway` contains the existing Gateway runtime ingress,
   normalization, admission, and evidence-routing contracts.
2. FPO integration contains `ObservationRequestCandidateV1` and visual
   handoff/request adapters. Those are task/provider-facing and are downstream
   of the cognitive handoff boundary.
3. Model Manager contains model/provider routing candidates, but those perform
   concrete selection/routing semantics and therefore are not reused here.
4. No independent candidate-only Perception Routing contract existed for the
   `Capability Resolution Candidate → Perception Routing Candidate` edge.

The chosen implementation is a small projection in
`capabilities/midplatform/core/observation_gateway/perception_routing_candidate_v1.py`.
It does not modify the existing Gateway or FPO contracts. A future adapter may
translate a routing candidate into a Gateway/FPO request after routing
admission, capability binding, and provider/model governance are explicitly
implemented.
