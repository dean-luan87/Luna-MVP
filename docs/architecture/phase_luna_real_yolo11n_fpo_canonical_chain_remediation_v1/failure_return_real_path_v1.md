# Failure Return Real Path v1

| Failure | Detection | Responsibility | Return |
|---|---|---|---|
| Missing canonical context | FPO compatibility seam | FPO adapter translation correctness; upstream owners retain source responsibility | Provider not admitted; no invocation |
| Binding mismatch/stale | Compatibility seam | Capability Governance or Provider Governance according to binding | Provider not admitted; invalidation retained |
| Runtime candidate unavailable | Upstream Runtime Admission | Runtime Admission | FPO acquisition remains blocked |
| Model asset/dependency unavailable | Model readiness/Diagnostics evidence | Model Governance / Diagnostics for their respective facts | Provider not admitted |
| Provider invocation failure | Provider adapter | Provider boundary | Provider result failure/evidence path; no semantic replanning in FPO |
| Evidence mapping failure | FPO/Gateway adapter | Mapping boundary | Candidate failure with trace/provenance |

A receives local semantic consequence later; Brain receives only global
consequence through the canonical Outcome path.

