# Admission Authority / Responsibility Matrix

| Action | Authority | Required evidence | Result receiver | Failure owner |
|---|---|---|---|---|
| Resolve logical capability | Capability Registry / Universal Slot Governance | Requirement, registry, scope, slot | Admission coordination and A boundary | Capability Governance |
| Resolve model identity/version/path | Model Manager / Model Governance | Registry and model contract | Capability Admission | Model Governance |
| Report dependency health | System Diagnostics | Probe/health candidate | Model/Capability Admission | Diagnostic evidence source for evidence quality |
| Report runtime/device health | Runtime Health / Resource Governance | Health/resource candidates | Capability Admission | Health/resource evidence owner |
| Verify integrity evidence | Integrity/Model Governance boundary | Declared metadata + observed evidence | Capability Admission | Integrity boundary |
| Decide Runtime Admission | Capability Admission Governance | All required refs and valid state | Executable Capability boundary | Capability Admission |
| Produce Executable Capability Candidate | Capability Admission / Runtime handoff | Accepted admission candidate | Provider Admission | Admission authority |
| Decide Provider admission | Provider Governance / FPO | Bounded request, model admission, provider compatibility, evidence expectations | Provider adapter | Provider/FPO admission owner |
| Invoke Provider | Authorized Provider adapter | Valid Provider admission | Observation Gateway | Provider/runtime executor |
| Persist refs | Loop mechanical engine | Supplied refs/commands | A/Brain via mechanical return | Loop for mechanical persistence only |

## Paired authority rule

No module is responsible for a Provider outcome unless it had authority to
admit or execute that outcome. Transport of an admission ref does not transfer
the admission authority.

