# Cognitive Attention Competition and Arbitration Architecture v1

## Scope

Attention is an independent cognitive resource governance layer. It decides
which information is worth processing under finite capacity; it does not own
Goal, Decision, Value Judgment, or Action authority.

```text
Field State + Self State + Goal + Risk + Resource
                    ↓
         Attention Competition
                    ↓
          Attention Arbitration
                    ↓
          Attention Allocation
                    ↓
        Observation Requirement
                    ↓
          Capability Observation
```

## Sources and classes

Attention Source candidates are Survival Attention, Goal Attention, Field
Attention, Maintenance Attention, Exploration Attention, and External Demand
Attention. They compete for attention resource; they are not decisions.

Arbitration classes are Mandatory Attention, Competitive Attention, and
Opportunistic Attention. Mandatory Attention may request preemption when a
survival or system-risk candidate appears. The result is an Arbitration
Candidate, never an Action.

## Core boundaries

Attention Priority Candidate combines Survival Impact, Goal Relevance, Field
Relevance, Temporal Urgency, Information Value, Uncertainty Reduction, and
Resource Cost. It produces a candidate allocation, not a final choice.

New Evidence may produce an Attention Interrupt Request. Arbitration may
reallocate attention resources, but it does not execute a capability, modify
Reality, change Goal, make a Decision, or trigger Action.

Attention has a lifecycle of Created, Allocated, Maintained, Decayed,
Released, and Archived. Persistence may be Persistent, Temporary, or
Interruptive, each with release criteria.

## Current scope

Role and Emotion are interface placeholders only. There is no Emotion Runtime,
Role Runtime, Social Field, B Route, Prediction, Decision, Action, real model
call, or hardware control in this phase.

Attention Resource includes Available Capacity, Current Allocation, Reserved
Capacity, and Recovery Capacity. Field Attention and External Demand Attention
are registered sources. Attention Lifecycle is Created, Allocated, Maintained,
Decayed, Released, and Archived. No Emotion Runtime, No Role Runtime, No B Route,
No Decision, and No Action are enabled.
