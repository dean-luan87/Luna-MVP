# Cognitive Observation Cycle Model v1

## Scope

This phase governs the loop from a Cognitive Field's observation need to
evidence feedback and Field reassessment. It is a governance contract, not an
observation runtime, scheduler, sensor driver, or model implementation.

```text
Cognitive Field
      ↓
Observation Requirement
      ↓
Observation Governance
      ↓
Capability Governance
      ↓
Evidence
      ↓
Reality Update Candidate
      ↓
Field Reassessment
```

`Observation Requirement ≠ Observation Execution`. A Field proposes what
information would improve situated understanding. Governance qualifies,
allocates, and monitors a candidate; Capability and Provider layers remain the
only possible evidence sources. No layer in this phase makes a Decision or
performs an Action.

## Observation lifecycle

The lifecycle is:

```text
Created
  ↓
Qualified
  ↓
Allocated
  ↓
Executing Candidate
  ↓
Evidence Received
  ↓
Evaluated
  ↓
Completed / Suspended
```

An observation may be Transient Observation, Persistent Observation, or
Background Observation. Persistence is a governance candidate and must have a
release condition; it is not an unlimited stream.

Reducer remains the sole State mutation authority. This model enables no SLAM Runtime.

## Priority and budget

Observation Priority is a candidate based on Survival Impact, Goal Alignment,
Reality Uncertainty, Temporal Urgency, Information Value, and Resource Cost.
High priority may include life safety, task-critical information, or high
uncertainty. Repetitive stable information is normally lower priority.

The Observation Budget accounts for camera/sensor time, microphone time, GPU or
CPU, battery/energy, network, memory, and attention. Budget governance may
return an Allocation Candidate, defer, compress, or suspend a request. It does
not act as a Scheduler and does not control hardware.

## Evidence feedback

```text
Observation
      ↓
Evidence
      ↓
Reality Update Candidate
      ↓
Field Reassessment
```

Observation does not directly change the Field. The existing Evidence Gateway,
Reality Workspace, and Reducer remain authoritative; `Reducer remains the sole
State mutation authority`. Evidence failure is feedback, not a fabricated
absence of reality.

## Current boundary

This phase has no real model call, no Camera Runtime, no OCR Runtime, no SLAM
Runtime, no Hardware Runtime, no Action Runtime, no Emotion Engine, no Role
System, and no B Route. It defines no automatic retry, automatic model switch,
automatic scheduling, or online learning.
