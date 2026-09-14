# Decision Commitment Model Definition v1

## Candidate model

`CognitiveDecisionCommitmentCandidateV1` may retain:

| Field | Meaning |
| --- | --- |
| `decision_candidate_reference` / `choice_space_reference` | Current option-space lineage |
| `context_reference` / `goal_reference` | Current context and goal references |
| `survival_alignment_reference` / `mission_alignment_reference` | Highest-value constraint references |
| `value_evaluation_reference` / `constraint_reference` | Value and cognitive-constraint references |
| `evidence_sufficiency_candidate` | Whether current evidence may support future consideration |
| `uncertainty` / `conflict_reference` | Explicit unresolved basis |
| `stopping_condition_reference` | Why further reasoning may be bounded |
| `delay_condition_reference` / `reversal_condition_reference` | Candidate delay/reconsideration conditions |
| `escalation_reference` | Candidate information/assistance/alternative path |
| `provenance` / `trace_ref` | Source lineage and trace closure |

It remains `candidate_only=true`, `not_fact=true`, `not_state=true`, `not_decision=true`, `not_action=true`, `not_permission=true`, and `not_memory=true`.

## Interpretation

Commitment expresses that a future Decision stage may receive a bounded option basis. It never means an option was selected or that any later action is authorized.
