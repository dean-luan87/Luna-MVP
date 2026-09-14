# System Diagnostics Existence Test v1

| Alternative | Finding |
|---|---|
| Brain sub-boundary | Rejected as primary owner: Brain would acquire low-level probes and lose global-policy separation. |
| Model Manager submodule | Too narrow; cannot own device, provider, protocol, or cross-domain facts. |
| Runtime Admission helper | Too late and consumer-specific; diagnostics must be reusable before admission. |
| Provider helper | Cannot explain dependency/config/resource facts outside one provider. |
| Generic observability utility | Too weak for provenance, classification, freshness, and responsibility. |
| Maintenance-plane diagnostic service | Correct operating context, but remains a boundary/function, not an automatically created Manager. |
| Independent Diagnostics boundary | **KEEP**: best separation of observation/classification from policy and consequence. |

The independent boundary is justified by cross-domain reuse, source independence,
admission separation, maintenance integration, and accountable diagnostic
failure responsibility. Its authority remains narrow: observed state and
evidence classification only.
