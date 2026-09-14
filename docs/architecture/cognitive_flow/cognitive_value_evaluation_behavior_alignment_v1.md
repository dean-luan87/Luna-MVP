# Cognitive Value Evaluation Behavior Alignment v1

## Candidate chain

`Behavior Boundary -> Behavior Candidate -> Cognitive Value Evaluation Candidate -> Future Decision Candidate` preserves the separation of space, possibility, evaluation, and selection.

Cognitive Value Evaluation can describe why a candidate might be useful, costly, risky, uncertain, or reversible. It cannot widen the Behavior Boundary, convert an unknown/restricted behavior to allowed, select a candidate, or emit an Action.

## Planning cases

| Case | Evaluation requirement | Frozen result |
| --- | --- | --- |
| Ordinary task | Low risk, ordinary value | Describe value/cost; no selection |
| Unknown environment | Risk and information gaps explicit | Preserve safe candidate alternatives |
| High-value goal | High benefit and high cost | Retain trade-off and reversibility |
| Mission conflict | High Mission Alignment, low ordinary return | Mission influences evaluation only |
| Survival conflict | High Mission Alignment, excessive survival risk | Survival limitation remains dominant |
