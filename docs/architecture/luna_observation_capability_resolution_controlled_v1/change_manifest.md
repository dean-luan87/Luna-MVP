# Change Manifest

## Added

- `capabilities/midplatform/model_manager/registries/universal_capability_slot/observation_demand_capability_resolution_v1.py`
- `capabilities/evaluation/observation_capability_resolution_controlled/`
- 本目录中的 architecture documentation。

## Modified

- `capabilities/midplatform/model_manager/registries/universal_capability_slot/__init__.py`
  exports the narrow bridge/resolution projection。
- `docs/architecture/README.md` adds this phase index entry。

## Reused

- `Capability Registry / Capability Governance` ownership boundary；
- `CapabilityRequirementV1`、`CapabilityModuleV1`、`UniversalCapabilitySlotV1` 作为
  compatibility context；
- existing capability admission/readiness vocabulary；
- Cognitive Flow `ObservationDemandCandidateV1` 与完整 upstream lineage。

## Not Modified

- Observation Demand、Strategy Coordination、Branch、Need、Sufficiency、Stop；
- Model Manager、Provider Manager、FPO、Observation Gateway 与 runtime execution。

## Deferred

Provider Binding、Model Binding、Capability Activation、Capability Scheduling、Resource
Scheduling、Perception Routing、FPO/Gateway runtime request、Camera/OCR/SLAM runtime、
Evidence Ingress/Fusion、Conflict Resolution、Decision、Task、Action 与 real-world
acquisition。

当前状态：`WAITING_FOR_USER_TERMINAL_VERIFICATION`。
