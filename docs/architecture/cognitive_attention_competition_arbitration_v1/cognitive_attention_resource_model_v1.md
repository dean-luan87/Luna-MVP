# Cognitive Attention Resource Model v1

## Resource state

```text
Attention Resource
├── Available Capacity
├── Current Allocation
├── Reserved Capacity
└── Recovery Capacity
```

Available Capacity is the uncommitted attention budget. Current Allocation is
the active candidate distribution. Reserved Capacity protects Mandatory
Attention. Recovery Capacity prevents continuous demand from exhausting the
subject.

## Allocation boundary

An Attention Allocation Candidate must include demand, expected Information
Value, Resource Cost, source, class, duration/persistence, and uncertainty. A
budget shortage may defer, compress, background, or suspend attention. It does
not fabricate information and does not grant an Observation or Action.

Neural Regulation may provide resource constraints. Brain retains final
evaluation. Attention does not implement a Scheduler, automatic frequency
adjustment, hardware control, or Runtime. Information Value and Mandatory
Attention are explicit resource terms. Attention does not implement a Scheduler
and does not perform automatic frequency adjustment.

Mandatory Attention remains reserved capacity.
