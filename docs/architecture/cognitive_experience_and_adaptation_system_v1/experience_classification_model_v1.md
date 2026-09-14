# Experience Classification Model v1

## Classes

| Class | Input | Future reference | Boundary |
|---|---|---|---|
| Episodic Experience | bounded event and Outcome | event similarity candidate | not Reality replay |
| Field Experience | Field context and repeated pattern | Field Pattern Candidate | not a Rule |
| Behavioral Experience | Behavior Candidate and Outcome | Behavior Pattern Candidate | not Action control |
| Self Experience | Capability/State evidence | Self Capability Adjustment Candidate | not Identity mutation |
| Interaction Experience | interaction outcome and provenance | Interaction Pattern Candidate | not Social Relationship |

Classification preserves `experience_id`, `field_reference`, `self_reference`,
`outcome_reference`, `evidence_reference`, `timestamp`, `confidence`,
`unknowns`, and `provenance`. A class label never upgrades a candidate into
Reality, Knowledge, Rule, or Decision.

## Promotion boundary

Classification → Evaluation → Retention Candidate is mandatory. An unconfirmed
Model guess, one-off noise, or unresolved Unknown remains a bounded candidate.

An unconfirmed Model guess is not promoted.
