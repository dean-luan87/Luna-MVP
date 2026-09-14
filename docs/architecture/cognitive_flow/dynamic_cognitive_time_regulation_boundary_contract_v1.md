# Dynamic Cognitive Time Regulation Boundary Contract v1

## Input boundary

Allowed inputs are governed references to Field/View, Field Event/Dynamics candidates, Context, Attention, Survival, risk, Information Value, Cognitive Constraint, Cognitive Depth, Reasoning Lifecycle/Interrupt, Decision Candidate/Commitment, resource constraints, provenance, and trace.

Raw model output, provider payload, Fact Store, State handle, Reducer command, Decision result, Action command, permission grant, real-time clock control, scheduler command, Memory, Learning output, or Hive output asserted as authority are forbidden.

## Output boundary

Field Dynamics, Time Budget, Urgency, Preemption, Mode Switching, and Decision Window outputs are candidate-only: `not_fact`, `not_state`, `not_decision`, `not_action`, `not_permission`, and `not_memory`.

## Negative guards

- Field Change Rate != Event Fact.
- Field Dynamics != State Mutation.
- Cognitive Time Budget != Runtime Scheduler.
- Urgency != Action Trigger.
- Preemption != Runtime Control.
- Mode Switching != Decision or Permission.
- Decision Window != Forced Decision.
- Time Pressure != Survival Override.
- Confidence != Authority.
- Reducer remains the only State Mutation Authority.
