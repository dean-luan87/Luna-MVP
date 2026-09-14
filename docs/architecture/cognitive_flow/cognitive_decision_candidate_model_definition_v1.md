# Decision Candidate Model Definition v1

## Candidate definition

A Decision Candidate is a possible selection option formed under current Context, Goal, Mission, Survival, Behavior Boundary, and Value Evaluation constraints. It does not indicate that Luna has decided.

`CognitiveDecisionCandidateV1` may contain:

| Field | Meaning |
| --- | --- |
| `candidate_option_reference` | Governed Behavior Candidate reference |
| `supporting_evidence_references` | Evidence lineage for option eligibility |
| `expected_outcome_candidate` | Possible, not guaranteed, outcome |
| `cost_reference` / `risk_reference` | Candidate cost and risk descriptions |
| `mission_alignment_reference` | Mission value input, subordinate to Survival |
| `survival_alignment_reference` | Survival constraint alignment |
| `reversibility_reference` | Candidate reversibility description |
| `uncertainty` | Explicit unknown information |
| `conflict_reference` | Trade-off/conflict candidate reference |
| `provenance` / `trace_ref` | Source lineage and trace closure |

No `selected`, `execute`, `command`, `permission`, State write target, Fact id, Decision id, or Memory target is permitted.
