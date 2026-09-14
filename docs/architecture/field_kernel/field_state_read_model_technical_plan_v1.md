# Field State Read Model Technical Plan v1

## Phase

Phase-P1-Field-Kernel-Field-State-Read-Model-Asset-Inventory-And-Technical-Planning-v1-001

Technical planning only. No runtime implementation.

## 1. 模块职责

1. read-only state access over reducer-produced state candidates.
2. deterministic projection generation for read consumers.
3. task/scene/object/time scoped query execution (candidate-only).
4. provenance/trace/version/replay preservation in every read result.
5. unavailable/stale/insufficient semantics without fallback fabrication.

## 2. 禁止权责

1. state mutation.
2. event reduction.
3. fact admission.
4. evidence fabrication.
5. real model execution.
6. action/task execution.
7. runtime loop ownership.

## 3. 最小输入合同候选

Required:
- query_id
- requester_ref
- query_scope
- field_state_ref or snapshot_ref
- required_fields
- trace_ref
- replay_key

Optional:
- task_ref
- scene_ref
- object_ref
- temporal_scope

## 4. 最小输出合同候选

Required:
- query_id
- read_status
- projection
- state_version
- source_state_ref
- provenance_refs
- trace_ref
- replay_key
- boundary_flags

Optional:
- stale_reason
- insufficiency_reason

## 5. 状态语义候选

- read_ready
- partial_projection
- insufficient_state
- stale_state
- state_unavailable
- query_rejected

## 6. 与相关模块关系

1. Field State Reducer
- upstream state candidate authority and mutation authority source.

2. Task Manager
- optional task scope selector/context consumer.

3. Observation Manager
- optional evidence lineage context, no fact admission handoff.

4. Navigation Manager
- optional view consumer for route/safety read contexts.

5. Field Perception Orchestrator
- optional field context consumer of read projections.

6. Situation Understanding
- optional context enrichment consumer; read model remains authoritative only for read projection surface.

## 7. 后续实施路线

1. Controlled Skeleton
- create read-model skeleton and boundary guards (candidate-only, no write).

2. Contract DryRun
- validate query/result schemas and status semantics with fixed fixtures.

3. Controlled Read Runtime
- implement read-only in-memory projection/query processor with deterministic replay.

4. Module Integration
- add integration runner for scope queries, stale/insufficient/unavailable branches.

5. Promotion / Baseline
- prepare manifest, baseline, registry dependency alignment and controlled promotion evidence.

## Governance and Boundary Notes

- Reducer remains the only mutation authority.
- Read Model remains projection/query authority only.
- no state write, no fact admission, no reducer override.
- trace_ref, replay_key, provenance_refs, state_version are mandatory preservation signals.
