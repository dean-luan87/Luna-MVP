# Current World Representation Integration DryRun Implementation v1

## Scope

This is a fixture-only, deterministic integration DryRun. It reuses Field Structure, Field Kernel State/Snapshot, Temporal Evolution, Reducer Output types, Read Model result types, and Current Cognitive Context types as fixed in-memory objects.

## Actual asset mapping

| Required asset | Actual path | Mapping |
| --- | --- | --- |
| Field Identity / Unit / Relation / State / Snapshot | `capabilities/cognitive_flow/field_kernel/core/` | `exact_reuse` |
| Reducer adapter | `capabilities/cognitive_flow/field_kernel/reducer_adapter_v1.py` | `exact_reuse`; not invoked in this DryRun |
| Reducer output | `capabilities/midplatform/core/field_state_reducer/field_state_reducer_types_v1.py` | `fixture_only` fixed output; runtime not invoked |
| State Version / Transition / History / lifecycle validator | `capabilities/cognitive_flow/field_kernel/temporal_evolution/` | `exact_reuse` |
| Read Model result | `capabilities/midplatform/core/field_state_read_model/module/field_state_read_model_module_types_v1.py` | `fixture_only` fixed result; query runtime not invoked |
| Current Cognitive Context / Builder / Lifecycle Validator | `capabilities/cognitive_flow/current_cognitive_context/` | `exact_reuse` |
| CWR Envelope | this module | minimal new read-only reference wrapper; `simulation_only=true` |

No parallel Reducer, Read Model, State, Snapshot, or Context implementation is created.

## DryRun behavior

The six fixed cases validate reference compatibility, version references, reducer-only mutation authority, read-only boundaries, unknown preservation, Context isolation, Analysis Boundary admission eligibility, Context refresh, and Evidence revocation refresh semantics. The DryRun invokes neither real Reducer nor real Read Model and does not connect real Field State, a database, a model, a network, or a task runtime.

The Envelope contains references only. It has no mutation methods and no Hypothesis, Decision, or Experience surface.

## Stop condition

Stop after V0 static checks and the authorized fixture-only V1 runner/verifier complete. Do not infer semantic correctness, automatic Context selection quality, actual world correctness, Hypothesis/Decision behavior, performance, concurrency, persistence, or transport behavior.
