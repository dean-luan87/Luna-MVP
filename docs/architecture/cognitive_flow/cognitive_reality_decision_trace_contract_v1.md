# Reality Decision Trace Contract v1

## Trace purpose

A decision trace allows a future simulation to explain why a Decision
Candidate was formed and whether the later Outcome Reference matched its
assumptions. It is not a decision log that implies an Action occurred.

```text
Situation Candidate
        ↓
Available Option Candidates
        ↓
Evaluation Factors / Priority / Confidence
        ↓
Decision Candidate
        ↓
Expected Outcome Candidate
        ↓
Future Outcome Reference
```

## Minimum fields

| Field | Boundary |
|---|---|
| `situation_ref` | represented context, not truth |
| `available_options` | non-ranked candidates, not recommendations |
| `evaluation_factors` | survival/goal/capability/resource/risk/experience factors |
| `decision_candidate_ref` | Brain judgment input, not an Action |
| `expected_outcome_ref` | hypothesis/expectation, not future fact |
| `confidence_and_unknowns` | explicit support limits |
| `trace_ref` | provenance linkage across the loop |

The trace must not fabricate a selected action, hide rejected options, or
convert outcome difference into immediate strategy change.
