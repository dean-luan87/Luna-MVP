# Task / Capability Governance Boundary v1

Task may express a required functional outcome, capability requirement ref,
slot/dependency ref, and execution prerequisite. Capability Governance owns
Scope, Logical Capability Resolution, model/provider mapping and Runtime
Admission. Provider Governance owns Provider admission/invocation.

The current `build_capability_routes_v1()` reads capability requirements from
the registry, returns routing candidates, and marks unknown/deprecated or
blocked entries. It does not itself invoke a Provider, but its module API
selection and `execution_request_candidates` make the ownership boundary too
broad.

Disposition: **NARROW / COMPATIBILITY_ONLY during migration**. Retain
requirement-to-request candidate construction and dependency ordering; remove
any implication that Task resolves a logical capability, selects a model or
Provider, or performs Runtime Admission.
