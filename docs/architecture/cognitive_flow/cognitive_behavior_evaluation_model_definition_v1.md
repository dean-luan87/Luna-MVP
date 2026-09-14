# Cognitive Behavior Evaluation Model Definition v1

## Candidate schema

`CognitiveBehaviorEvaluationCandidateV1` is a future, non-authoritative evaluation of one Behavior Candidate. It may contain:

| Field | Meaning |
| --- | --- |
| `behavior_candidate_reference` | The evaluated behavior candidate |
| `context_reference` / `field_reference` / `goal_reference` | Current cognitive situation references |
| `survival_constraint_reference` | Survival constraint reference |
| `behavior_boundary_reference` / `constraint_reference` | Governing behavior-space constraints |
| `belief_reference` / `hypothesis_reference` | Uncertain interpretive references |
| `survival_value_candidate` | Possible contribution to survival safety |
| `goal_value_candidate` | Possible task relevance/value |
| `information_value_candidate` | Possible uncertainty-reduction benefit |
| `relationship_value_candidate` | Future social/relationship relevance, where applicable |
| `experience_value_candidate` | Historical-pattern relevance, not authority |
| `physical_cost_candidate` / `cognitive_cost_candidate` / `time_cost_candidate` | Candidate resource costs |
| `risk_exposure_candidate` / `opportunity_cost_candidate` | Candidate downside dimensions |
| `uncertainty` / `reversibility_candidate` | Unknown conditions and potential ability to reverse |
| `provenance` / `trace_ref` | Source lineage and trace closure |

No single numeric score is required or authoritative. The result must remain candidate-only, non-Fact, non-State, non-Decision, non-Action, non-Permission, and non-Memory.

## Reversibility

Reversibility describes whether a future behavior could plausibly be undone or exited under current uncertainty. It is not a command and does not make a behavior safe. A small, reversible exploration can remain distinct from an extended, difficult-to-reverse entry even where the possible value is similar.
