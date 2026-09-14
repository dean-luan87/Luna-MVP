# Module Boundary Update

## Purpose

This update records target positioning. It does not edit the passed source-phase
documents or change their active owners.

## Existing modules

### Field State Reducer

Keep the existing formal mainline at
`capabilities/midplatform/core/field_state_reducer/module/`. It continues to reduce
admitted field events into candidate field state with trace and replay. The v2
position is **Field Context Management input**, implemented later through an
adapter. It gains no Memory, Intent, Causality, or Action authority.

### Observation Manager and Attention

The Observation Manager remains the Evidence/Environment Understanding owner for
observation request coordination and evidence candidates. Its attention
coordinator is perceptual coordination, not the owner of cognitive intent or
causality. Cognitive Attention remains the governed allocation layer and may later
consume Intent and Causal Projection candidates.

### Task Manager

The Task Manager remains the task lifecycle, dependency, routing, interruption,
and aggregation owner. It is downstream from approved intent/decision candidates.
It is not the Action Execution Layer and retains no real action, runtime dispatch,
or goal-creation authority.

### Model Manager

The Model Manager remains inside Capability Governance. It manages model identity,
admission, matching, resource evaluation, routing candidates, lifecycle candidates,
fallback, diagnostics, and trace/replay. It supplies cognitive organs through
governed capabilities but cannot become Brain, Intent, Causal, or Decision owner.

### Memory System

Memory remains the owner of historical storage, consolidation, activation,
retention, and retrieval. The v2 evolution path is:

```text
Outcome / Feedback → Experience Candidate → Experience Compression Candidate
→ Memory Candidate / Network Evolution Candidate → governed admission
```

Memory is no longer described as a passive warehouse, but it is not absorbed by
the Personal Cognitive Network.

### Emotion context

Emotion stays under Cognitive Integration and may contribute attachment or
adaptive-signal candidates to the network. It does not own Value Evaluation,
Intent, Decision, identity, or network mutation. Value Utility remains the owner
of value and cost/risk evaluation.

### Decision and Action

Causal reasoning and Intent Processing enrich candidate context. Decision
Arbitration retains selection authority; Action Boundary/Runtime retain execution
authority. No upstream network or gate can issue an action command.

## Previously described as new

- **Intent Engine:** existing Cognitive Intent Architecture v1 is reusable; a
  future engine would implement that contract rather than create a parallel owner.
- **Causal Reasoning Layer:** existing causality plans and v2 subjective-causality
  object schemas are reusable; engineering implementation remains absent.
- **Personal Cognitive Network:** this is the genuinely new integration
  responsibility, but it must be a typed projection/network over canonical source
  objects, not a replacement store for them.

