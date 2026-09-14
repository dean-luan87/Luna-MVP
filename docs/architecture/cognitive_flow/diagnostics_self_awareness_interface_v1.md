# Diagnostics–Self Awareness Interface v1

## Diagnostic output

Diagnostics reports a structured candidate:

```json
{
  "capability": "vision",
  "status": "degraded",
  "reason": "hardware_failure",
  "confidence": 0.9
}
```

Possible causes include hardware failure, model anomaly, low light, protocol
failure, resource shortage, and unknown. Diagnostics must preserve provenance,
timestamp, evidence references, and uncertainty.

## Feedback path

```text
Registry / Hardware / Model Observation
              ↓
          Diagnostics
              ↓
      Capability State Candidate
              ↓
      Self Capability Context Candidate
              ↓
      Neural Regulation / Brain Awareness
```

Diagnostics cannot decide "do not look", change a life goal, define personality,
or execute hardware control. Adoption or State mutation remains governed by
Validation → Adoption and the Reducer.
