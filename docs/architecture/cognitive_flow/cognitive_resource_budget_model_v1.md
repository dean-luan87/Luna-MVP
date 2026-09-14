# Cognitive Resource Budget Model v1

## Resource classes

The Cognitive Resource Budget covers:

- compute;
- battery / energy;
- attention;
- memory / storage;
- network.

## Allocation chain

```text
Need
  ↓
Expected Value
  ↓
Resource Cost
  ↓
Allocation Candidate
  ↓
Governed Capability Support
```

Brain supplies long-horizon resource policy and value context. Neural proposes
dynamic regulation candidates. Middleware evaluates capability envelopes,
availability, and physical resource constraints. Final State changes require the
Reducer and an authorized adoption path.

## Boundary

Resource Management is not a Scheduler. It does not assign wall-clock execution,
open devices, invoke models, create Goals, or make Decisions. A denied or
degraded allocation becomes a constraint candidate and may be escalated.
