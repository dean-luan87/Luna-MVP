# Cognitive Outcome Model Definition v1

## Candidate model

`CognitiveOutcomeCandidateV1` may contain:

| Field | Meaning |
| --- | --- |
| `expected_outcome_reference` | Expected Outcome Candidate reference |
| `actual_outcome_candidate` | Candidate observation of what may have occurred |
| `difference_candidate` | Candidate difference between expected and observed outcomes |
| `success_failure_candidate` | Contextual candidate result; not truth or learning label |
| `unexpected_event_reference` | Candidate unexpected event reference |
| `decision_commitment_reference` / `context_reference` | Preceding decision-context lineage |
| `evidence_references` | Required observed/evaluated evidence |
| `provenance` / `trace_ref` | Source lineage and trace closure |

Outcome is `candidate_only`, non-Fact, non-State, non-Decision, non-Action, non-Permission, and non-Memory. “Actual” describes an observed candidate, not an asserted reality record.
