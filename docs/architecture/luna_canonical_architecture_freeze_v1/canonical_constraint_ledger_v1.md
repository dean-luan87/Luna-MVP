# Canonical Constraint Ledger v1

## Precedence

1. Hard Safety
2. Hard Permission
3. Grant validity and scope
4. Protected Resource ceiling/reserve
5. Resource degradation/optimization
6. Local Attention/Task/Decision priority

| Constraint | Policy/version owner | Evidence source | Enforcement points | Revocation / failure responsibility |
|---|---|---|---|---|
| Safety | Safety/Brain | perception, Field, Context, Diagnostics, Action Result, human/external input | Decision, Task, Runtime Admission, Provider, Observation, Action | Policy error → Safety/Brain; enforcement error → enforcing boundary |
| Permission | Permission Governance | Identity/Role/Relationship/Context, OS/service access | Observation, Runtime, Provider, Action, data access | Revocation invalidates dependent candidates; policy error → Permission |
| Grant | Brain | Goal/Concern/priority/policy/source refs | Envelope, A, Decision, Task, Runtime, Action | Brain owns scope/version/revocation; consumers block stale Grant |
| Resource | Resource Governance | Diagnostics measured facts, priority, reserve policy | Attention, Task, Runtime Admission, Provider, Action | Resource policy/reservation error → Resource; measurement error → Diagnostics |
| Protocol | Protocol Governance | source-owner proposal, registry, drift diagnostics | static/runtime validation, adapters, admissions | Protocol lifecycle error → Protocol; consumer adaptation error → consumer |
| Capability constraint | Capability Governance | Requirement, Slot, mappings, declarations | Runtime Admission, Observation/Action | Capability owner for logical/binding error; runtime owner for executable error |

## Freeze rules

- Policy owner and enforcement point are separate.
- A consumer may enforce or block but may not weaken policy.
- Brain owns global precedence binding; it does not own every local enforcement implementation.
- Constraint refs must carry scope, version, provenance and stale/revocation state.
- A constraint conflict is a governed record, not permission for a consumer to invent a new global policy.

