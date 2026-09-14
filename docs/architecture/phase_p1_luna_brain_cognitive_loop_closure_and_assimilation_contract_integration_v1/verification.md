# Verification plan

The user owns execution.  Do not run these commands from the Agent.

Runner:

```bash
cd /Users/luanlei/Desktop/Luna-Core && \
python -m capabilities.midplatform.core.cognitive_flow.integration.brain_cognitive_loop_closure_assimilation_controlled.runner_v1
```

Verifier:

```bash
cd /Users/luanlei/Desktop/Luna-Core && \
python -m capabilities.midplatform.core.cognitive_flow.integration.brain_cognitive_loop_closure_assimilation_controlled.verifier_v1 \
_eval_out/brain_cognitive_loop_closure_assimilation_controlled_v1/runner_summary_v1.json
```

The Verifier must pass both cases only when canonical proof contains runtime
execution, canonical owners, the required Sufficiency/Stop chain, and the
Case-B causal links from Cycle 1 Gap/Re-observation/next-cycle ingress into
Cycle 2 revision.  It must also pass the negative closure probe.
