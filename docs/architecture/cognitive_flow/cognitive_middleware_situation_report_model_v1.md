# Cognitive Middleware Situation Report Model v1

## Definition

A Middleware Situation Report describes the current **execution environment** relevant to a received CWO. It lets Neural Governance see what capability conditions, constraints, degradations, and alternatives exist before or during capability organization.

It is not a cognitive situation/world-understanding object and does not make a Decision.

```text
MiddlewareSituationReport {
  work_objective_ref,
  capability_availability,
  provider_status,
  resource_constraint,
  failure_candidate,
  degradation_candidate,
  alternative_capability_candidate,
  protocol_compatibility,
  trace
}
```

## Report dimensions

| Dimension | Example | Boundary |
|---|---|---|
| Capability availability | Vision available; spatial capability available. | Availability does not imply invocation. |
| Provider status | OCR degraded; a provider may be suspended. | Status does not evaluate evidence truth. |
| Resource constraint | Battery/latency/compute limit. | Constraint does not alter Goal or Attention. |
| Failure | Required contract unavailable. | Failure does not cancel the CWO. |
| Degradation | Lower-quality or partial coverage expected. | Degradation must remain visible. |
| Alternative capability | Candidate capability path under current conditions. | Alternative does not rewrite CWO purpose. |

## Example

```text
Vision: available
OCR: degraded
Spatial: available
Latency: high
Alternative: scene-understanding capability candidate may offer partial text/landmark coverage
```

The report is sent to Neural Governance as a condition candidate. Neural may supervise objective alignment; Brain decides whether this condition matters to its cognitive need.
