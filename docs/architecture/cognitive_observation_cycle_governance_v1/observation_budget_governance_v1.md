# Observation Budget Governance v1

## Budget dimensions

The budget evaluates camera/sensor time, microphone time, CPU/GPU compute,
battery/energy, network, memory, and attention. Each Observation Requirement
provides an estimated Resource Cost and expected Information Value candidate.

```text
Observation Need
      ↓
Information Value
      ↓
Resource Cost
      ↓
Budget Evaluation
      ↓
Allocation Candidate
```

## Boundary

Budget Governance may qualify, defer, compress, background, or suspend an
observation candidate. It does not perform Action, open a Camera, call OCR,
call SLAM, set hardware frequency, or bypass Capability Governance. It is not
a Scheduler and does not implement a Scheduler. It is not a Scheduler.

When budget is insufficient, the result is a Resource Constraint Candidate,
not a fabricated Evidence result. The Unknown requirement remains visible to
the Field and A Route.

## Safety priority

Survival Impact, Goal Alignment, Reality Uncertainty, and Temporal Urgency are
considered together. No single local metric may replace Brain Intent or the
Reality/Field boundary.
