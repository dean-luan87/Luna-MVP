# A3 Cognitive Analysis Runtime Validation Contract v1

## Scope

Runtime Validation Closure consumes only serialized Runtime Skeleton DryRun output. It validates that output against the Runtime Boundary Contract; it does not authorize Runtime, call `execute()`, invoke an external capability, or modify State.

## Input Validation

The validation Runner accepts one Runtime Skeleton DryRun result file. It requires:

- the frozen DryRun phase/run/fixture identifiers;
- `runtime_authorization_status=NOT_AUTHORIZED`;
- a skeleton result with the controlled schema version;
- non-empty Context, Evidence, Hypothesis, and Analysis Question references in the evidence trace;
- canonical, parseable deterministic JSON.

Input validation does not resolve, fetch, mutate, or re-evaluate any reference.

## Output Validation

The accepted skeleton envelope must contain an Analysis Result Candidate, Evidence Trace, Uncertainty, Warning Codes, Runtime Flags, and validation issue codes. The candidate must remain `not_executed`; uncertainty must remain explicit rather than being treated as a conclusion.

## Boundary Validation

The following values are mandatory:

- `runtime_executed=false`
- `simulation_only=true`
- `model_invoked=false`
- `network_invoked=false`
- `database_invoked=false`
- `state_writeback=false`
- `decision_executed=false`

Both top-level DryRun flags and nested Runtime Flags must agree. Any contradictory value is a blocker.

## Permission Validation

The closure verifies that State writeback and Decision execution are both denied. No Context, Snapshot, Event, Evidence, Fact Store, Action, Admission, or Reducer operation is permitted or inferred from a passing validation result.

## Runtime Forbidden Capability Validation

The closure verifies declared absence of model, network, database, and external invocation. It does not itself introduce OCR, SLAM, camera, sensor, system time, randomness, automatic UUID generation, persistence, or external adapters.

## Authority

`runtime_authorized=false` remains true. A passing Validation Closure result is only evidence that a non-executing Skeleton DryRun output conforms to this contract.
