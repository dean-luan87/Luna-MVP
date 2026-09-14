# External Capability Fitness Plan

## Profile

Use `ExternalCapabilityFitnessProfileV1`, not a primary Model Fit Profile.
It is scoped to:

`Task + Observation Requirement + Environment Condition + Resource Constraint`.

## Measures

- evidence usefulness and stability;
- latency and resource cost;
- uncertainty and conflict generated;
- additional observation burden;
- effect on hypothesis revision and task completion;
- normalization/provider failure rate;
- stale-result exposure.

## Interpretation

The profile answers which external implementation better supports Luna's
cognitive goal under stated conditions. It does not optimize the model, rank
models globally, change bindings, select a provider at runtime, or turn Model
PASS into Luna PASS.
