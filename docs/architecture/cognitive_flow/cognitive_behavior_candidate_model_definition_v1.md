# Cognitive Behavior Candidate Model Definition v1

## Candidate schema

`CognitiveBehaviorCandidateV1` is a future traceable, non-authoritative candidate. It contains:

| Field | Meaning |
| --- | --- |
| `context_reference` | Current Cognitive Context reference |
| `field_reference` | Field or Field View reference |
| `goal_reference` | Current task/goal reference |
| `survival_constraint_reference` | Survival constraint reference |
| `behavior_boundary_reference` | Governing Behavior Boundary reference |
| `belief_reference` / `hypothesis_reference` | Uncertain explanatory references |
| `candidate_behavior` | A possible behavior description, not a command |
| `expected_outcome_candidate` | Possible outcome, not a guarantee |
| `risk_candidate_reference` | Candidate risk reference, not a Fact |
| `reversibility` | Whether a future behavior is expected to be reversible |
| `cost_estimate` | Candidate cost estimate |
| `information_gain_potential` | Possible information benefit |
| `provenance` / `trace_ref` | Source lineage and trace closure |

It must be candidate-only, non-Fact, non-State, non-Decision, non-Action, non-Permission, and non-Memory. It contains no Action command, permission grant, state-write target, Fact id, Decision id, or Memory target.

## Planned candidate taxonomy

- **Information Seeking Behavior**: approach for observation, change viewpoint, or request help.
- **Safe Exploration Behavior**: move slowly or preserve distance.
- **Task Progress Behavior**: continue navigation or seek a task-relevant location.
- **Avoidance Behavior**: retreat, bypass, or preserve separation.
- **Wait / Defer Behavior**: pause pending evidence or changed context.

These are labels for behavior possibilities, never executable instructions.
