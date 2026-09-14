# Verification

The agent performs static inspection and `git diff --check` only. User-terminal execution is required.

Run the controlled Runner first:

```bash
python3 -m capabilities.evaluation.provider_invocation_result_runtime_observation_gateway_evidence_controlled.runner_v1
```

Then run the Verifier:

```bash
python3 -m capabilities.evaluation.provider_invocation_result_runtime_observation_gateway_evidence_controlled.verifier_v1
```

The Runner writes `_eval_out/provider_invocation_result_runtime_observation_gateway_evidence_controlled_v1/runner_summary_v1.json`. The Verifier computes the final decision from functional checks, contract failures, Governance Backbone preflight/postflight, cognitive result, and operational result. Runner readiness status and verifier final decision are separate.
