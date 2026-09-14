# Verification

Run from the canonical repository root:

```sh
cd /Users/luanlei/Desktop/Luna-Core
python3 -m capabilities.evaluation.cognitive_requirement_alternative_satisfaction_basis.runner_v1
python3 -m capabilities.evaluation.cognitive_requirement_alternative_satisfaction_basis.verifier_v1
```

The Agent must not execute these commands. The verifier should cover:

- legacy exact coverage present/missing;
- alternative basis A, B, none, and multiple basis coverage;
- one semantic requirement rather than multiple source conditions;
- Sandbox Scenario 12 Round 0 unsatisfied and Round 1 satisfied by signage;
- Scenario 10 Need with zero strategies;
- Scenario 11 irrelevant-change stability;
- candidate-only/read-only/non-Truth and no downstream side effects;
- unchanged Information Need subtraction and absence of strategy,
  observation, capability, resource, decision, task or action execution.

Expected phase status before user execution:
`IMPLEMENTATION_READY_FOR_USER_EXECUTION`.
