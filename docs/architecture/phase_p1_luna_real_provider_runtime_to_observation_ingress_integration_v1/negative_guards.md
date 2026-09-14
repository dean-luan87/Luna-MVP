# Negative Guards

The Runner covers three fail-closed cases:

- unavailable provider result: no runtime observation or fake Evidence;
- malformed provider result: adapter rejection before Gateway admission;
- unresolved capability: no provider request and no provider call.

Recorded fixtures keep `provider_invocation=false` and `model_invocation=false`.
The bridge also preserves candidate-only, no-Truth, no-Field-mutation, and no
downstream Decision/Task/Action/Runtime Executor boundaries.

The re-observation case is request-candidate coverage only. It verifies that
Field Perception Orchestrator next-cycle ingress is carried into a provider
request without producing a provider result or triggering a provider call.

Provider success with an empty result is contractually distinct from provider
failure. The result type can represent `empty_result=true`; no additional
absence semantics are promoted in this phase.
