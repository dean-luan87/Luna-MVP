# Ownership and authority

| Boundary | Authority | Not owned |
| --- | --- | --- |
| FPO / Active Observation Control | semantic continuation, stop, redirect, provider-switch control | runtime session identity or invocation |
| Permission / Admission Manager | Runtime Execution Grant | Provider session lifecycle or invocation |
| Runtime Executor | execution instance and mechanical allocation lifecycle | Provider semantic choice or observation meaning |
| Provider Runtime Governance | Provider runtime session lifecycle and controlled invocation boundary | cognition, Gateway ingress, world truth |
| Observation Gateway | runtime observation ingress/admission proof | Provider selection and pre-session execution authorization |

`BoundedProviderSessionCandidateV1` 是 FPO semantic-control candidate；
`ProviderRuntimeSessionV1` 是本阶段新增的 authoritative synthetic lifecycle
record。两者不能互换。

`ProviderRuntimeRequestV1` 属于 candidate-only downstream request，并在现有
真实 OCR adapter 路径中可进入实际 Provider 调用，因此本阶段不复用它。
