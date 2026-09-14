# Capability Resolution and Invocation Boundary

Resolution accepts a structured `CapabilityRequirementV1`, consults registered
Module definitions and projected Slot bindings, and returns:

- `READY_CANDIDATE`
- `UNAVAILABLE_CANDIDATE`
- `DEGRADED_CANDIDATE`

The result preserves Module, Slot, Implementation, Model, Provider, reason,
and recovery references.

`CapabilityInvocationCandidateV1` is a handoff candidate only. It does not
invoke a provider, execute a model, activate a camera, execute Runtime, or
bypass Observation Gateway/FPO for visual capabilities.
