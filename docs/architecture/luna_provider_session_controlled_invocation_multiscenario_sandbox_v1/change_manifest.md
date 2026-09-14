# Change manifest

## Added

- Provider Runtime Governance session/invocation typed contracts;
- controlled multi-scenario evaluation package;
- synthetic sandbox architecture documentation.

## Reused

- Provider Binding, Runtime Grant, Runtime Allocation, and Execution Instance
  canonical contracts;
- Protocol Manager Governance Backbone;
- FPO `BoundedProviderSessionCandidateV1` only as a documented semantic
  distinction;
- existing Gateway and `ProviderRuntimeRequestV1` contracts as downstream
  compatibility references.

## Not modified

Cognition, Demand, Capability, Routing, FPO semantic control, Provider Binding,
Runtime Grant, Runtime Allocation, Execution Instance, Observation Gateway,
Provider/Model managers, and existing real execution adapters.

## Deferred

Real session start, Provider/Model invocation, retry/fallback, resource
scheduling, RuntimeObservation, Gateway ingress, Evidence, Truth, and World
integration.
