# Cognitive Field Health Monitoring Model v1

## Monitored conditions

Health Monitoring observes:

1. abnormal lifecycle, such as a Field Active for an unexpected duration;
2. information inflation, such as unreleased Transient Context;
3. Unknown accumulation;
4. Field State drift from Reality State;
5. resource exhaustion or boundary violations;
6. stale Provenance or missing lifecycle timestamps.

## Output

```text
Health Signal
      ↓
Diagnostic Candidate
      ↓
Neural / Middleware / Brain Review Path
```

Diagnostics does not repair, close, reprioritize, create a Goal, make a Decision,
or execute Action. It reports field_id, condition, evidence, confidence,
severity candidate, and suggested review path. Health Monitoring does not execute Action.
