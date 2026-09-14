# Field State Read Model Asset Inventory v1

## Scope

Phase-P1-Field-Kernel-Field-State-Read-Model-Asset-Inventory-And-Technical-Planning-v1-001

Asset inventory only. No runtime implementation, no state write, no reducer modification.

## A. 现有正式主干

1. Field State Reducer capability formal mainline
- capabilities/midplatform/core/field_state_reducer/module/
- capabilities/midplatform/core/field_state_reducer/state_reduction/
- tools/evaluation/midplatform/run_field_state_reducer_module_integration_v1.py
- capabilities/registry/manifests/field_state_reducer_manifest_v1.json
- capabilities/registry/baselines/field_state_reducer_module_baseline_v1.json
- capabilities/registry/luna_capability_registry_v1.json (luna.field_state_reducer)
- capabilities/registry/luna_capability_module_baseline_registry_v1.json (baseline flags)

2. Protocol assets directly tied to admitted event / temporal validity / output contract
- docs/architecture/luna_field_state_reducer_technical_planning_v1/field_state_reducer_output_contract_v1.json
- docs/architecture/luna_field_event_temporal_validity_protocol_planning_v1/temporal_validity_schema_v1.json
- docs/architecture/luna_field_event_temporal_validity_protocol_planning_v1/field_event_temporal_validity_protocol_negative_guards_v1.json

## B. 可直接复用资产

1. Input/Output surface and status registry
- module/field_state_reducer_module_types_v1.py
- module/field_state_reducer_module_output_builder_v1.py

2. Deterministic projection candidate and boundary flags
- module/field_state_reducer_read_projection_candidate_v1.py
- module/field_state_reducer_module_api_v1.py

3. Provenance/trace/replay and reduction handoff
- state_reduction/state_reduction_provenance_replay_v1.py
- state_reduction/state_reduction_selection_handoff_builder_v1.py
- state_reduction/state_reduction_types_v1.py

4. Contract loading pattern (planning-source contracts)
- state_reduction/state_reduction_contract_loader_v1.py

## C. 应扩展资产

1. Extract Read Model authority from reducer output candidate semantics
- extend from read_model_projection_candidate to independent Field State Read Model contracts.

2. Expand projection scope
- from reducer-local projection to task/scene/object/time scoped query surface.

3. Expand status semantics
- from reducer statuses to dedicated read model statuses:
  read_ready, partial_projection, insufficient_state, stale_state, state_unavailable, query_rejected.

4. Expand query contract
- add requester_ref, query_scope, required_fields, optional task/scene/object/temporal selectors.

## D. Legacy / stub / duplicate assets

1. Skeleton/dryrun legacy artifacts (non-formal runtime)
- field_state_reducer_skeleton_v1.py
- field_state_reducer_controlled_dryrun_cases_v1.py
- run_field_state_reducer_controlled_skeleton_v1.py
- verify_field_state_reducer_controlled_skeleton_implementation_v1.py

2. Bytecode artifact (non-source)
- module/__pycache__/field_state_reducer_read_projection_candidate_v1.cpython-310.pyc

3. Naming drift risk
- dependency map contains planned capability id luna.field_read_model; target module naming in this phase is Field State Read Model. Naming alignment is required before promotion.

## E. 真实缺口

1. No dedicated Field State Read Model module mainline exists under capabilities/midplatform/core.
2. No dedicated query schema for read-only projection/query authority.
3. No dedicated result schema for unavailable/stale/insufficient semantics.
4. No dedicated module-level planner checker for read-model technical planning completeness.
5. No dedicated integration runner/verifier for Field State Read Model (planning phase only).

## F. 结构性 blocker

1. Capability naming ambiguity
- planned dependency edge uses luna.field_read_model, while this phase uses Field State Read Model terminology.

2. Ownership boundary must stay strict
- Reducer remains sole mutation authority; Read Model must stay projection/query only.

3. Promotion precondition blocker
- no formal read-model contracts and no module inventory baseline for read-model yet.

## G. Dependency 与 ownership 边界

1. Ownership
- Field State Reducer: only mutation authority (candidate reduction orchestration), no persistence/fact admission/action/runtime ownership.
- Field State Read Model: read-only projection/query authority, never mutation/fact admission/reduction owner.

2. Dependency
- Required upstream: luna.field_state_reducer (source state candidate/projection lineage).
- Optional context dependencies: Task Manager, Observation Manager, Navigation Manager, Field Perception Orchestrator, Situation Understanding.

3. Boundary invariants
- candidate-only processing.
- no direct state mutation.
- no fact admission.
- no evidence fabrication.
- no model/provider execution.
- no task/action execution.
- no runtime loop ownership.
