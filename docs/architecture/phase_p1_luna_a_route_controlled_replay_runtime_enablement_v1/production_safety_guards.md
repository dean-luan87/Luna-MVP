# Production Safety Guards

Controlled replay explicitly requires `non_live=true` and rejects `LIVE_RUNTIME`. The runner and canonical proof require:

`model_invocation=false`, `provider_invocation=false`, `live_observation_execution=false`, `action_execution=false`, `field_mutation=false`, and `world_truth_declared=false`.

