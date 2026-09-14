# A / Loop / Decision / Action Boundary

## A → Loop

A produces semantic decisions or supplied semantic refs. Loop validates authority, scope, grant, and state version, then mechanically records Need refs, state versions, pause/wait/resume, supersede, close, freeze, outcome and history.

Loop must not compute Need, Sufficiency, Reconsideration, semantic resume reason, closure reason, or local disposition. Existing legacy helpers remain compatibility/retirement candidates, not canonical authority.

## A → Decision/Action

A local semantic disposition is not automatically a Decision or Action. The conceptual handoff is:

`A local disposition → Brain/Decision Governance as applicable → Task/Action execution`.

A does not execute external actions, mutate Task lifecycle, or become Decision/Action owner.
