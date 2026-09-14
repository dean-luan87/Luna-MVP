# Existing binding and runtime contracts

`capabilities/midplatform/core/cognitive_flow/integration/capability_model_provider_binding_controlled/types_v1.py` 已有：

- `CapabilityModelBindingCandidateV1`：Capability Governance 拥有的 Capability↔Model candidate；需要 model asset/declaration。
- `ModelProviderBindingCandidateV1`：Provider Governance 拥有的 Model↔Provider binding candidate；需要 model asset/version/loader/provider declaration。
- `BindingResultV1` / `BindingChainResultV1`：candidate-only binding validation result。

这些是纯 candidate contract，但不是可由 optional-model Provider Target 直接构造的 generic Provider Target Binding。现有 runtime ingress `ProviderRuntimeRequestV1` 还要求 `execution_instance_ref`；`RuntimeObservationEnvelopeV1` 要求 observation/execution/provider identity，因此不能在本阶段使用。

结论：当前采用 Route C 的最小顺序裁决与 preparation seam。`ProviderBindingRuntimePreparationCandidateV1` 是受治理的前置投影，不替换既有 Model↔Provider Binding contract。
