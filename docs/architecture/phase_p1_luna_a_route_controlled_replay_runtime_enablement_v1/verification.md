# Verification

User terminal commands:

```text
python -m capabilities.midplatform.core.a_route_orchestration.run_a_route_controlled_replay_runtime_enablement_v1
python -m capabilities.midplatform.core.a_route_orchestration.verify_a_route_controlled_replay_runtime_enablement_v1 _eval_out/a_route_controlled_replay_runtime_enablement_v1/runner_summary_v1.json
```

The Verifier fails unless Gateway admission, A-Route execution, canonical Cognitive State Formation execution evidence, and at least one canonical transition are all present. It rejects a bare `runtime_executed=true` claim.

