# Intent Alignment Trace Model v1

## Trace chain

```text
Original Intent
        ↓
Intent Contract
        ↓
Interpretation Candidate
        ↓
Requirement Candidate
        ↓
Capability Observation Request Candidate
        ↓
Evidence Candidate
        ↓
Situation Impact Candidate
        ↓
Decision Support Candidate
        ↓
Alignment Score Candidate
```

## Required fields

`original_purpose_ref`, `non_negotiable_objective_ref`,
`allowed_interpretation_ref`, `requirement_ref`, `capability_request_ref`,
`evidence_ref`, `coverage_ref`, `missing_information_ref`, `situation_ref`,
`decision_support_ref`, `drift_candidates`, `alignment_score_candidate`, and
`trace_ref`.

The trace answers whether returned Evidence supports the Original Purpose, not
whether a model returned data or reached a local performance metric.

