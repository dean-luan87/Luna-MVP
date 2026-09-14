# Observation Perception Routing Candidate — Controlled Implementation v1

Status: `WAITING_FOR_USER_TERMINAL_VERIFICATION`

This phase adds a candidate-only handoff after Capability Resolution:

`Observation Demand → Capability Resolution Candidate → Perception Routing Candidate`

It is not a second Observation Gateway or FPO. The new projection is placed in
the existing `core/observation_gateway` control namespace, before the Gateway's
runtime ingress boundary. It preserves the cognition and capability lineage
without submitting a request or selecting an implementation.

The phase stops at `PerceptionRoutingCandidateV1`. The follow-on
compatibility phase projects that candidate into the existing FPO boundary;
runtime admission, binding, and execution remain deferred.
