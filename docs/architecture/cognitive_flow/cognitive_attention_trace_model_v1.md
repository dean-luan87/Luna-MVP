# Attention Trace Model v1

## Trace chain

```text
Attention Intent
        ↓
Attention Requirement
        ↓
Capability Observation Candidate
        ↓
Evidence Candidate
        ↓
Attention Feedback
        ↓
Situation Impact Candidate
```

## Required trace fields

`intent_ref`, `requirement_ref`, `axis_ref`, `situation_ref`,
`observation_candidate_ref`, `capability_ref`, `evidence_ref`, `feedback_ref`,
`situation_impact_ref`, `priority_candidate`, `unknowns`, and `trace_ref`.

The trace must support “why did Luna look here?” and “why was another need not
selected?” without treating priority as fact, decision, action, or a hidden
model-call log.

