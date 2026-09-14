# Reality Experience Interface Readiness Model v1

## Purpose

The A-to-B Experience interface is not expanded in this phase. This review
checks that its future output is sufficient for governed reflection without
exposing A internals or granting B current control.

## Minimum Experience Candidate coverage

| Field | Meaning |
|---|---|
| `context_ref` | represented situation and relevant goal/resource frame |
| `decision_trace_ref` | options, factors, confidence, expectation reference |
| `outcome_ref` | outcome trace with uncertainty and temporal scope |
| `difference_ref` | prediction/outcome deviation candidate where applicable |
| `failure_type_candidates` | localizable candidate classes, including Unknown Cause |
| `value_impact_ref` | survival value feedback candidate, not Reward |
| `confidence_and_unknowns` | support limits retained for later reflection |

The interface exports only governed candidates. Experience Candidate cannot
directly update Self, Strategy, Attention, Provider selection, or current A
decision; B returns only through Validation, Reality Feasibility, and Adoption
Candidate boundaries.
