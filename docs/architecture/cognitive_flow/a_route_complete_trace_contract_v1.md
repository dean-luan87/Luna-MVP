# A-Route Complete Trace Contract v1

## Structured end-to-end trace

```json
{
  "survival_drive_reference": {},
  "brain_intent": {},
  "intent_preservation": {},
  "attention_requirement": {},
  "reality_evidence": {},
  "world_understanding": {},
  "self_understanding": {},
  "situation_candidate": {},
  "option_generation": {},
  "decision_evaluation": {},
  "decision_candidate": {},
  "execution_boundary": {},
  "outcome_evidence": {},
  "situated_outcome_evaluation": {},
  "cause_attribution": {},
  "adaptation_candidate": {},
  "experience_candidate": {}
}
```

This is a structured provenance contract, not private chain-of-thought, a
Runtime record, a real Action plan, an Outcome truth claim, or a State mutation
request.

## Trace validity

- every stage must reference its relevant upstream candidate;
- Reality Evidence must pass through World Understanding and Situation Candidate before Decision Candidate;
- the Decision Trace includes Situation, Self, Goal, Resource, options, evaluation, Unknowns, and confidence;
- the Outcome Trace includes expected/actual outcome, difference, cause, and adaptation candidate;
- Experience Candidate includes Situation, Decision, Outcome, Cause, Adaptation, Confidence, and Unknown factors;
- absent coverage is explicitly represented as Unknown rather than omitted;
- Experience Candidate is handoff-only and cannot initiate B control or write Memory.
