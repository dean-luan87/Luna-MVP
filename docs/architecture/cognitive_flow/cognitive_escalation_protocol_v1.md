# Cognitive Escalation Protocol v1

## Escalation candidate

Neural emits an `Escalation Candidate` when a governed signal exceeds a review
boundary. Required fields are `escalation_id`, `source`, `trigger_type`,
`evidence_reference`, `affected_scope`, `urgency_candidate`,
`confidence_candidate`, `unknowns`, `resource_context`, and `requested_review`.

## Trigger classes

- `unknown_growth`: material information is missing or becoming less reliable;
- `risk_increase`: a potential safety or survival impact rises;
- `conflict_detected`: current evidence or state projections disagree;
- `capability_shortfall`: available capability cannot satisfy a requirement;
- `resource_stress`: power, thermal, compute, or attention envelope is constrained;
- `temporal_change`: a relevant state transition requires reassessment.

## Review path

```text
Neural Signal
  ↓
Escalation Candidate
  ↓
Attention / Situation Candidate
  ↓
Brain Evaluation
  ↓
Decision Candidate (if authorized)
```

Escalation does not directly change Goal, Intent, World State, Self, Attention,
Decision, or Action. A local monitoring response may be recorded only through the
Reducer contract. Priority is a candidate; Brain retains final judgment.
