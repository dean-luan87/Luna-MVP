# Global Policy versus Enforcement Matrix v1

| Domain | Policy owner / version authority | Evidence source | Enforcement points | Enforcement responsibility |
|---|---|---|---|---|
| Safety | Brain global Safety authority; Safety Governance sub-boundary for domain policy refs | Field, Context, Diagnostics, Observation, Action, human input | Envelope/Decision/Task/Runtime/Provider/Action/Observation | each enforcing boundary must reject stale/revoked policy; policy error is Brain/Safety responsibility |
| Permission | Brain global/scoped authority; Permission Governance owns permission contract/scope/ref | Identity, Role, Relationship, Context, OS permission evidence | Observation, Capability Runtime Admission, Provider, Action | consumer boundary enforces supplied scope; grant/deny/revocation error is Permission responsibility |
| Resource | Brain ceilings/reserves/priority; Resource Governance budget/reservation policy | Diagnostics/runtime measurements | Attention, Runtime Admission, Provider, Task, Action | allocator/enforcer respects ceilings; measurement error is Diagnostics responsibility |
| Brain Grant | Brain | Concern, Goal, policy, source versions | Working Envelope and downstream boundaries | Brain for grant; consuming boundary for stale-use enforcement |
| Capability constraints | Capability Governance for logical contract; Runtime Admission for executable assessment | requirement, mapping, model/provider refs | Runtime Admission, Provider, Observation/Action | corresponding capability/admission owner |
| Protocol | Protocol Governance | change proposal, registry, fingerprint/drift | validators, producer/consumer bindings, adapters | Protocol Governance for compatibility declaration; producer/consumer for implementation conformance |

Repeated checks are enforcement of one versioned policy, not new policy ownership. A valid protocol, model, capability, Grant or diagnostic PASS never bypasses Safety, Permission or Resource enforcement.

## Precedence

Hard Safety and Permission prohibitions constrain execution before Resource optimization and local priority. Protected Resource reserves constrain local priority. Brain owns global override/escalation. Exact cross-constraint precedence is a recorded contract gap, not a license for Attention, Task or Runtime to invent ordering.

