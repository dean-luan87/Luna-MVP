# Entity–Neural Handshake Model v1

## Purpose

The Entity–Neural Handshake defines the candidate-based protocol establishment required before an Entity can advertise capabilities or receive scoped CWO routing candidates. It is an architecture contract, not a connection/runtime implementation.

```mermaid
flowchart LR
    D[Discovery Candidate] --> A[Authentication / Trust Candidate]
    A --> C[Capability Exchange Candidate]
    C --> P[Protocol Alignment Candidate]
    P --> S[Signal Channel Establishment Candidate]
    S --> R[Eligible Entity Routing Candidate]
```

## Handshake stages

| Stage | Purpose | Does not grant |
|---|---|---|
| Discovery | Identify a potential Entity endpoint. | Automatic admission or work assignment. |
| Authentication | Verify bounded owner/trust relationship. | Brain/Memory authority. |
| Capability exchange | Obtain advertised roles, constraints, and profiles. | Provider execution. |
| Protocol alignment | Confirm signal schemas, versions, trace, and boundary compatibility. | Protocol self-modification. |
| Signal channel establishment | Establish a scoped candidate communication path. | Persistent autonomous control channel. |

## Invariants

- Handshake identity is Entity identity, never personality identity.
- A successful channel permits only protocol-scoped candidate exchange.
- Any capability work still requires CWO routing and Middleware feasibility organization.
- Failure/degradation returns a candidate to Neural Governance; it never creates a new Goal or changes Brain state directly.
