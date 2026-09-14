# Cognitive Field Activation Policy v1

## Activation sources and guards

| Source | Example | Required guard |
|---|---|---|
| Brain Intent | Airport Navigation Field | Intent reference and bounded scope |
| Neural Detection | Self Maintenance Field | evidence, anomaly, confidence, escalation path |
| External Event | Social Interaction Field | event provenance and validity |
| User | explicit request | request reference and authority check |

Activation produces a Field Candidate. The policy validates source, scope,
authority, resource candidate, validity, Unknown, and provenance. It does not
perform Decision, Prediction, Planning, Reasoning, or Action. It does not perform Decision.
It does not perform Prediction.

## Attention relation

Field activation does not equal Attention activation. Attention operates inside
an active field and requests information; Attention does not create a Field.
