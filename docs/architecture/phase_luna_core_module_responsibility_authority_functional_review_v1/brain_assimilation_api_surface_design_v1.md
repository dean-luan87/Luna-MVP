# Brain Assimilation Conceptual API Surface v1

Documentation-only groups:

- `adjudicate_outcome_candidate`: input Outcome Candidate and governance refs; output final adjudication candidate.
- `apply_concern_consequence`: input accepted outcome and Concern refs; output closure/continuation candidate.
- `apply_goal_consequence`: input Goal-impact candidate; output Brain-owned Goal governance candidate.
- `generate_followup_concern_candidate`: input unresolved consequence; output NewConcernCandidate.
- `generate_intent_impact_candidate`: input Intent impact; output Intent Governance handoff.
- `generate_experience_candidate_handoff`: input accepted lineage; output candidate-only handoff.
- `generate_memory_candidate_handoff`: input retained event refs; output candidate-only handoff.
- `record_assimilation`: input authorized decision and refs; output Brain governance trace for Loop.

None directly mutates Memory, Intent, Field, Task, Loop or executes Action.
