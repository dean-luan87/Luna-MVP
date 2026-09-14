# Regression execution order

Synthetic:

```text
python3 capabilities/midplatform/core/cognitive_flow/integration/cognitive_mainline_consolidated_regression_checkpoint_controlled/run_cognitive_mainline_consolidated_regression_checkpoint_v1.py --group synthetic
python3 capabilities/midplatform/core/cognitive_flow/integration/cognitive_mainline_consolidated_regression_checkpoint_controlled/verify_cognitive_mainline_consolidated_regression_checkpoint_v1.py
```

Real-approved, only when explicitly authorized:

```text
python3 capabilities/midplatform/core/cognitive_flow/integration/cognitive_mainline_consolidated_regression_checkpoint_controlled/run_cognitive_mainline_consolidated_regression_checkpoint_v1.py \
  --group real-approved \
  --real-capability-source <approved-input-path> \
  --real-capability-model-path <approved-model-path> \
  --real-capability-dependency-status <terminal-verified-dependency-status> \
  --real-capability-declared-checksum <terminal-declared-checksum> \
  --real-capability-observed-checksum <terminal-observed-checksum>
python3 capabilities/midplatform/core/cognitive_flow/integration/cognitive_mainline_consolidated_regression_checkpoint_controlled/verify_cognitive_mainline_consolidated_regression_checkpoint_v1.py
```

The five `--real-capability-*` values are required for `REAL-CAPABILITY` and
are forwarded unchanged as the child Runner's `--source`, `--model-path`,
`--dependency-status`, `--declared-checksum`, and `--observed-checksum`.
The checkpoint does not approve, calculate, or substitute any of them.

If any value is absent, the checkpoint records
`READINESS_ARGUMENTS_REQUIRED`, does not launch the child, and records
`provider_invocation_attempted=false`.

`--group all` has the same requirement when it reaches the real capability
entry. Synthetic-only execution does not require these arguments.
