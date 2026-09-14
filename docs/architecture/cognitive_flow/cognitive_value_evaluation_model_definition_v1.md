# Cognitive Value Evaluation Model Definition v1

## Candidate schema

`CognitiveValueEvaluationCandidateV1` is a traceable evaluation candidate for a governed Behavior Candidate. It may retain:

| Dimension | Candidate meaning |
| --- | --- |
| Mission Alignment | Relation to a Mission Constraint candidate |
| Survival Impact | Possible safety/support impact under current constraints |
| Goal Contribution | Possible contribution to the current goal |
| Information Gain | Potential reduction of a relevant unknown |
| Resource Cost | Time, compute, attention, energy, movement, and opportunity cost |
| Risk Exposure | Candidate exposure to uncertain downside |
| Reversibility | Potential to undo, exit, or limit a future behavior |
| Experience Reference | Historical pattern relevance; never authority |

Required references are Behavior Candidate, Behavior Boundary, Cognitive Constraint, Context, Field/View, Goal, Survival, Mission, Belief/Hypothesis, Information Value, provenance, and trace. Output remains `candidate_only`, `not_fact`, `not_state`, `not_decision`, `not_action`, `not_permission`, and `not_memory`.

No scalar reward, aggregate rank, or confidence is authoritative. The model describes competing dimensions; future Decision governance would separately interpret approved candidates.
