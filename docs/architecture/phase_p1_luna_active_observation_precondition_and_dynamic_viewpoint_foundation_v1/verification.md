# Verification

The user-terminal commands are:

```text
python3 -m capabilities.evaluation.active_observation_precondition_dynamic_viewpoint_foundation.active_observation_precondition_runner_v1
python3 -m capabilities.evaluation.active_observation_precondition_dynamic_viewpoint_foundation.active_observation_precondition_verifier_v1
```

The verifier is intended to check unknown-not-necessary, demand-not-invocation,
condition-gated windows and eligibility, condition gaps and adjustment needs,
dynamic open/close transitions, Self decision ownership, candidate-only and
no-mutation boundaries, identity/trace completeness, and empty validation
errors.

This is controlled dynamic-state verification. Until the user runs the
commands, the phase remains `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
It must not be reported as real dynamic viewpoint verification.

