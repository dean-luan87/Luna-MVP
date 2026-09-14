# Luna Capability Admission Matrix v1

## Admission Checks

| admission stage | required evidence | governing authority | denial condition | result boundary |
| --- | --- | --- | --- | --- |
| Capability Proposal | stable ID candidate, owner, required input, expected output, dependencies | L1 Capability Registry reference | missing/duplicate identity or undeclared owner | proposal only |
| Capability Assessment | purpose, boundary, risk, implementation/dependency declaration | Governance Core | capability claims authority outside declared scope | assessment only |
| Contract Compatibility Check | input/output Contract refs, candidate/Fact boundary, trace/provenance rules | L1 Protocol Governance | schema/enum/boundary mismatch | no execution eligibility |
| Protocol Compatibility Check | allowed Protocol versions and lifecycle state | L1 Protocol Governance | inactive/deprecated-incompatible/bypassed version | no dependency approval |
| Permission Scope Review | existing Permission/Admission reference and denied operations | L1 Permission/Admission | self-granted, overbroad, State/Fact/Decision scope | no permission grant |
| Authority Approval | L0 alignment, review evidence, diagnostics plan | designated L1 authorities | constitutional/boundary conflict | no registration/activation |
| Registration | Registry-owned lifecycle decision | L1 Capability Registry | required evidence incomplete or duplicate lifecycle | identity/lifecycle record only |

## Capability Boundary

| Capability may | Capability must not |
| --- | --- |
| process governed input; generate candidate output; provide declared service within a future Execution Context | modify Constitution/Protocol; grant Permission; bypass Admission; write State; become Fact authority; execute Decision/Action without separate authority; self-register/self-upgrade |

## Upgrade Governance

| upgrade type | minor | major | breaking | required handling |
| --- | --- | --- | --- | --- |
| implementation change | internal refactor preserving Contracts, dependencies, flags, and output semantics | behavior change needing regression evidence | changes candidate/Fact or authority boundary | minor review; major compatibility review; breaking replacement candidate |
| dependency change | additive compatible governed dependency | dependency requiring new Protocol/Permission assessment | ungoverned or incompatible dependency | dependency inventory and Protocol review |
| input/output change | optional compatible field/reference addition | required Contract evolution | remove/reinterpret input/output or candidate semantics | Protocol lifecycle change governance and migration |
| permission change | diagnostic/reference metadata only | newly requested governed scope | self-grant, scope expansion, State/Fact/Decision privilege | Permission/Admission review; no Capability-only approval |
| protocol dependency change | compatible Active Protocol version selection | new Protocol version migration | bypass/deprecated incompatible Protocol dependency | Protocol compatibility and rollback plan |

Breaking upgrades create a replacement Candidate; they cannot mutate an Active/Frozen Capability in place. Rollback selects the prior compatible Frozen/Active baseline by reference and preserves historical trace.

