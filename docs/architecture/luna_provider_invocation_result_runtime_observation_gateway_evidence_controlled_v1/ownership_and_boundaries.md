# Ownership and boundaries

| Boundary | Owner | Responsibility | Not responsible for |
|---|---|---|---|
| Invocation result | Provider Runtime Governance | execution-domain outcome and failure | world meaning |
| Result adapter | existing provider-runtime-to-observation integration boundary | shape conversion and lineage preservation | semantic authority or truth |
| Runtime observation envelope | existing Observation Gateway contract | ingress-shaped observation reference | sufficiency or world truth |
| Gateway admission | Observation Gateway Governance | ingress validation, provenance, integrity | provider selection, execution, truth |
| Evidence packaging | existing Gateway evidence path | source-linked candidate evidence | interpretation, sufficiency, Current World |
| Semantic continuation | FPO / Active Observation Control | continue/stop/redirect and sufficiency | this phase's formation |

`BoundedProviderSessionCandidateV1` remains an FPO semantic candidate and is not treated as a runtime session. `ProviderInvocationResultV1` is the sole upstream result consumed by the new adapter.
