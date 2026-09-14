# User-terminal verification

Run from the repository root:

```bash
python3 -m capabilities.evaluation.provider_session_controlled_invocation_multiscenario_sandbox.runner_v1
python3 -m capabilities.evaluation.provider_session_controlled_invocation_multiscenario_sandbox.verifier_v1
```

The runner writes:

`_eval_out/provider_session_controlled_invocation_multiscenario_sandbox_v1/runner_summary_v1.json`

The verifier owns the final decision. Runner status and verifier
`final_decision` are separate contracts.
