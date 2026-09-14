# Cognitive Behavior Boundary Model Definition v1

## Candidate model

`BehaviorBoundaryCandidateV1` is a future traceable candidate with the following reference-oriented fields:

| Field | Meaning |
| --- | --- |
| `context_reference` | Current Cognitive Context reference |
| `field_reference` | Relevant Field reference |
| `field_identity_affordance_reference` | Stable Field constraint and affordance reference |
| `survival_constraint_reference` | Survival-first constraint reference |
| `goal_reference` | Current task/goal reference |
| `belief_reference` | Belief State reference; never an action source |
| `allowed_behavior_candidates` | Behaviors that may be considered under current evidence |
| `restricted_behavior_candidates` | Behaviors whose current constraints are explicit |
| `unknown_behavior_candidates` | Behaviors whose safety or availability remains unresolved |
| `risk_reference` | Candidate risk reference; not a Fact |
| `required_evidence_references` | Evidence required before a future boundary can expand |
| `provenance` / `trace_ref` | Source lineage and trace closure |

The candidate must carry no action command, permission grant, Fact identifier, State-write target, Decision identifier, or Memory target.

## Relationship rule

`Field Identity -> Field Affordance -> Behavior Boundary -> Future Action Candidate` is a constraint path. Each arrow denotes candidate constraint inheritance, never execution authority.
