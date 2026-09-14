# Verification

The user-terminal controlled evaluation writes:

`_eval_out/perception_routing_admission_compatibility_v1/runner_summary_v1.json`

and the verifier writes:

`_eval_out/perception_routing_admission_compatibility_v1/verifier_report_v1.json`

From the canonical root, run:

```bash
python3 -m capabilities.evaluation.perception_routing_admission_compatibility_controlled.runner_v1
python3 -m capabilities.evaluation.perception_routing_admission_compatibility_controlled.verifier_v1
```

The verifier checks required cases, status/count semantics, multiple-route
preservation, same-class and same-capability lineage, zero and fail-closed
behavior, provider/model non-fabrication, Scenario 12 separation,
candidate/read-only/non-Truth flags, immutable upstream snapshots, deterministic
replay, and all no-runtime guards.

This phase remains `WAITING_FOR_USER_TERMINAL_VERIFICATION` until real terminal
output is supplied.
