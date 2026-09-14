# Change manifest

## Added

- FPO integration compatibility candidate contract and pure formation
  function.
- Controlled fixtures, evaluation wrapper, runner, and verifier.
- Ownership, compatibility, contract, fixture, guard, and verification docs.

## Modified

- No previously verified cognitive, routing, FPO runtime, Gateway runtime,
  Provider, or Model implementation was modified.

## Reused

- `PerceptionRoutingCandidateV1` and its existing candidate-only lineage.
- Existing FPO Active Observation Control owner and its control taxonomy.
- Existing Observation Gateway ingress/admission contracts as documented
  downstream boundaries.
- Existing FPO `ObservationRequestCandidateV1` only for compatibility review;
  it is not repurposed.

## Not modified

- Observation Gateway runtime and `ObservationIngressRequestV1`.
- FPO runtime and Active Observation Control engine.
- Capability Registry / Capability Admission.
- Provider Manager, Model Manager, FPO/Gateway runtime submission.

## Deferred

- Runtime admission decision and runtime grant.
- Gateway submission and FPO active-observation runtime request.
- Provider/Model binding and invocation.
- Capability activation, Slot reservation, and resource scheduling.
- Routing admission/selection, Attention scheduling, and execution.
- Camera/OCR/SLAM/VLM runtime and Observation execution.
- Evidence ingress/fusion, Conflict Resolution, Decision, Task, and Action.
