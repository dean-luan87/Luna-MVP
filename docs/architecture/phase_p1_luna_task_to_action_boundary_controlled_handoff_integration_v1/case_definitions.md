# Case Definitions

## Case A

The existing sufficient first-cycle case reaches one admitted planned Task.
That Task produces one Task-to-Action handoff and one Action Candidate.

## Case B

The existing two-cycle case has no Decision, Task, or Action handoff in cycle
1. After final Sufficiency and Stop, its admitted planned Task produces one
Task-to-Action handoff and one Action Candidate.

## Negative case

`action_handoff_without_valid_task` supplies no valid admitted Task. The
adapter rejects it and does not invoke Action Governance.
