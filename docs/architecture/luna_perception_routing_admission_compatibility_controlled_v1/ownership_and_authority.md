# Ownership and authority

| Boundary | Current owner | Meaning in this phase |
|---|---|---|
| Capability inventory, slot lifecycle, capability admission, Slot reservation/activation | Capability Registry / Universal Slot Governance | Upstream source-owned eligibility/lifecycle; not re-resolved or mutated here |
| Active-observation control and continuation | Field Perception Orchestrator / Active Observation Control | Existing STOP, CONTINUE, REDIRECT, SWITCH_PROVIDER, ADD_CAPABILITY, RECONSIDER, DEFER, FAIL semantics |
| Runtime ingress admission and evidence routing | Observation Gateway Governance | Existing Gateway runtime ingress boundary and live-mode admission proof |
| Provider/model binding | Provider Governance / Model Manager | Downstream binding; not formed here |
| Compatibility projection | This phase in the existing FPO integration namespace | Candidate-only handoff shape only |

There is no standalone Routing Admission Governance owner in the inspected
repository. A new super-owner was not required.

FPO and Gateway are complementary, not interchangeable: FPO controls the
active observation semantic lifecycle, while Gateway validates/adopts a
runtime ingress and produces its Gateway-owned runtime admission proof. This
phase reaches neither runtime authority.

The existing `Capability Admission Governance` decision means a capability is
eligible within the capability system. It does not imply that a particular
observation route is admitted for runtime execution.
