# User-terminal verification

The agent only performs static inspection and `git diff --check`; it does not
run Python or the evaluation. Run from the repository root:

```bash
python3 -m capabilities.evaluation.evidence_context_field_current_world_controlled.runner_v1
python3 -m capabilities.evaluation.evidence_context_field_current_world_controlled.verifier_v1
```

The runner writes:

`_eval_out/evidence_context_field_current_world_controlled_v1/runner_summary_v1.json`

The verifier must report the controlled case count, resolved governance set,
preflight/postflight status, independent Scenario 12 paths, and the unified
final decision. A user-terminal result is required before the phase can be
called verified.
