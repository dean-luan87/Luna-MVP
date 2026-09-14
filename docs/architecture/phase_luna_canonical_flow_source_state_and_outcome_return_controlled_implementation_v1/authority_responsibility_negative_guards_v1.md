# Authority, Responsibility and Negative Guards v1

## Responsibility

- Provider/result adapter: Provider Result mapping only.
- Evidence adapter: Evidence correlation and mapping.
- Source-state handoff adapter: candidate target/version/provenance mapping.
- Field: future Field admission and mutation.
- Current World: candidate representation lifecycle.
- Outcome Evaluation: Outcome Candidate correctness.
- Outcome→Brain adapter: adjudication-input mapping.
- Brain: future final adjudication and Assimilation.

## Required false guards

`source_mutation_executed`, `world_truth_declared`, `field_reducer_executed`, `current_world_authoritative_write`, `brain_adjudication_executed`, `brain_state_mutation`, `intent_mutation`, `task_mutation`, `memory_mutation`, `experience_mutation`, `learning_execution`, `provider_invocation_executed`, `action_execution_executed`, and `runtime_execution` remain false.

