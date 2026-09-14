# Capability Boundary, Authority Contract and Runtime Grant Model

## Three separate concepts

### Capability Boundary

Capability Boundary defines what a module or reasoning role is structurally
capable of doing. It is immutable for the granted context and cannot be
expanded by a Runtime Authority Grant.

Examples:

| Role | Allowed structural capability | Immutable forbidden capability |
|---|---|---|
| Brain | global concern/goal/safety/resource governance, adjudication, assimilation | direct detailed local reasoning after delegation; Provider identity selection |
| A | reality reasoning, Need judgment, Hypothesis reasoning, evidence relevance, local sufficiency, B request | Concern admission/split/merge, Provider identity, Loop mechanics authority |
| B | bounded contingency reasoning, scenario exploration, contingency result formation | Concern ownership, final Need/sufficiency, result adoption, Loop control |
| Loop | persistence, state recording, pause/wait storage, trace, closure/history mechanics | semantic judgment, Capability selection, B request, Truth, Concern split/merge |
| Capability/Model Governance | Scope, Resolution, Invocation candidate, Provider/model mapping | cognitive conclusion, World Truth, Goal, Decision, Action |

Brain Runtime Grant cannot grant a forbidden Capability Boundary item.

### Authority Contract

Authority Contract defines which role class is eligible to exercise a semantic
authority:

- Brain: Concern admission, Concern identity, split/merge, global Goal,
  global priority, final adjudication and assimilation;
- A: local Need, Hypothesis, evidence relevance, local sufficiency,
  reconsideration, Observation/Capability requests, B request and local
  continuation;
- B: bounded contingency reasoning only;
- Loop: mechanical persistence and lifecycle operations;
- Capability/Model Governance: Scope, Resolution, Invocation and Provider
  identity mapping.

### Runtime Authority Grant

Runtime Authority Grant is a concrete, scoped permission for one work instance
and one cognitive context. It is:

- scoped to a receiver, Concern and Work;
- bounded by Capability Boundary and Authority Contract;
- revocable;
- expiring or condition-bounded;
- linked to a result receiver and responsibility owner;
- traceable and candidate-only in this phase.

## Non-escalation rule

Granting runtime authority changes what an eligible role may exercise for one
work instance. It does not change the role's Capability Boundary, canonical
owner or semantic identity.

## Expiry and revocation

Grant validity begins at valid_from_state_ref and ends when any
valid_until_condition_ref is met. A grant may also be revoked when a
revocation_condition_ref is met, including:

- source state version becomes stale;
- Concern is superseded, merged or globally stopped;
- Safety, Permission or Resource boundary changes;
- requested scope exceeds the grant;
- receiver role or capability boundary is no longer eligible;
- result receiver or responsibility owner is no longer valid.

Revocation is a governance decision associated with the issuer or explicitly
declared revocation authority. Loop may mechanically stop accepting commands
after revocation, but Loop cannot decide that semantic revocation occurred.
Expiry and revocation do not retroactively invalidate already recorded trace
history; they invalidate future exercise of the grant.
