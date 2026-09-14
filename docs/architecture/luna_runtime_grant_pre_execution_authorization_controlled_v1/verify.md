# User-terminal verification

Run from the repository root using module execution so package-relative
imports resolve:

```sh
python3 -m capabilities.evaluation.runtime_grant_pre_execution_authorization_controlled.runner_v1
python3 -m capabilities.evaluation.runtime_grant_pre_execution_authorization_controlled.verifier_v1
```

The runner writes:

`_eval_out/runtime_grant_pre_execution_authorization_v1/runner_summary_v1.json`

The runner status indicates artifact generation readiness. The verifier owns
the final decision and emits `GO` only when functional, contract, governance
preflight, governance postflight, cognitive, and operational checks all pass;
otherwise it emits `NO_GO`.
