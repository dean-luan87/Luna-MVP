# Verification

The synthetic Runner is:

`capabilities/evaluation/level1_cognitive_evaluation_run/runner_v1.py`

It creates one explicit synthetic registry entry/sample, composes one existing Level-1 case, attaches an existing White-box V1 trace/profile, assesses A-Route readiness, writes one immutable archive record, and emits a summary. It does not invoke Luna cognition or any external capability.

The Verifier is:

`capabilities/evaluation/level1_cognitive_evaluation_run/verifier_v1.py`

It reads the Runner summary and archive, checks linkage, archive location/immutability, V1 reuse, explicit unavailable metrics, synthetic non-cognition status, and all negative boundaries. It must not be interpreted as real cognitive evaluation.

User terminal commands, from the canonical root:

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 -m capabilities.evaluation.level1_cognitive_evaluation_run.runner_v1
python3 -m capabilities.evaluation.level1_cognitive_evaluation_run.verifier_v1 _eval_out/level1_cognitive_evaluation_run_boundary_v1/runner_summary_v1.json
```

These commands were not run by the agent.

