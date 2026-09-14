# Change manifest

## Added

- `capabilities/midplatform/core/observation_gateway/perception_routing_candidate_v1.py`
- `capabilities/evaluation/observation_perception_routing_controlled/`
- this controlled implementation documentation set

## Modified

No pre-existing canonical cognitive, capability-resolution, Gateway, or FPO
implementation was modified.

## Reused

- `ObservationDemandCandidateV1` from Cognitive Flow;
- `ObservationDemandCapabilityRequirementAdapterV1` and
  `ObservationDemandCapabilityResolutionCandidateV1` from Capability
  Registry / Capability Governance;
- existing Observation Gateway/FPO contracts as compatibility references only.

## Not modified

Observation Demand owner, Capability Resolution owner, Capability Registry,
Capability Slot lifecycle, Observation Gateway, FPO, Provider Manager, and
Model Manager.

## Deferred

Routing Admission, Routing Selection, Capability Binding/Activation, Slot
Reservation, Resource Scheduling, Attention Scheduling, FPO runtime request,
Observation Gateway submission, Provider/Model binding, Camera/OCR/SLAM/VLM
runtime, Observation Execution, Evidence Ingress/Fusion, Conflict Resolution,
Decision, Task, Action, and real-world acquisition.

Sandbox integration remains `DEFERRED`; this phase uses an independent
controlled evaluation package.
