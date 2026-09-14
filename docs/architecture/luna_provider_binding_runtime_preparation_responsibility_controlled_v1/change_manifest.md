# Change manifest

## Added

- Provider Governance canonical `provider_binding_runtime_preparation_v1.py`。
- `capabilities/evaluation/provider_binding_runtime_preparation_responsibility_controlled/` fixtures、engine、runner、verifier。
- 本阶段责任、契约、顺序与验证文档。

## Reused

- `ProviderRuntimeTargetPreparationCandidateV1`。
- Existing `CapabilityModelBindingCandidateV1` / `ModelProviderBindingCandidateV1` 作为后续 binding contract evidence。
- Provider Runtime Governance、Provider Registry、FPO、Runtime Observation、Observation Gateway ownership contracts。

## Modified

- `docs/architecture/README.md` 仅增加索引条目。

## Not Modified

- Cognition、Observation Demand、Capability Resolution、Routing、FPO runtime、Provider Registry、Model Manager binding types、Gateway runtime、Execution Instance、Runtime Session。

## Deferred

Provider Binding decision、Model Binding、Runtime Allocation、Execution Instance、Provider Session、Provider admission execution、Gateway Runtime Admission、slot/resource reservation、capability activation、Provider/Model invocation、Observation Execution、Evidence Ingress/Fusion、Decision、Task、Action。
