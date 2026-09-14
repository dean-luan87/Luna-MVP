# Decision Trace Validation Model v1

## Structured trace contract

```json
{
  "situation_reference": {},
  "self_context": {},
  "goal_context": {},
  "resource_context": {},
  "options": [],
  "evaluation": {
    "survival_impact": {},
    "goal_alignment": {},
    "capability_fit": {},
    "resource_cost": {},
    "risk": {},
    "uncertainty": {},
    "experience_reference": {},
    "confidence": {}
  },
  "decision_candidate": {},
  "confidence": {},
  "unknowns": []
}
```

The trace records structured decision basis only: references, constraints,
option differences, evaluation fields, and Unknown factors. It is not private
chain-of-thought, an Action plan, Outcome prediction, Runtime record, or State
mutation request.

This structured trace does not contain private chain-of-thought.

## Trace assertions

- The situation reference must be present before option generation.
- Self context, Goal, Resource, Risk, and Unknowns must remain visible in evaluation.
- The decision candidate names a candidate option and its support boundary; it does not execute.
- changed material Evidence creates a new trace reference rather than overwriting past context.
- Brain Evaluation is the final cognitive judgment boundary; trace production does not approve a decision.
