# Cognitive Field Resource Governance Model v1

## Resource classes

Field Resource Governance evaluates:

- Attention;
- Memory;
- Compute;
- Sensor;
- Energy.

## Allocation path

```text
Field Resource Request
      ↓
Resource Evaluation
      ↓
Allocation Candidate
      ↓
Monitoring
```

Low battery may produce a reduced observation or frequency candidate, but a Field
does not decide it. Neural and Middleware evaluate resource envelopes; Brain may
review important conflicts. Resource Governance is not a Scheduler and does not
execute Action or directly mutate State. Resource Governance does not execute Action.

## Required trace

Every request preserves field reference, process reference, resource type, cost,
expected value, constraint, allocation status, confidence, and escalation path.
