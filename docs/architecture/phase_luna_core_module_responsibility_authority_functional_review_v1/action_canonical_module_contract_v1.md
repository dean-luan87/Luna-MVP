# Action Governance — Canonical Module Contract v1

## Canonical purpose

Action Governance validates and admits a concrete operation that may change
external or system state or produce an externally observable effect, binds it
to Decision/Task, capability/runtime and Brain constraints, and returns an
auditable execution handoff/result boundary without owning the underlying
purpose, capability taxonomy or Provider runtime.

## Why it exists

Removing this boundary would force Task, Decision or Provider to own side
effect admission, permission/safety checks, target freshness, idempotency,
reversibility, execution trace and result uncertainty. Those responsibilities
are distinct from organizing work or implementing a capability.

## Authority and responsibility

Action Governance authoritatively admits, rejects, suspends or cancels a
concrete Action candidate under supplied constraints and mechanically rejects
stale, duplicate, invalid or unauthorized execution. Runtime Executor/Provider
owns execution. Action Governance does not select the Goal, resolve Need,
decide Task completion, declare World Truth or perform the side effect itself.

The repository Action contract is explicitly candidate-only: controlled output
records `runtime_executed=False`, `action_executed=False`,
`scheduler_executed=False`, `device_control_executed=False` and a candidate
runtime handoff. This is a controlled seam, not a runtime GO declaration.

## Disposition

**NARROW** as an independent side-effect admission/result boundary. Keep
concrete operation, permission/safety/resource/precondition/idempotency and
trace responsibilities; leave execution to Runtime Executor/Provider and
organization to Task. Timing: `CONTRACT_ONLY /
RUNTIME_CONSOLIDATION_LATER`.
