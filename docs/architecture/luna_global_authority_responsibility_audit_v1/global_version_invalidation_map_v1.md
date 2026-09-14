# Global Version and Invalidation Map v1

There is no global version. Each owner versions its state or contract, and downstream bindings carry source-version refs.

| Domain | Version authority | Representative invalidation | Affected bindings / admission | Semantic consequence owner |
|---|---|---|---|---|
| Brain Concern/Grant | Brain | revoke, expiry, supersession | Envelope, Decision, Task, runtime admissions | Brain/A |
| Intent | Intent Governance | intent change/supersession | Envelope, Decision, Task | Intent Governance / Brain |
| Role / Perspective | source / Projection | role change, projection invalidation | Envelope, Permission, Semantic/Snapshot | A/Brain |
| Field / Context / World | respective source/formation | new event, stale evidence, refresh | Envelope, Snapshot, A | Field/Context/State Formation then A |
| Task / Decision / Action | respective owner | change, revoke, cancel, stale source | downstream readiness/admission | Decision/Task/Action |
| Capability / Model / Provider | respective owner | mapping/version/retirement/unavailable | Runtime/Provider/Observation/Action | Capability/Decision/A |
| Safety/Permission/Resource | domain governance under Brain | policy change, revocation, exhaustion | Envelope, Runtime, Provider, Action | Brain/A/Outcome |
| Observation/Evidence | Observation/Gateway | stale, duplicate, source mismatch | World/Field/Snapshot/A | A |
| Diagnostics | Diagnostics | TTL expiry, restart, device/runtime change | Runtime/Provider/Action admission | admission owner |
| Working Envelope | Envelope binding boundary | any required source/constraint invalidation | Semantic/Snapshot/A | A/Brain |
| Protocol | Protocol Governance | supersession, deprecation, incompatibility | bindings/adapters/validation | affected source owner + Protocol Governance |
| Outcome | Outcome/Brain | stale/mixed result or new evidence | assimilation/follow-up | Brain |

## Propagation rule

Source change → versioned invalidation ref → affected admission/binding rejects or marks stale → new candidate where permitted → named semantic owner decides consequence. No source owner directly mutates another owner’s state.

## Representative traces

- Permission revocation → invalidates Envelope/Runtime/Provider/Action admission → mechanical block/cancel → A/Brain evaluate consequence.
- Model retirement → invalidates new Runtime candidates and mappings → Provider cannot admit retired asset → Capability/A choose alternative cognition.
- Protocol supersession → binding drift → Diagnostics evidence → Protocol lifecycle consequence → producer/consumer adaptation.
- Evidence stale → Gateway/World/Snapshot binding invalidation → A decides refresh, defer or reconsider.

