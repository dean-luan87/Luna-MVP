# Luna Capability Runtime Integration Architecture v1

## Position

Capability Runtime is the L4 operating framework for admitted capability
execution. It receives a Capability Request that has passed the Execution
Boundary, creates a bounded execution context, and returns a result through the
Evidence Gateway. This phase defines the framework contracts only.

```text
L2 Capability Request
        ↓
L1 Admission / Lifecycle / Resource Governance
        ↓
Capability Runtime
  Executor → Context → Adapter Boundary → Result Collector
        ↓                         ↓
  Health / Failure / Trace    Evidence Gateway
        ↓                         ↓
  Capability Profile       L2 Cognitive Update
```

## Runtime subsystems

Capability Executor, Execution Context Manager, Provider Adapter Layer,
Capability Lifecycle, Resource Governance, Scheduler Boundary, Result
Collector, Health Manager, Cache Boundary, Trace Integration, and Failure
Handler.

## Boundary principles

- Capability Runtime runs only admitted Capability Requests; it does not create
  Intent, Goal, Decision, or Action.
- Provider Adapter isolates provider identity and implementation details.
- Results are raw results until Result Collector and Evidence Gateway validate
  them; they do not become Reality or Memory directly.
- Resource Governance constrains usage; it does not grant capability authority.
- Health and feedback produce profile/calibration candidates, never automatic
  model parameter changes or uncontrolled provider switching.
- This phase has no Provider instance, model call, hardware driver, scheduler,
  or runtime execution.

