# Field Event Admission & Temporal Validity Module v1

## 当前阶段判断

- Phase: Phase-P1-Field-Kernel-Field-Event-Admission-Temporal-Validity-Module-v1-001
- Stage: Controlled Complete Module Implementation
- Execution Mode: Controlled Skeleton Implementation
- Previous Phase: Field Event and Temporal Validity Protocol Planning v1
- Previous Phase Decision: planning_assets_available
- Current Status Contract: WAITING_FOR_USER_TERMINAL_VERIFICATION

## 当前工作内容描述

In scope: a deterministic, in-memory admission boundary between Field Event Candidate and Field State Reducer. It provides structured types, temporal assessment, admission decisions, stable reason codes, a runner, and a final phase verifier.

Out of scope: persistence, queues, streaming, cross-device clock correction, semantic interpretation, full provenance graphs, Reducer execution, Field State mutation, Read Model changes, fact admission, registry/lifecycle/baseline/protocol mutation, and production activation.

## Formal API

```text
admit_field_event(event_candidate, policy, context) -> FieldEventAdmissionResultV1
```

`policy.evaluated_at` is mandatory and timezone-aware. The caller supplies it so identical input, policy, and context produce identical output. The module never reads the system clock.

## Input and Context

The event candidate supports `event_id`, `event_type`, `field_ref`, `occurred_at`, `observed_at`, `received_at`, `source_chain`, `evidence_refs`, `payload`, and `trace_ref`.

The controlled context contains only known event IDs for duplicate detection and latest occurred-at timestamps per field. Explicit policy values control age, disorder, and future tolerances. No context is loaded from a database, queue, network, model, or runtime store.

## Deterministic Decision Priority

1. Missing structural fields or invalid structures → `rejected_event`.
2. Known event ID → `duplicate_event`.
3. Missing temporal information or safely future-dated event → `deferred_event`.
4. Invalid/non-timezone-aware timestamp → `rejected_event`.
5. Event older than configured age → `expired_event`.
6. Invalid internal chronology or older-than-tolerance field sequence → `out_of_order_event`.
7. Otherwise → `admitted_event`.

Only `admitted_event` sets `reducer_eligible=true` and emits a `reducer_input_candidate`. That object remains `candidate_only=true` and `not_fact=true`.

## Stable Result Contract

Every result contains `admission_status`, `reason_code`, `event_ref`, `field_ref`, `temporal_assessment`, `evidence_refs`, `source_chain`, `trace_ref`, `evaluated_at`, and `reducer_eligible`. Decision steps preserve an explainable trace. The original event and context are not mutated.

## Required Pre-Read and Input Assets

- Field Event and Temporal Validity Protocol planning assets.
- Field State Reducer module input and error/trace types.
- Field State Read Model read-only boundary.
- Luna Engineering Phase Execution and Verification Governance v1.

## Target and Required Final Files

- `capabilities/midplatform/core/field_event_admission_types_v1.py`
- `capabilities/midplatform/core/field_event_admission_api_v1.py`
- `capabilities/midplatform/core/field_event_admission_contract_v1.json`
- `docs/architecture/field_kernel/field_event_admission_temporal_validity_module_v1.md`
- `tools/evaluation/midplatform/run_field_event_admission_temporal_validity_controlled_v1.py`
- `docs/architecture/field_kernel/verify_field_event_admission_temporal_validity_module_v1.py`

## Negative Guards

- No check weakening or hardcoded pass.
- No direct Field State mutation and no Reducer invocation.
- No candidate-to-fact promotion.
- No default admission when safe temporal assessment is unavailable.
- No database, queue, network, model, provider, action, or runtime loop.
- No registry, lifecycle, active baseline, or L1 protocol modification.

## Verification Authority

- V0: Agent did not execute static checks because this phase instruction forbids execution.
- V1: Agent did not execute runner or component validation.
- V2: User Terminal only; run `python docs/architecture/field_kernel/verify_field_event_admission_temporal_validity_module_v1.py` after running the controlled runner.
- V3: ChatGPT only after the complete V2 output is returned.
- Expected success decision: `READY_FOR_CHATGPT_V3_AUDIT`.
- Expected success next: return complete verifier output to ChatGPT.
- Expected failure decision: `BLOCKED_BY_VERIFIER_FAILURE`.
- Expected failure next: remediate only failed module assets and rerun V2.

## Stop and Blocker Conditions

Stop at `WAITING_FOR_USER_TERMINAL_VERIFICATION` after the six required files exist. Missing artifacts, contract drift, syntax/import failure, boundary violation, or controlled-case failure blocks verification. This phase does not declare GO or enter another phase.

