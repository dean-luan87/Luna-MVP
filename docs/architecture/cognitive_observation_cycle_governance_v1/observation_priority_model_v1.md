# Observation Priority Model v1

## Priority candidate

Observation Priority is a candidate allocation signal, not a Decision. It is
derived from:

- Survival Impact;
- Goal Alignment;
- Reality Uncertainty;
- Temporal Urgency;
- Information Value;
- Resource Cost;
- Confidence Requirement;
- current Field constraints.

High-priority candidates include life-safety information, task-critical
information, and rapidly changing or highly uncertain Reality. Low-priority
candidates include repetitive observations of a stable state.

## No importance shortcut

Importance does not mean the observation must execute immediately. The
governance layer compares Information Value with Resource Cost and returns an
Allocation Candidate. Brain retains Goal and Decision authority; Neural and
Middleware retain resource and capability governance.

## Resource outcomes

An observation can be allocated, deferred, compressed, backgrounded, or
suspended. A rejected request remains an Unknown or Missing Information
candidate; it is never silently converted into a Fact.

This model is not a Scheduler. It does not implement a Scheduler, time-based
execution, sensor control, automatic model calls, or Action.
