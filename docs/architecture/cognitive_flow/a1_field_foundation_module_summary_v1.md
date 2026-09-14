# A1 Field Foundation Module Summary v1

## Purpose and status

A1 is Luna's **Field Foundation and governed world-state foundation**. It
organizes the stable, governed inputs from which a Field can be represented:
Field Identity, Field Unit, Field Relation, Field State, temporal evolution,
and read-only snapshot foundations. It is not a World Model, knowledge base,
or cognitive-analysis system.

The authoritative state-mutation path is frozen:

```text
Field Event Candidate
  -> Field Event Admission / Temporal Validity
  -> Admitted Event
  -> Field State Reducer
  -> Field State
```

The **Field State Reducer is the unique Field State mutation authority**.

## Actual asset mapping

| Concern | Existing asset entry points | Role in A1 |
| --- | --- | --- |
| Field structure | `capabilities/cognitive_flow/field_kernel/core/field_identity_v1.py`, `field_unit_v1.py`, `field_relation_v1.py` | Field Identity, Unit, and structural Relation candidates. |
| Field state and snapshot | `field_state_v1.py`, `field_snapshot_v1.py`, `snapshot_api_v1.py` | Governed current state representation and derived read-only Snapshot foundation. |
| Admission boundary | `capabilities/midplatform/core/field_event_admission_types_v1.py`, `field_event_admission_api_v1.py` | Transforms a Field Event Candidate only through the governed admission boundary. |
| State mutation | `capabilities/midplatform/core/field_state_reducer/field_state_reducer_types_v1.py` | Sole producer of authoritative Field State changes. |
| Temporal organization | `capabilities/cognitive_flow/field_kernel/temporal_evolution/state_version_v1.py`, `transition_record_v1.py`, `history_projection_v1.py` | State Version, Transition Record, Temporal Evolution, and History Projection after reducer output. |
| Read representation | `capabilities/midplatform/core/field_state_read_model/module/field_state_read_model_module_types_v1.py` | Governed, read-only access to the current world representation. |

The governing architecture entries are
`field_kernel_authority_contract_plan_v1.md`,
`field_kernel_integration_contract_v1.md`,
`field_temporal_evolution_architecture_plan_v1.md`, and
`field_kernel_permission_matrix_v1.md` under
`docs/architecture/cognitive_flow/`.

## Responsibilities

A1 provides the foundation for:

- identifying a Field and its Units;
- representing non-causal structural Relations;
- accepting only governed, admitted field-event effects through the Reducer;
- maintaining Field State as the current governed world description;
- organizing State Version, Transition Record, Temporal Evolution, and
  History Projection from reducer-produced state;
- deriving read-only Field Snapshot foundations for governed queries.

Its direct governed input is an **admitted field event**. Its outputs are
Field State, State Version, Transition Record, temporal/history projection,
and Snapshot-reading foundations.

## Non-responsibilities and frozen prohibitions

A1 does not select Current Cognitive Context, perform Cognitive Analysis,
produce Hypotheses, interpret causes, make Decisions, take Action, or maintain
Experience, Self, or Hive structures. A2 may consume its state and temporal
representation only as read-only inputs.

The following routes are permanently prohibited:

- External Capability -> Field State;
- Cognitive Analysis -> Field State;
- Field Snapshot -> Field State;
- Current Cognitive Context -> Field State;
- Experience, Self, or Hive -> Field State while bypassing Admission and the
  Reducer.

## Maturity record

| Area | Current maturity |
| --- | --- |
| Architecture and authority contract | Complete for the A1 foundation. |
| Controlled object skeleton and contracts | Complete. |
| Fixture / simulation representations | Present; non-production only. |
| Runtime integration | Not completed by A1. |
| Cognitive analysis, decision, experience, self, and hive | Outside A1 and unimplemented here. |

This summary records architecture and existing assets; it does not change
their contracts, runtime behavior, or governance status.
