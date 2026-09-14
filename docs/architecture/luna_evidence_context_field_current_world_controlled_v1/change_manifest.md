# Change manifest

## Added

- `capabilities/midplatform/core/evidence_to_field_event_adapter_v1.py` —
  minimal candidate-only Evidence-to-Field Event bridge.
- `capabilities/evaluation/evidence_context_field_current_world_controlled/` —
  fixtures, controlled engine, runner, and verifier.
- This architecture documentation directory.

## Reused without semantic changes

- `FieldEventCandidateV1` and `admit_field_event`;
- `FieldKernelReducerAdapterV1` and `FieldStateReducerModuleV1`;
- `FieldStateV1` projection and `CurrentWorldCandidateV1`;
- Context Foundation skeleton;
- Governance Backbone.

No existing Provider, Session, Invocation, Runtime Observation, Gateway,
Evidence, Cognition, FPO, Reducer, or Governance Backbone business file was
modified by this phase.

The existing Field Reducer remains candidate-only and non-persistent. No new
owner, store, Truth manager, or Current World manager was created.
