# Runtime Admission Authority / Responsibility Matrix

| Action | Decision authority | Evidence provider | Executor | Result receiver | Failure responsibility |
|---|---|---|---|---|---|
| Select logical capability | Capability Governance / Registry within admitted request | Requirement, registry, scope | Resolution governance | A/Observation handoff | Capability Governance |
| Resolve model asset | Model Manager / Model Governance | Registry, contract, manifest | Resolver | Capability Admission | Model Governance for resolution failure |
| Declare model metadata | Model Manifest / Model Governance | Registered asset contract | Registry/contract repository | Model Admission | Model Governance |
| Verify dependency health | System Diagnostics evidence; reviewed by Admission | Dependency probe/runtime diagnostics | Existing diagnostic probe only | Model/Capability Admission | Diagnostic source for evidence quality; Admission for decision |
| Verify observed integrity | Integrity/admission boundary using Model Governance data | Observed checksum evidence | Integrity verifier/terminal adapter in transition | Model/Capability Admission | Integrity boundary for invalid/missing evidence |
| Admit executable capability | Capability Admission Governance | Model, Provider, Runtime, permission/resource evidence | Capability Runtime handoff | Observation/FPO | Capability Admission |
| Admit Provider invocation | Provider Governance/FPO under Capability Admission | Provider session, model admission, bounded request | Provider adapter | Observation Gateway | Provider/FPO admission boundary |
| Invoke Provider | Authorized Runtime/Provider adapter | Valid admission candidate | Provider adapter | Observation Gateway | Provider adapter/runtime |
| Return evidence | Observation Gateway/FPO | Provider output and provenance | Gateway normalization/routing | A assessment boundary | Evidence gateway/provider boundary |
| Handle admission failure | Capability Admission for candidate status; A receives evidence gap | Failure candidate | No Provider invocation if blocked | A/Brain governance as appropriate | The owner that made the failed admission decision |

## Pairing rule

No transport module becomes responsible merely because it carries a ref. Every
admission result must identify its decision authority, evidence basis, result
receiver, and error owner.

