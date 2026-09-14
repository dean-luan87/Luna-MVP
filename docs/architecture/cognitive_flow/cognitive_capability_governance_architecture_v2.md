# Cognitive Capability Governance Architecture v2

## Position

Capability Governance Plane belongs to **Cognitive Middleware**. It governs which registered capability/provider can be admitted, described, calibrated, resolved, observed, degraded, or retired. It does not own Goal, Attention, Decision, Truth, Action, or State mutation.

Shared generic Protocol Governance remains under the Cognitive Neural/Governance boundary. The Middleware plane consumes its compatibility/admission/trace contracts; it does not create a second Protocol Manager.

```mermaid
flowchart TB
    subgraph Middleware[Cognitive Middleware]
        subgraph Plane[Capability Governance Plane]
            registry[Capability Registry]
            admission[Admission / Permission Validation]
            contract[Capability Contract / Manifest Mapping]
            baseline[Baseline / Calibration Reference]
            lifecycle[Lifecycle Governance]
            health[Health / Diagnostics]
            resolver[Capability Resolver]
            registry --> resolver
            admission --> resolver
            contract --> resolver
            baseline --> health
            lifecycle --> resolver
            health --> resolver
        end
        resource[Resource Manager]
        evidence[Evidence Gateway]
        resolver --> resource
        resolver --> evidence
    end

    protocol[Shared Neural Protocol Governance<br/>compatibility / trace / boundary] --> admission
    protocol --> contract
    providers[Capability Providers<br/>Model / Hardware / External Service] --> health
    providers --> evidence
    resolver --> providerCandidate[Capability Candidate Set]
    providerCandidate --> providers
```

## Plane responsibilities

| Plane concern | Reused asset class | Result form |
|---|---|---|
| Registry | Canonical Capability Registry | registered capability/provider metadata candidate |
| Admission | Model/Skill/Permission admission contracts | admission/constraint/failure candidate |
| Contract/Manifest | manifests, schemas, adapter/profile references | contract compatibility candidate |
| Baseline/Calibration | baseline registry and recalibration assets | diagnostic/calibration reference candidate |
| Lifecycle | lifecycle registry and provider lifecycle governance | availability/degradation/retirement candidate |
| Health/Diagnostics | manager diagnostics, trace/replay | reliability/resource/failure candidate |
| Resolver | model/provider routing inputs plus resource constraints | Capability Candidate Set |

## Authority boundary

- Brain/Neural signals state what information is needed.
- Capability Governance Plane states what registered/admitted/feasible capability alternatives exist.
- Provider execution is future Runtime Admission work.
- Evidence Gateway is the only cognition-facing output boundary.

## Status

`COGNITIVE_CAPABILITY_GOVERNANCE_ARCHITECTURE_V2_READY_WITH_NOTES`

`WAITING_FOR_USER_TERMINAL_VERIFICATION`
